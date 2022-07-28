import pytest
import json
import dateutil.parser
import uuid
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.utils import timezone
from collection_service.collection.api.serializers import CollectionSerializer
from collection_service.users.models import Service

pytestmark = pytest.mark.django_db


class TestCollectionView(TestCase):

    read_token = None
    write_token = None
    generated_collections = []

    @classmethod
    def setUpTestData(self):
        client = APIClient()
        self.api_client = client

        read_permission_service = Service.objects.create(origin="gfbio:collections:read", username="read")
        read_permission_service.user_permissions.add(Permission.objects.get(codename="view_collection"))
        self.read_token = "Token " + Token.objects.create(user=read_permission_service).key

        write_permission_service = Service.objects.create(origin="gfbio:collections:write", username="write")
        write_permission_service.user_permissions.add(Permission.objects.get(codename="add_collection"))
        self.write_token = "Token " + Token.objects.create(user=write_permission_service).key

        collection_test_data = [
            # Two test-collections for user 17
            {
                "set": [
                    "00c0ffee",
                    "447-abc"
                ],
                "service": read_permission_service,
                "external_user_id": "17"
            },
            {
                "set": [
                    "Code red"
                ],
                "service": write_permission_service,
                "external_user_id": "17"
            },
            # One test-collection for different user
            {
                "set": [
                    "Test5",
                ],
                "service": read_permission_service,
                "external_user_id": "5"
            },
            # Collection with anonymous user
            {
                "set": [
                    "ano-1",
                    "ano-2"
                ],
                "service": read_permission_service
            }
        ]

        for entry in collection_test_data:
            serializer = CollectionSerializer(
                data=entry
            )
            if serializer.is_valid():
                self.generated_collections.append(serializer.save())

    def test_get_collections_list_for_known_external_user_id(self):
        response = self.api_client.get('/api/collections/users/17/', HTTP_AUTHORIZATION=self.read_token)
        content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(content))
        self.assertEqual(str(self.generated_collections[0].id), content[0]["id"])
        self.assertTrue("set" in content[0])
        self.assertTrue("created" in content[0])
        self.assertFalse("modified" in content[0])

    def test_get_collections_list_for_unknown_external_user_id(self):
        response = self.api_client.get('/api/collections/users/8/', HTTP_AUTHORIZATION=self.read_token)
        content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(content))

    def test_get_collections_list_not_authenticated(self):
        response = self.api_client.get('/api/collections/users/17/')
        self.assertEqual(403, response.status_code)

    def test_get_collections_list_no_permission(self):
        response = self.api_client.get('/api/collections/users/17/', HTTP_AUTHORIZATION=self.write_token)
        self.assertEqual(403, response.status_code)

    def test_get_collections_list_for_not_a_service(self):
        user = Service.objects.create(username="TestUser")
        user.user_permissions.add(Permission.objects.get(codename="view_collection"))
            
        token = "Token " + Token.objects.create(user=user).key
        response = self.api_client.get('/api/collections/users/17/', HTTP_AUTHORIZATION=token)

        self.assertEqual(403, response.status_code)

    def test_get_specific_collection(self):
        test_id = str(self.generated_collections[0].id)
        response = self.api_client.get(f'/api/collections/{test_id}/', HTTP_AUTHORIZATION=self.read_token)
        content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual(test_id, content["id"])
        self.assertTrue("set" in content)
        self.assertEqual("00c0ffee", content["set"][0])
        self.assertEqual("gfbio:collections:read", content["origin"])

    def test_get_invalid_collection(self):
        response = self.api_client.get('/api/collections/87654321-4321-4321-4321-cba987654321/',
            HTTP_AUTHORIZATION=self.read_token)
        self.assertEqual(404, response.status_code)

    def test_get_specific_collection_not_authenticated(self):
        test_id = str(self.generated_collections[0].id)
        response = self.api_client.get(f'/api/collections/{test_id}/')
        self.assertEqual(403, response.status_code)

    def test_get_specific_collection_no_permission(self):
        test_id = str(self.generated_collections[0].id)
        response = self.api_client.get(f'/api/collections/{test_id}/', HTTP_AUTHORIZATION=self.write_token)
        self.assertEqual(403, response.status_code)

    def test_post_valid_collection_with_user(self):
        test_collection = {
            "external_user_id": "17",
            "set": ["abc", "def", "ghi"],
        }
        response = self.api_client.post('/api/collections/', test_collection, format="json",
            HTTP_AUTHORIZATION=self.write_token)

        self.assertEqual(201, response.status_code)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual("17", content["external_user_id"])
        self.assertEqual("abc", content["set"][0])
        self.assertEqual("gfbio:collections:write", content["origin"])
        self.assertTrue((timezone.now() - dateutil.parser.isoparse(content["created"])).total_seconds() < 10)

    def test_post_valid_collection_anonymous(self):
        test_collection = {
            "set": ["abc", "def", "ghi"],
        }
        response = self.api_client.post('/api/collections/', test_collection, format="json",
            HTTP_AUTHORIZATION=self.write_token)

        self.assertEqual(201, response.status_code)
        content = json.loads(response.content.decode('utf-8'))
        self.assertIsNone(content["external_user_id"])

    def test_post_valid_collection_with_dictionary_as_set(self):
        test_collection = {
            "external_user_id": "17",
            "set": {
                "at": "def",
                "de": "abc",
                "ch": "ghi"
            }
        }
        response = self.api_client.post('/api/collections/', test_collection, format="json",
            HTTP_AUTHORIZATION=self.write_token)

        self.assertEqual(201, response.status_code)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual("abc", content["set"]["de"])

    def test_post_invalid_collection_no_set(self):
        test_collection = {
            "external_user_id": "Test-User"
        }
        response = self.api_client.post('/api/collections/', test_collection, format="json",
            HTTP_AUTHORIZATION=self.write_token)

        self.assertEqual(400, response.status_code)

    def test_post_invalid_collection_empty(self):
        test_collection = {}
        response = self.api_client.post('/api/collections/', test_collection, format="json",
            HTTP_AUTHORIZATION=self.write_token)

        self.assertEqual(400, response.status_code)

    def test_post_ignores_given_id(self):
        test_guid = uuid.uuid4()
        test_collection = {
            "set": ["abc", "def", "ghi"],
            "id": test_guid
        }
        response = self.api_client.post('/api/collections/', test_collection, format="json",
            HTTP_AUTHORIZATION=self.write_token)
        content = json.loads(response.content)

        self.assertEqual(201, response.status_code)
        self.assertNotEqual(str(test_guid), str(content["id"]))

    def test_post_ignores_given_created_date(self):
        test_date = "2022-01-01T00:00:00.0"
        test_collection = {
            "set": ["abc", "def", "ghi"],
            "created": test_date
        }
        response = self.api_client.post('/api/collections/', test_collection, format="json",
            HTTP_AUTHORIZATION=self.write_token)
        content = json.loads(response.content)

        self.assertEqual(201, response.status_code)
        self.assertNotEqual(str(test_date), str(content["created"]))

    def test_post_collections_not_authenticated(self):
        test_collection = {
            "set": ["abc", "def", "ghi"],
        }
        response = self.api_client.post('/api/collections/', test_collection, format="json")
        self.assertEqual(403, response.status_code)

    def test_post_collections_no_permission(self):

        test_collection = {
            "set": ["abc", "def", "ghi"],
        }
        response = self.api_client.post('/api/collections/', test_collection, format="json",
            HTTP_AUTHORIZATION=self.read_token)
        self.assertEqual(403, response.status_code)
