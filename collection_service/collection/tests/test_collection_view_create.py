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


class TestCollectionViewCreate(TestCase):

    other_token = None
    add_token = None
    schema_service_token = None
    generated_collections = []

    @classmethod
    def setUpTestData(self):
        client = APIClient()
        self.api_client = client

        add_permission_service = Service.objects.create(origin="gfbio:collections:add", username="add")
        add_permission_service.user_permissions.add(Permission.objects.get(codename="add_collection"))
        self.add_token = "Token " + Token.objects.create(user=add_permission_service).key

        other_permission_service = Service.objects.create(origin="gfbio:collections:read", username="read")
        other_permission_service.user_permissions.add(Permission.objects.get(codename="view_collection"))
        self.other_token = "Token " + Token.objects.create(user=other_permission_service).key

        permission_service_with_schema = Service.objects.create(
            origin="gfbio:collections:with_schema",
            username="schema",
            validation_schema={
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "string"
                        },
                        "name": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "id", "name"
                    ]
                }
            }
        )
        permission_service_with_schema.user_permissions.add(Permission.objects.get(codename="add_collection"))
        permission_service_with_schema.user_permissions.add(Permission.objects.get(codename="change_collection"))
        self.schema_service_token = "Token " + Token.objects.create(user=permission_service_with_schema).key

        collection_test_data = [
            # Two test-collections for user 17
            {
                "set": [
                    "00c0ffee",
                    "447-abc"
                ],
                "service": other_permission_service,
                "external_user_id": "17"
            },
            {
                "set": [
                    "Code red"
                ],
                "service": add_permission_service,
                "external_user_id": "17"
            },
            # One test-collection for different user
            {
                "set": [
                    "Test3",
                ],
                "service": other_permission_service,
                "external_user_id": "5"
            },
            # Collection with anonymous user
            {
                "set": [
                    "ano-1",
                    "ano-2"
                ],
                "service": other_permission_service
            }
        ]

        for entry in collection_test_data:
            serializer = CollectionSerializer(
                data=entry
            )
            if serializer.is_valid():
                self.generated_collections.append(serializer.save())

    def test_post_valid_collection_with_user(self):
        test_collection = {
            "external_user_id": "17",
            "set": ["abc", "def", "ghi"],
        }
        response = self.api_client.post(
            '/api/collections/',
            test_collection,
            format="json",
            HTTP_AUTHORIZATION=self.add_token
        )

        self.assertEqual(201, response.status_code)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual("17", content["external_user_id"])
        self.assertEqual("abc", content["set"][0])
        self.assertEqual("gfbio:collections:add", content["origin"])
        self.assertTrue((timezone.now() - dateutil.parser.isoparse(content["created"])).total_seconds() < 10)

    def test_post_valid_collection_no_user_id(self):
        test_collection = {
            "set": ["abc", "def", "ghi"],
        }
        response = self.api_client.post(
            '/api/collections/',
            test_collection,
            format="json",
            HTTP_AUTHORIZATION=self.add_token
        )

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
        response = self.api_client.post(
            '/api/collections/',
            test_collection,
            format="json",
            HTTP_AUTHORIZATION=self.add_token
        )

        self.assertEqual(201, response.status_code)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual("abc", content["set"]["de"])

    def test_post_invalid_collection_no_set(self):
        test_collection = {
            "external_user_id": "Test-User"
        }
        response = self.api_client.post(
            '/api/collections/',
            test_collection,
            format="json",
            HTTP_AUTHORIZATION=self.add_token
        )

        self.assertEqual(400, response.status_code)

    def test_post_invalid_collection_empty(self):
        test_collection = {}
        response = self.api_client.post(
            '/api/collections/',
            test_collection,
            format="json",
            HTTP_AUTHORIZATION=self.add_token
        )

        self.assertEqual(400, response.status_code)

    def test_post_ignores_given_id(self):
        test_guid = uuid.uuid4()
        test_collection = {
            "set": ["abc", "def", "ghi"],
            "id": test_guid
        }
        response = self.api_client.post(
            '/api/collections/',
            test_collection,
            format="json",
            HTTP_AUTHORIZATION=self.add_token
        )
        content = json.loads(response.content)

        self.assertEqual(201, response.status_code)
        self.assertNotEqual(str(test_guid), str(content["id"]))

    def test_post_ignores_given_created_date(self):
        test_date = "2022-01-01T00:00:00.0"
        test_collection = {
            "set": ["abc", "def", "ghi"],
            "created": test_date
        }
        response = self.api_client.post(
            '/api/collections/',
            test_collection,
            format="json",
            HTTP_AUTHORIZATION=self.add_token
        )
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
        response = self.api_client.post(
            '/api/collections/',
            test_collection,
            format="json",
            HTTP_AUTHORIZATION=self.other_token
        )
        self.assertEqual(403, response.status_code)

    def test_post_valid_collection_against_schema(self):
        test_collection = {
            "external_user_id": "17",
            "set": [
                {
                    "id": "Test123",
                    "name": "TestData"
                },
                {
                    "id": "Test124",
                    "name": "TestData2"
                }
            ],
        }
        response = self.api_client.post(
            '/api/collections/',
            test_collection,
            format="json",
            HTTP_AUTHORIZATION=self.schema_service_token
        )

        self.assertEqual(201, response.status_code)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual("Test123", content["set"][0]["id"])
        self.assertEqual("gfbio:collections:with_schema", content["origin"])

    def test_post_invalid_collection_against_schema_fails(self):
        test_collection = {
            "external_user_id": "17",
            "set": [
                {
                    "id": "Test123",
                    "name": "TestData"
                },
                {
                    "id": 1235,
                    "url": "TestData2"
                }
            ],
        }
        response = self.api_client.post(
            '/api/collections/',
            test_collection,
            format="json",
            HTTP_AUTHORIZATION=self.schema_service_token
        )

        self.assertEqual(400, response.status_code)
        content = json.loads(response.content.decode('utf-8'))["non_field_errors"]
        self.assertEqual("1 : 'name' is a required property", content[0])
        self.assertEqual("id : 1235 is not of type 'string'", content[1])
