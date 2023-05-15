import pytest
import json
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import Permission
from django.test import TestCase
from collection_service.collection.api.serializers import CollectionSerializer
from collection_service.users.models import Service

pytestmark = pytest.mark.django_db


class TestCollectionViewUpdate(TestCase):

    update_token = None
    updateOfOthers_token = None
    other_token = None
    schema_service_token = None
    generated_collections = []

    valid_test_collection = {
        "external_user_id": "17",
        "set": [
            {
                "id": "Test123",
                "name": "TestData"
            },
            {
                "id": "Test321",
                "name": "TestData2"
            }
        ],
    }

    invalid_test_collection = {
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

    @classmethod
    def setUpTestData(self):
        client = APIClient()
        self.api_client = client

        other_permission_service = Service.objects.create(origin="gfbio:collections:other", username="other")
        self.other_token = "Token " + Token.objects.create(user=other_permission_service).key

        update_permission_service = Service.objects.create(origin="gfbio:collections:update", username="update")
        update_permission_service.user_permissions.add(Permission.objects.get(codename="change_collection"))
        self.update_token = "Token " + Token.objects.create(user=update_permission_service).key

        updateOfOthers_permission_service = Service.objects.create(
            origin="gfbio:collections:updateOfOthers",
            username="updateOfOthers"
        )
        updateOfOthers_permission_service.user_permissions.add(
            Permission.objects.get(codename="change_collection")
        )
        updateOfOthers_permission_service.user_permissions.add(
            Permission.objects.get(codename="change_collection_of_other_service")
        )
        self.updateOfOthers_token = "Token " + Token.objects.create(user=updateOfOthers_permission_service).key

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
        permission_service_with_schema.user_permissions.add(Permission.objects.get(codename="change_collection"))
        self.schema_service_token = "Token " + Token.objects.create(user=permission_service_with_schema).key

        collection_test_data = [
            # Two test-collections for user 17
            {
                "set": [
                    "00c0ffee",
                    "447-abc"
                ],
                "service": update_permission_service,
                "external_user_id": "17"
            },
            {
                "set": [
                    "Code red"
                ],
                "service": update_permission_service,
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
            },
            # Collection of service with delete rights
            {
                "set": [
                    "Test5",
                ],
                "service": other_permission_service
            },
            # Collection with schema
            {
                "external_user_id": "24",
                "set": [
                    {
                        "id": "Test6.1",
                        "name": "TestData"
                    },
                    {
                        "id": "Test6.2",
                        "name": "TestData2"
                    }
                ],
                "service": permission_service_with_schema
            }
        ]

        for entry in collection_test_data:
            serializer = CollectionSerializer(
                data=entry
            )
            if serializer.is_valid():
                self.generated_collections.append(serializer.save())

    def test_put_valid_collection_to_own_collection(self):
        test_id = str(self.generated_collections[0].id)
        test_collection = {
            "set": [
                "00c0ffee",
                "447-abc",
                "another thing"
            ],
            "external_user_id": "17",
        }
        response = self.api_client.put(
            f'/api/collections/{test_id}/',
            test_collection,
            format="json",
            HTTP_AUTHORIZATION=self.update_token
        )

        self.assertEqual(200, response.status_code)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual("00c0ffee", content["set"][0])
        self.assertEqual("another thing", content["set"][2])
        self.assertEqual("gfbio:collections:update", content["origin"])

    def test_put_invalid_collection_to_own_collection(self):
        test_id = str(self.generated_collections[0].id)
        response = self.api_client.put(
            f'/api/collections/{test_id}/',
            {},
            format="json",
            HTTP_AUTHORIZATION=self.update_token
        )

        self.assertEqual(400, response.status_code)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual('This field is required.', content["set"][0])

    def test_put_valid_collection_against_schema_own_collection(self):
        test_id = str(self.generated_collections[5].id)
        response = self.api_client.put(
            f'/api/collections/{test_id}/',
            self.valid_test_collection,
            format="json",
            HTTP_AUTHORIZATION=self.schema_service_token
        )

        self.assertEqual(200, response.status_code)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual("Test123", content["set"][0]["id"])
        self.assertEqual("gfbio:collections:with_schema", content["origin"])

    def test_put_invalid_collection_against_schema_fails_own_collection(self):
        test_id = str(self.generated_collections[5].id)
        response = self.api_client.put(
            f'/api/collections/{test_id}/',
            self.invalid_test_collection,
            format="json",
            HTTP_AUTHORIZATION=self.schema_service_token
        )

        self.assertEqual(400, response.status_code)
        content = json.loads(response.content.decode('utf-8'))["non_field_errors"]
        self.assertEqual("1 : 'name' is a required property", content[0])
        self.assertEqual("id : 1235 is not of type 'string'", content[1])

    def test_put_valid_collection_against_schema_others_collection(self):
        test_id = str(self.generated_collections[5].id)
        response = self.api_client.put(
            f'/api/collections/{test_id}/',
            self.valid_test_collection,
            format="json",
            HTTP_AUTHORIZATION=self.updateOfOthers_token
        )

        self.assertEqual(200, response.status_code)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual("Test123", content["set"][0]["id"])
        self.assertEqual("gfbio:collections:with_schema", content["origin"])

    def test_put_invalid_collection_against_schema_fails_others_collection(self):
        test_id = str(self.generated_collections[5].id)
        response = self.api_client.put(
            f'/api/collections/{test_id}/',
            self.invalid_test_collection,
            format="json",
            HTTP_AUTHORIZATION=self.updateOfOthers_token
        )

        self.assertEqual(400, response.status_code)
        content = json.loads(response.content.decode('utf-8'))["non_field_errors"]
        self.assertEqual("1 : 'name' is a required property", content[0])
        self.assertEqual("id : 1235 is not of type 'string'", content[1])

    def test_put_collection_missing_permission_other_collection_fails(self):
        test_id = str(self.generated_collections[2].id)
        response = self.api_client.put(
            f'/api/collections/{test_id}/', self.valid_test_collection,
            HTTP_AUTHORIZATION=self.update_token
        )

        self.assertEqual(403, response.status_code)

    def test_put_collection_missing_permission_fails(self):
        test_id = str(self.generated_collections[1].id)
        response = self.api_client.put(
            f'/api/collections/{test_id}/', self.valid_test_collection,
            HTTP_AUTHORIZATION=self.other_token
        )

        self.assertEqual(403, response.status_code)

    def test_put_collection_missing_auth_fails(self):
        test_id = str(self.generated_collections[1].id)
        response = self.api_client.put(f'/api/collections/{test_id}/', self.valid_test_collection)

        self.assertEqual(403, response.status_code)

    def test_put_to_missing_collection_fails(self):
        test_id = str("Non-Exsiting")
        response = self.api_client.put(
            f'/api/collections/{test_id}/', self.valid_test_collection,
            HTTP_AUTHORIZATION=self.updateOfOthers_token
        )

        self.assertEqual(404, response.status_code)
