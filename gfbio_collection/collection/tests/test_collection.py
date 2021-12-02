
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
    @responses.activate
    def setUpTestData(cls):
        super().setUpTestData()

        user = User.objects.get(username='new_user')
        user.is_user = True
        user.is_site = False
        user.save()

    # 200 successful HTTP request
    @responses.activate
    def test_get(self):
        response = self.api_client.get('/api/collections/')
        self.assertEqual(200, response.status_code)
        # 404 not found
        self.assertEqual(404, response.status_code)

    # no text or bad format causes deserialization failure
    @responses.activate
    def test_get_json(self):
        response = self.api_client.get('/api/collections/')
        self.assertEqual(200, response.status_code)
        # deserialization fails with empty json
        assert(response.json())

    # unauthorized
    @responses.activate
    def test_get_without_credentials(self):
        response = self.api_client.get('/api/collections/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(401, response.status_code)

        # it does not make a difference if credentials are given
        self.api_client.credentials(
            HTTP_AUTHORIZATION='Basic ' + base64.b64encode(
                b'user:invalidpassword').decode('utf-8')
        )
        response = self.api_client.get('/api/collections/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(401, response.status_code)

    # 201 created
    @responses.activate
    def test_simple_post(self):
        self.assertEqual(0, len(Collection.objects.all()))
        response = self.api_client.post(
            '/api/collections/',
            {'payload': {"dataid":"001.002.003", "content":[3,2,1], "valid":null}},
            format='json'
        )
        self.assertEqual(201, response.status_code)
        self.assertIn(b'id', response.content)
        self.assertIn(b'payload', response.content)
        # raises an error, because one item is created
        self.assertEqual(0, len(Collection.objects.all()))

    def test_get_json_and_post(self):
        url = "http://ws.pangaea.de/es/portals/pansimple/_search?pretty="
        headers = requests.structures.CaseInsensitiveDict()
        headers["Accept"] = "application/json"

        response = requests.get(url, headers=headers)
        json_data = response.json()
        print(response.status_code)

        response = self.api_client.post(
            '/api/collections/',
            {'payload': json_data},
            format='json'
        )
        self.assertEqual(201, response.status_code)
        assert (response.json())
        self.assertIn(b'id', response.content)
        self.assertIn(b'payload', response.content)

    #todo:
    #  get the id, or make it id independent
    #  test serializers ex. /api/collection/29/?format=json
        response = self.api_client.get('/api/collections/?format=json', headers=headers)
        self.assertJSONEqual(json_data, response.json(), msg=None)
        # raises an error
        self.assertJSONNotEqual(json_data, response.json(), msg=None)

    #todo: 400 bad request
