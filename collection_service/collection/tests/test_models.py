import re
from django.test import TestCase
from django.utils import timezone
from collection_service.collection.models import Collection
from collection_service.users.models import Service


class TestCollectionModel(TestCase):

    def test_valid(self):
        test_collection = Collection(
            external_user_id=17,
            set=["abc", "def", "ghi"],
            service=Service(origin="gfbio:test")
        )
        self.assertEqual(17, test_collection.external_user_id)
        self.assertEqual("abc", test_collection.set[0])
        self.assertEqual("gfbio:test", test_collection.service.origin)
        self.assertTrue((timezone.now() - test_collection.created).total_seconds() < 4)
        self.assertTrue((timezone.now() - test_collection.modified).total_seconds() < 4)

    def test_autoGuid(self):
        test_collection = Collection()
        self.assertIsNotNone(test_collection.id)
        guid_regex = r"^[0-9A-Fa-f]{8}(\-[0-9A-Fa-f]{4}){3}\-[0-9A-Fa-f]{12}$"
        self.assertIsNotNone(re.fullmatch(guid_regex, str(test_collection.id)))

    def test_str(self):
        test_collection = Collection()
        name_regex = r"^collection_[0-9A-Fa-f]{8}(\-[0-9A-Fa-f]{4}){3}\-[0-9A-Fa-f]{12}$"
        self.assertIsNotNone(re.fullmatch(name_regex, str(test_collection)))
