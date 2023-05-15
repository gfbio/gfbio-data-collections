import pytest
import json
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import Permission
from django.test import TestCase
from collection_service.collection.api.serializers import CollectionSerializer
from collection_service.users.models import Service

pytestmark = pytest.mark.django_db


class TestCollectionViewRead(TestCase):

    read_token = None
    other_token = None
    generated_collections = []

    @classmethod
    def setUpTestData(self):
        client = APIClient()
        self.api_client = client

        read_permission_service = Service.objects.create(origin="gfbio:collections:read", username="read")
        read_permission_service.user_permissions.add(Permission.objects.get(codename="view_collection"))
        self.read_token = "Token " + Token.objects.create(user=read_permission_service).key

        other_permission_service = Service.objects.create(origin="gfbio:collections:add", username="add")
        self.other_token = "Token " + Token.objects.create(user=other_permission_service).key

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
                "service": other_permission_service,
                "external_user_id": "17"
            },
            # One test-collection for different user
            {
                "set": [
                    "Test3",
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
        response = self.api_client.get('/api/collections/users/17/', HTTP_AUTHORIZATION=self.other_token)
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
        response = self.api_client.get(
            '/api/collections/87654321-4321-4321-4321-cba987654321/',
            HTTP_AUTHORIZATION=self.read_token
        )
        self.assertEqual(404, response.status_code)

    def test_get_specific_collection_not_authenticated(self):
        test_id = str(self.generated_collections[0].id)
        response = self.api_client.get(f'/api/collections/{test_id}/')
        self.assertEqual(403, response.status_code)

    def test_get_specific_collection_no_permission(self):
        test_id = str(self.generated_collections[0].id)
        response = self.api_client.get(f'/api/collections/{test_id}/', HTTP_AUTHORIZATION=self.other_token)
        self.assertEqual(403, response.status_code)
