import os
import json
import responses
from django.test import TestCase

from gfbio_collections.collections.models import Collection
from gfbio_collections.users.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

TEST_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_data"))


def _get_collection_request_data():
    with open(os.path.join(
        TEST_DATA_DIR,
        'sample_awi.json'), 'r') as data_file:
        return json.load(data_file)


class TestCollectionView(TestCase):

    def post(self, client, test_data):
        response = client.post(
            '/api/collections/',
            test_data,
            format='json'
        )

        self.assertEqual(201, response.status_code)
        # small check for the collection name
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(test_data['collection_name'], content['collection_name'])
        # comment: the next line would work, when there is a link to a user
        # self.assertEqual('new_user', content[user.USERNAME_FIELD])
        return response

    def get(self, client):
        response = client.get('/api/collections/')

        content = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        return content

    @responses.activate
    def test_valid_max_post_of_fresh_user(self):
        self.assertEqual(0, len(Collection.objects.all()))

        user = User.objects.create_user(
            username='new_user', email='new@user.de', password='pass1234', )
        user.save()

        token, created = Token.objects.get_or_create(user_id=user.id)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        test_data = _get_collection_request_data()

        # test POST
        self.post(client, test_data)

        # test POST again
        self.post(client, test_data)

        # now we should have two elements
        self.assertEqual(2, len(Collection.objects.all()))

        # test GET
        content = self.get(client)
        # and we should be able to get two elements from the service
        self.assertEqual(2, len(content))
