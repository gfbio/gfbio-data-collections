
import os
import json
import responses

from django.test import TestCase

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from gfbio_collection.users.models import User
from gfbio_collection.collection.models import Collection

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # project root

def _get_test_data_dir_path():
    return '{0}{1}gfbio_colelction{1}collection{1}tests{1}test_data'.format(
        os.getcwd(),
        os.sep, )
    #return 'test_data'

def _get_collection_request_data():
    with open(os.path.join(
            #_get_test_data_dir_path(),
            './test_data',
            'sample_awi.json'), 'r') as data_file:
        return json.load(data_file)


class TestCollectionView(TestCase):

    @responses.activate
    def test_valid_max_post_of_fresh_user(self):

        self.assertEqual(0, len(Collection.objects.all()))

        user = User.objects.create_user(
            username='new_user', email='new@user.de', password='pass1234', )
        #user.site_configuration = self.site_config
        user.save()

        token, created = Token.objects.get_or_create(user_id=user.id)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = client.post(
            '/api/collections/',
            _get_collection_request_data(),
            format='json'
        )

        self.assertEqual(201, response.status_code)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual('new_user', content['user'])

        response = client.post(
            '/api/collection/',
            _get_collection_request_data(),
            format='json'
        )

        self.assertEqual(2, len(Collection.objects.all()))

        response = client.get('/api/collection/')
        content = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(content))
