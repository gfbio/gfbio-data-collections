import pytest
from django.test import TestCase
from django.utils import timezone
from collection_service.collection.api.serializers import CollectionSerializer
from collection_service.users.models import Service

pytestmark = pytest.mark.django_db


class TestCollectionSerializer(TestCase):
    testService = None

    @classmethod
    def setUpTestData(self):
        self.testService = Service.objects.create(origin="gfbio:collections:test_data")

    def test_serializer_works_with_all_data(self):
        test_collection = {
            "external_user_id": "17",
            "set": ["abc", "def", "ghi"],
            "service": self.testService
        }
        test_serializer = CollectionSerializer(data=test_collection)
        self.assertTrue(test_serializer.is_valid())
        saved = test_serializer.save()
        self.assertEqual("17", saved.external_user_id)
        self.assertEqual("abc", saved.set[0])
        self.assertEqual("gfbio:collections:test_data", test_serializer.data["origin"])
        self.assertTrue((timezone.now() - saved.created).total_seconds() < 4)
        self.assertTrue((timezone.now() - saved.modified).total_seconds() < 4)

    def test_serializer_works_with_anonymous_user(self):
        test_collection = {
            "set": ["abc", "def", "ghi"],
            "service": self.testService
        }
        test_serializer = CollectionSerializer(data=test_collection)
        self.assertTrue(test_serializer.is_valid())
        saved = test_serializer.save()
        self.assertIsNone(saved.external_user_id)

    def test_serializer_fails_with_no_service(self):
        test_collection = {
            "set": ["abc", "def", "ghi"],
        }
        test_serializer = CollectionSerializer(data=test_collection)
        self.assertFalse(test_serializer.is_valid())

    def test_serializer_fails_with_unknown_service(self):
        test_collection = {
            "set": ["abc", "def", "ghi"],
            "service": Service()
        }
        test_serializer = CollectionSerializer(data=test_collection)
        self.assertFalse(test_serializer.is_valid())

    def test_serializer_fails_with_no_set(self):
        test_collection = {
            "service": self.testService
        }
        test_serializer = CollectionSerializer(data=test_collection)
        self.assertFalse(test_serializer.is_valid())

    def test_serializer_fails_with_empty_set(self):
        test_collection = {
            "set": [],
            "service": self.testService
        }
        test_serializer = CollectionSerializer(data=test_collection)
        self.assertFalse(test_serializer.is_valid())

    def test_serializer_fails_with_trivial_json_for_set(self):
        test_collection = {
            "set": "Muhaha",
            "service": self.testService
        }
        test_serializer = CollectionSerializer(data=test_collection)
        self.assertFalse(test_serializer.is_valid())
