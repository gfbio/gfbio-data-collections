import os
import json
import base64
import responses
import requests
import pytest

from django.test import TestCase

from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status
from django.urls import reverse

from gfbio_collections.users.models import User
from gfbio_collections.collection.models import Collection

from django.core.management.commands.test import Command as BaseCommand


# wrap django"s built-in test command to always delete the database if it exists [ref](# https://adamj.eu/tech/2020/01/13/make-django-tests-always-rebuild-db/)
class Command(BaseCommand):
    def handle(self, *test_labels, **options):
        options["interactive"] = False
        return super().handle(*test_labels, **options)


class TestCollectionViewBase(TestCase):
    """
    TestCollectionViewBase instantiate a user and credentials into api_client
    """

    @classmethod
    def setUpTestData(cls, username="new_user", email="new@user.de", password="pass123"):

        client = APIClient()

        try:
            user = User.objects.get(username=username)
        except:
            user = User.objects.create_user(
                username=username, email=email, password=password)

        # fixme: find better way to store test user data
        #  should user data be within APIClient, cuttenrly automatic passord is generated
        # cls.data = {
        #     'username': user.username,
        #     'email': user.email,
        #     'password': user.password
        # }

        # # fixme: how to use token access and refresh?
        # # def api_client as in [https://newbedev.com/django-rest-framework-jwt-unit-test
        # refresh = RefreshToken.for_user(user)
        # client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        user.save()

        cls.api_client = client


class TestCollectionViewGetRequests(TestCollectionViewBase):
    """
    Set of testing functions written for development
    """

    maxDiff = None

    # 200 successful HTTP request
    def test_get(self):
        """
        The simple self.client is used for tests without credentials
        """
        response = self.client.get("/api/collections/")
        self.assertEqual(200, response.status_code)

    # 404 not found
    def test_get_fails(self):
        """
        collections must be used in plural
        """
        response = self.client.get("/api/collection/")
        self.assertEqual(404, response.status_code)

    def test_get_json(self):
        """
        assert valid deserialization, as with with "assert(response.json())",
        where no text or bad format leads to deserialization failure
        """
        response = self.client.get("/api/collections/")
        self.assertEqual(response.json(), list())

    # not 401 unauthorized
    def test_get_with_wrong_credentials(self):
        """
        test authentication credentials
        """
        # fixme: Currently it does not make a difference if credentials are given
        self.api_client.credentials(
            HTTP_AUTHORIZATION="Basic " + base64.b64encode(
                b"user:invalidpassword").decode("utf-8")
        )
        response = self.api_client.get("/api/collections/")
        self.assertNotEqual(401, response.status_code)

        # post
        collection_payload = {"hits": {"hits": [{"_id": "1234567", "_source": {"parameter": ["Time", "Location"]}}]}}
        response = self.api_client.post(
            "/api/collections/",
            {"collection_payload": collection_payload},
            format="json",
        )

        self.assertEqual(201, response.status_code)

        # patch
        query_string = "/api/collections/" + str(Collection.objects.last().id) + "/"
        response = self.api_client.get(query_string)
        self.assertNotEqual(301, response.status_code)
        self.assertNotEqual(404, response.status_code)

        response = self.api_client.put(query_string,
                                       {"collection_payload": collection_payload},
                                       format="json",
                                       )
        self.assertEqual(403, response.status_code)

        # not 401 unauthorized

    def test_get_with_wrong_credentials(self):
        """
        it does not make a difference if credentials are given
        """
        # credentials
        self.api_client.credentials(
            HTTP_AUTHORIZATION="Basic " + base64.b64encode(
                b"new_user:pass123").decode("utf-8")
        )
        response = self.api_client.get("/api/collections/")
        self.assertNotEqual(401, response.status_code)

        # post
        collection_payload = {"hits": {"hits": [{"_id": "1234567", "_source": {"parameter": ["Time", "Location"]}}]}}
        response = self.api_client.post(
            "/api/collections/",
            {"collection_payload": collection_payload},
            format="json",
        )

        self.assertEqual(201, response.status_code)

        # patch
        query_string = "/api/collections/" + str(Collection.objects.last().id) + "/"
        response = self.api_client.get(query_string)
        self.assertNotEqual(301, response.status_code)
        self.assertNotEqual(404, response.status_code)

        response = self.api_client.put(query_string,
                                       {"collection_payload": collection_payload},
                                       format="json",
                                       )

        # fixme: currently following response raises no post permission.
        #  How to use credentials correctly?
        #  Current implementation works via login, but not with credentials function!
        self.assertEqual(403, response.status_code)

    # 201 created
    def test_simple_post(self):
        """
        it does not make a difference if credentials are given
        """
        # self.assertEqual(0, len(Collection.objects.all()))

        # simple data
        # collection_payload = {"hits": {"hits": [
        #     {"_id": "1234567", "_source": {"parameter": ["Time", "Location"]}},
        #     {} # empty source
        #     ]}}

        # simple data
        collection_payload = {}
        collection_payload["hits"] = {"hits": []}
        collection_payload["hits"]["hits"].append({"_id": "1234567", "_source": {"data": [3, 2, 1]}})
        collection_payload["hits"]["hits"].append({})

        response = self.api_client.post(
            "/api/collections/",
            {"collection_payload": collection_payload},
            format="json",
        )

        self.assertEqual(201, response.status_code)
        self.assertIn(b"id", response.content)
        self.assertIn(b"collection_payload", response.content)
        # self.assertEqual(1, len(Collection.objects.all()))
        self.assertEqual(2, len(Collection.objects.last().collection_payload["hits"]["hits"]))

    # test data case with local data request
    def test_get_json_and_post(self):
        """
        the method POST, i.e. json validation also requires api_client
        """
        headers = requests.structures.CaseInsensitiveDict()
        headers["Accept"] = "application/json"

        # # # get data remotely
        url = "http://ws.pangaea.de/es/portals/pansimple/_search?pretty="
        response = requests.get(url, headers=headers)
        json_data = response.json()

        # # get data locally
        # with open(os.path.join(
        #     "./test_data",
        #     "_search.json"), "r") as data_file:
        #     json_data = json.load(data_file)

        # post to collections
        response = self.api_client.post(
            "/api/collections/",
            {"collection_payload": json_data},
            format="json"
        )
        self.assertEqual(201, response.status_code)

        # compare entry json used in post with the retrieved one from collection (nothing changed)
        response = self.api_client.get("/api/collections/", headers=headers)
        self.assertEqual(200, response.status_code)
        json_data_get = response.json()[0]["collection_payload"]
        # does not work for remote json, because of numerical rounding at coordinates
        # self.assertEqual(json_data_get, json_data)

    # get anonymous user
    def test_collection_owner(self):
        # self.assertEqual(0, len(Collection.objects.all()))
        collection_payload = {"hits": {"hits": [{"_id": "1234567", "_source": {"parameter": ["Time", "Location"]}}]}}

        response = self.api_client.post(
            "/api/collections/",
            {"collection_payload": collection_payload},
            format="json",
        )

        self.assertEqual(201, response.status_code)
        # check for AnonymousUser
        self.assertTrue(Collection.objects.all().values_list("collection_owner").exists())
        self.assertTrue(Collection.objects.filter(collection_owner="AnonymousUser").exists())

    # get anonymous user
    def test_post_get_multiple_users(self):
        # anonymous
        self.test_simple_post()

        # login existing user
        self.api_client.login(username='new_user', password='pass123')
        collection_payload = {"hits": {"hits": [{"_id": "1234567", "_source": {"parameter": ["Time", "Location"]}}]}}
        response = self.api_client.post(
            "/api/collections/",
            {"collection_payload": collection_payload},
            format="json",
        )
        self.assertEqual(201, response.status_code)
        self.api_client.logout()
        self.assertTrue(Collection.objects.filter(collection_owner="new_user").exists())

        # create new user and force authenticate
        self.setUpTestData(username="new_user_2")

        user = User.objects.get(username='new_user_2')
        self.api_client.force_authenticate(user=user)
        response = self.api_client.post(
            "/api/collections/",
            {"collection_payload": collection_payload},
            format="json",
        )
        self.assertEqual(201, response.status_code)
        self.api_client.force_authenticate(user=None)

        # for testing
        # Collection.objects.all()
        # Collection.objects.all().values_list("collection_owner")
        self.assertTrue(Collection.objects.filter(collection_owner="new_user").exists())
        self.assertTrue(Collection.objects.filter(collection_owner="new_user_2").exists())

    # test jwt
    def test_jwt_token_authentication(self):
        '''
        tests token authentication using Simple JWT
        https://github.com/jazzband/djangorestframework-simplejwt
        '''

        # creates user
        test_user = User.objects.create_user(username='user@foo.com', password='pass')
        self.assertEqual(test_user.is_active, 1, 'Active User')

        # obtain token for active user, needs explicit credentials
        url = reverse('jwt_obtain_token')
        test_user.is_active = False
        test_user.save()
        response = self.client.post(url, {'username': 'user@foo.com', 'password': 'pass'},
                                    format='json')
        self.assertEqual(401, response.status_code)
        test_user.is_active = True
        test_user.save()
        response = self.client.post(url, {'username': 'user@foo.com', 'password': 'pass'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get token
        self.assertTrue('access' in response.data)
        jwt_token = response.data['access']

        # verify token
        verification_url = reverse('jwt_token_verify')
        response = self.api_client.post(verification_url, {'token': jwt_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.api_client.post(verification_url, {'token': 'abc'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # access to a private view (e.g. users list)
        url = reverse('api:users-list')
        self.api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'abc')
        response = self.api_client.get(url, data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        response = self.api_client.get(url, data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.api_client.force_authenticate(user=None)

        # # todo: implement access to current user
        # self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token_access))
        # response = self.client.get(reverse('user-me'), data={'format': 'json'})
        # self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
