import pytest
from collection_service.collection.api.serializers import CollectionSerializer
from collection_service.collection.models import Collection
from django.test import TestCase
from django.utils import timezone

pytestmark = pytest.mark.django_db


class TestCollectionSerializer(TestCase):

    def test_serializer_works_with_all_data(self):
        test_collection = {
            "external_user_id": "17",
            "set": ["abc", "def", "ghi"],
            "origin": "gfbio.collections.testData"
        }
        test_serializer = CollectionSerializer(data=test_collection)
        test_serializer.is_valid(True)
        saved = test_serializer.save()
        self.assertEqual("17", saved.external_user_id)
        self.assertEqual("abc", saved.set[0])
        self.assertEqual("gfbio.collections.testData", saved.origin)
        self.assertTrue((timezone.now() - saved.created).total_seconds() < 4 )

    def test_serializer_works_with_anonymous_user(self):
        test_collection = {
            "set": ["abc", "def", "ghi"],
            "origin": "gfbio.collections.testData"
        }
        test_serializer = CollectionSerializer(data=test_collection)
        test_serializer.is_valid(True)
        saved = test_serializer.save()
        self.assertIsNone(saved.external_user_id)

    def test_serializer_works_with_no_origin(self):
        test_collection = {
            "set": ["abc", "def", "ghi"],
        }
        test_serializer = CollectionSerializer(data=test_collection)
        if(test_serializer.is_valid()):
            self.fail("Should not be valid without origin.")

    def test_serializer_works_with_no_set(self):
        test_collection = {
            "origin": "gfbio.collections.testData"
        }
        test_serializer = CollectionSerializer(data=test_collection)
        if(test_serializer.is_valid()):
            self.fail("Should not be valid without a set.")
