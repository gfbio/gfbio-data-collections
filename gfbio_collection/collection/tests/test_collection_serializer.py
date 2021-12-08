
import os
import json
import base64
import responses
import requests

from django.test import TestCase

from gfbio_collection.collection.api.serializers import CollectionSerializer

from django.core.management.commands.test import Command as BaseCommand

# wrap django's built-in test command to always delete the database if it exists [ref](https://adamj.eu/tech/2020/01/13/make-django-tests-always-rebuild-db/)
class Command(BaseCommand):
    def handle(self, *test_labels, **options):
        options["interactive"] = False
        return super().handle(*test_labels, **options)

class CollectionSerializerTest(TestCase):

    # test for attribute names, the model bellow should be hardwired, i.e. contains the attributes "payload" as written
    def test_empty_collection(self):
        attribute_name = "collection_payload"
        serializer = CollectionSerializer(data={
            'collection_identifier': 1,
            attribute_name: {}
        })
        valid = serializer.is_valid()
        self.assertFalse(valid)

    # test for attribute name, the model bellow should be hardwired, i.e. contains at least the attribute "payload" as written
    # fixme: the attribute contnt is already considered in the schema right?
    # def test_contains_expected_attribute(self):
    #     attribute_name = "collection_payload"
    #     serializer = CollectionSerializer(data={
    #         'collection_identifier': 1,
    #         attribute_name: {"dataid": "001.002.003", "content": [3, 2, 1], "valid": False}
    #     })
    #     valid = serializer.is_valid()
    #     self.assertTrue(valid)
    #     self.assertIn(attribute_name, serializer.validated_data)
