
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

    # test for attribute names, the model bellow should be hardwired
    def test_simple_collection(self):
        serializer = CollectionSerializer(data={
            'id': 1,
            'collection_name': "new name",
            'payload': {"dataid": "001.002.003", "content": [3, 2, 1], "valid": False}
        })
        valid = serializer.is_valid()
        self.assertTrue(valid)
        self.assertIn('collection_name', serializer.validated_data)
        self.assertIn('payload', serializer.validated_data)

