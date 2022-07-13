import pytest
import re
from collection_service.collection.models import Collection
from django.test import TestCase


class TestCollectionModel(TestCase):

    def test_valid(self):
        test_collection = Collection(external_user_id = 17, set = ["abc", "def", "ghi"], origin="gfbio.collections.testData")
        self.assertEqual(17, test_collection.external_user_id)
        self.assertEqual("abc", test_collection.set[0])
        self.assertEqual("gfbio.collections.testData", test_collection.origin)

    def test_autoGuid(self):
        test_collection = Collection()
        self.assertIsNotNone(test_collection.id)
        self.assertIsNotNone(re.fullmatch(r"^collection_[0-9A-Fa-f]{8}(\-[0-9A-Fa-f]{4}){3}\-[0-9A-Fa-f]{12}$", str(test_collection)))

    def test_str(self):
        test_collection = Collection()
        self.assertIsNotNone(re.fullmatch(r"^collection_[0-9A-Fa-f]{8}(\-[0-9A-Fa-f]{4}){3}\-[0-9A-Fa-f]{12}$", str(test_collection)))
