import pytest
import json
import dateutil.parser
import uuid
from rest_framework.test import APIClient
from django.test import TestCase
from django.utils import timezone
from collection_service.collection.api.serializers import CollectionSerializer

pytestmark = pytest.mark.django_db


class TestCollectionView(TestCase):

    generated_test_data = []

    @classmethod
    def setUpTestData(cls):
        client = APIClient()
        cls.api_client = client

        test_data = [
            # Two test-collections for user 17
            {
                "set": [
                    "00c0ffee",
                    "447-abc"
                ],
                "origin": "gfbio.collectionService.testData.1",
                "external_user_id": "17"
            },
            {
                "set": [
                    "Code red"
                ],
                "origin": "gfbio.collectionService.testData.2",
                "external_user_id": "17"
            },
            # One test-collection for different user
            {
                "set": [
                    "Test5",
                ],
                "origin": "gfbio.collectionService.testData.3",
                "external_user_id": "5"
            },
            # Collection with anonymous user
            {
                "set": [
                    "ano-1",
                    "ano-2"
                ],
                "origin": "gfbio.collectionService.testData.4",
            }
        ]

        for entry in test_data:
            serializer = CollectionSerializer(data=entry)
            if (serializer.is_valid(True)):
                cls.generated_test_data.append(serializer.save())

    def test_get_collections_list_for_known_external_user_id(self):
        response = self.api_client.get('/api/collections/users/17/')
        content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(content))
        self.assertEqual(str(self.generated_test_data[0].id), content[0]["id"])
        self.assertTrue("set" in content[0])

    def test_get_collections_list_for_unknown_external_user_id(self):
        response = self.api_client.get('/api/collections/users/8/')
        content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(content))

    def test_get_specific_collection(self):
        test_id = str(self.generated_test_data[0].id)
        response = self.api_client.get(f'/api/collections/{test_id}/')
        content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual(test_id, content["id"])
        self.assertTrue("set" in content)
        self.assertEqual("00c0ffee", content["set"][0])
        self.assertEqual("gfbio.collectionService.testData.1", content["origin"])

    def test_get_invalid_collection(self):
        response = self.api_client.get('/api/collections/654321-4321-4321-4321-cba987654321/')
        self.assertEqual(404, response.status_code)

    def test_post_valid_collection_with_user(self):
        test_collection = {
            "external_user_id": "17",
            "set": ["abc", "def", "ghi"],
            "origin": "gfbio.collections.testData"
        }
        response = self.api_client.post('/api/collections/', test_collection, format="json")

        self.assertEqual(201, response.status_code)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual("17", content["external_user_id"])
        self.assertEqual("abc", content["set"][0])
        self.assertEqual("gfbio.collections.testData", content["origin"])
        self.assertTrue((timezone.now() - dateutil.parser.isoparse(content["created"])).total_seconds() < 10)

    def test_post_valid_collection_anonymous(self):
        test_collection = {
            "set": ["abc", "def", "ghi"],
            "origin": "gfbio.collections.testData"
        }
        response = self.api_client.post('/api/collections/', test_collection, format="json")

        self.assertEqual(201, response.status_code)
        content = json.loads(response.content.decode('utf-8'))
        self.assertIsNone(content["external_user_id"])

    def test_post_invalid_collection_no_origin(self):
        test_collection = {
            "set": ["abc", "def", "ghi"]
        }
        response = self.api_client.post('/api/collections/', test_collection, format="json")

        self.assertEqual(400, response.status_code)

    def test_post_invalid_collection_no_origin(self):
        test_collection = {
            "origin": "gfbio.collections.testData"
        }
        response = self.api_client.post('/api/collections/', test_collection, format="json")

        self.assertEqual(400, response.status_code)

    def test_post_invalid_collection_empty(self):
        test_collection = {}
        response = self.api_client.post('/api/collections/', test_collection, format="json")

        self.assertEqual(400, response.status_code)

    def test_post_ignores_given_id(self):
        test_guid = uuid.uuid4()
        test_collection = {
            "set": ["abc", "def", "ghi"],
            "origin": "gfbio.collections.testData",
            "id": test_guid
        }
        response = self.api_client.post('/api/collections/', test_collection, format="json")
        content = json.loads(response.content)

        self.assertEqual(201, response.status_code)
        self.assertNotEqual(str(test_guid), str(content["id"]))

    def test_post_ignores_given_created_date(self):
        test_date = "2022-01-01T00:00:00.0"
        test_collection = {
            "set": ["abc", "def", "ghi"],
            "origin": "gfbio.collections.testData",
            "created": test_date
        }
        response = self.api_client.post('/api/collections/', test_collection, format="json")
        content = json.loads(response.content)

        self.assertEqual(201, response.status_code)
        self.assertNotEqual(str(test_date), str(content["created"]))
