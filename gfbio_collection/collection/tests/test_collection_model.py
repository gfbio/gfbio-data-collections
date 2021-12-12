
import os
import json
import base64
import responses
import requests

from django.test import TestCase

from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APIClient

from gfbio_collection.users.models import User
from gfbio_collection.collection.models import Collection

from django.core.management.commands.test import Command as BaseCommand

# wrap django's built-in test command to always delete the database if it exists [ref](# https://adamj.eu/tech/2020/01/13/make-django-tests-always-rebuild-db/)
class Command(BaseCommand):
    def handle(self, *test_labels, **options):
        options["interactive"] = False
        return super().handle(*test_labels, **options)

# TestCollectionViewBase instantiate a user and credentials into api_client
# the simple self.client is used for tests without credentials
class TestCollectionViewBase(TestCase):

    @classmethod
    def setUpTestData(cls):

        # fresh user
        user = User.objects.create_user(
            username='new_user', email='new@user.de', password='pass1234', )
        user.save()

        client = APIClient()

        cls.api_client = client


class TestCollectionViewGetRequests(TestCollectionViewBase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        user = User.objects.get(username='new_user')
        user.is_user = True
        user.is_site = False
        user.save()

    # 200 successful HTTP request
    def test_get(self):
        response = self.client.get('/api/collections/')
        self.assertEqual(200, response.status_code)

    # 404 not found
    def test_get(self):
        # "collection" without s requires an {id}
        response = self.client.get('/api/collection/')
        self.assertEqual(404, response.status_code)

    # no text or bad format causes deserialization failure
    def test_get_json(self):
        response = self.client.get('/api/collections/')
        # following replaces deserialization with "assert(response.json())":
        self.assertEqual(response.json(),list())

    # not 401 unauthorized
    def test_get_with_wrong_credentials(self):
        # it does not make a difference if credentials are given
        self.api_client.credentials(
            HTTP_AUTHORIZATION='Basic ' + base64.b64encode(
                b'user:invalidpassword').decode('utf-8')
        )
        response = self.api_client.get('/api/collections/')
        self.assertNotEqual(401, response.status_code)

    # 201 created
    def test_simple_post(self):
        self.assertEqual(0, len(Collection.objects.all()))
        # response = self.api_client.post(
        #     '/api/collections/',
        #     {'metadata': "0123456",
        #      'hits': {
        #          'collection_payload':
        #              [
        #                  {
        #                      "_id": "001.002.003",
        #                      "_source": {"dataid": "001.002.003", "content": [3, 2, 1], "valid": False}
        #                  }
        #              ]
        #      }
        #      },
        #     format='json'
        # )

        collection_payload = {
            "took": 511,
            "_shards": {
                "total": 2,
            },
            "hits":
                {
                    "max_score": 1.0,
                    "hits":
                        [
                            {
                                "_index": "portals_v2",
                                "_type": "pansimple",
                                "_id": "urn:gfbio.org:abcd:2_292_277:7638959+/+22948775",
                                "_score": 1.0,
                                "_source": {
                                    "accessRestricted": False,
                                    "parameter": [
                                        "Date",
                                        "Locality",
                                        "Longitude",
                                        "Latitude"
                                    ],
                                }
                            },
                            {},
                        ]
                },
        }
        response = self.api_client.post(
            '/api/collections/',
            {'collection_payload': collection_payload},
            format='json',
        )

        self.assertEqual(201, response.status_code)
        self.assertIn(b'id', response.content)
        self.assertIn(b'collection_payload', response.content)

    # test data case with local data request
    def test_get_json_and_post(self):

        headers = requests.structures.CaseInsensitiveDict()
        headers["Accept"] = "application/json"

        # # get data remotely
        # url = "http://ws.pangaea.de/es/portals/pansimple/_search?pretty="
        # response = requests.get(url, headers=headers)
        # json_data = response.json()

        # get data locally
        with open(os.path.join(
            './test_data',
            '_search.json'), 'r') as data_file:
            json_data = json.load(data_file)

        # post to collections
        response = self.api_client.post(
            '/api/collections/',
            {'collection_payload': json_data},
            format='json'
        )
        self.assertEqual(201, response.status_code)

        # get from collection
        # compare entry json used in post with the retrieved one from collection (nothing changed)
        response = self.api_client.get('/api/collections/', headers=headers)
        self.assertEqual(200, response.status_code)
        json_data_get = response.json()[0]['collection_payload']
        self.assertEqual(json_data_get, json_data)
