import os
import json
import base64
import responses
import requests

from django.test import TestCase

from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APIClient

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
    def setUpTestData(cls):
        # fresh user
        user = User.objects.create_user(
            username="new_user", email="new@user.de", password="pass1234", )
        user.save()

        client = APIClient()

        cls.api_client = client

    @classmethod
    def setUpTestData(cls, username="new_user", email="new@user.de", password="Pass12345#", is_user=True, is_site=False):
        # fresh user
        user = User.objects.create_user(
            username=username, email=email, password=password, )
        user.is_user = is_user
        user.is_site = is_site
        user.save()

        client = APIClient()
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
    def test_get(self):
        """
        collections must be used in plural
        """
        response = self.client.get("/api/collectionss/")
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
        it does not make a difference if credentials are given
        """
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

        #fixme; patch
        # moved permanently?!
        response = self.api_client.get("/api/collections/" + str(Collection.objects.last().id))
        self.assertNotEqual(301, response.status_code)

        # response = self.api_client.put(
        #     "/api/collections/" + str(Collection.objects.last().id),
        #     {"collection_payload": collection_payload},
        #     format="json",
        # )
        # self.assertEqual(403, response.status_code)

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
        Alternatively use setUpTestData for testing with credentials
        In addition POST, i.e. json validation also requires api_client
        """
        headers = requests.structures.CaseInsensitiveDict()
        headers["Accept"] = "application/json"

        # # # get data remotely
        # url = "http://ws.pangaea.de/es/portals/pansimple/_search?pretty="
        # response = requests.get(url, headers=headers)
        # json_data = response.json()

        # get data locally
        with open(os.path.join(
            "./test_data",
            "_search.json"), "r") as data_file:
            json_data = json.load(data_file)

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
        self.assertEqual(json_data_get, json_data)

    # get anonymous user
    def test_collection_owner(self):
        #self.assertEqual(0, len(Collection.objects.all()))
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
        self.api_client.login(username='new_user', password='Pass12345#')
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
        super().setUpTestData(username="new_user_2")

        user = User.objects.get(username='new_user_2')
        self.api_client.force_authenticate(user=user)
        response = self.api_client.post(
            "/api/collections/",
            {"collection_payload": collection_payload},
            format="json",
        )
        self.assertEqual(201, response.status_code)
        self.api_client.force_authenticate(user=None)

        # fixme: not posting with credentials but as anonymous
        super().setUpTestData(username="new_user_3")

        # set credentials
        self.api_client.credentials(
            HTTP_AUTHORIZATION="Basic " + base64.b64encode(
                b"new_user_3:Pass12345#").decode("utf-8")
        )
        credentials = base64.b64encode(b"new_user_3:Pass12345#").decode("utf-8")
        self.api_client.credentials(HTTP_AUTHORIZATION='Basic ' + credentials)

        response = self.api_client.post(
            "/api/collections/",
            {"collection_payload": collection_payload},
            format="json",
        )
        self.assertEqual(201, response.status_code)
        self.api_client.credentials()

        # for testing
        Collection.objects.all()
        Collection.objects.all().values_list("collection_owner")

        #todo: sessionauthentication

        #todo: tokenauthentication
        # token = Token.objects.get(user__username='new_user_2')
        # self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


        # self.assertTrue(Collection.objects.filter(collection_owner="new_user").exists())
