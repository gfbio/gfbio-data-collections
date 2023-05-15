import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import Permission
from django.test import TestCase
from collection_service.collection.api.serializers import CollectionSerializer
from collection_service.users.models import Service

pytestmark = pytest.mark.django_db


class TestCollectionView(TestCase):

    other_token = None
    delete_token = None
    deleteOfOthers_token = None
    generated_collections = []

    @classmethod
    def setUpTestData(self):
        client = APIClient()
        self.api_client = client

        other_permission_service = Service.objects.create(origin="gfbio:collections:other", username="other")
        self.other_token = "Token " + Token.objects.create(user=other_permission_service).key

        delete_permission_service = Service.objects.create(origin="gfbio:collections:delete", username="delete")
        delete_permission_service.user_permissions.add(Permission.objects.get(codename="delete_collection"))
        self.delete_token = "Token " + Token.objects.create(user=delete_permission_service).key

        deleteOfOther_permission_service = Service.objects.create(
            origin="gfbio:collections:deleteOfOther",
            username="deleteOfOthers"
        )
        deleteOfOther_permission_service.user_permissions.add(Permission.objects.get(codename="delete_collection"))
        deleteOfOther_permission_service.user_permissions.add(
            Permission.objects.get(codename="change_collection_of_other_service")
        )
        self.deleteOfOthers_token = "Token " + Token.objects.create(user=deleteOfOther_permission_service).key

        collection_test_data = [
            # Two test-collections for user 17
            {
                "set": [
                    "00c0ffee",
                    "447-abc"
                ],
                "service": other_permission_service,
                "external_user_id": "17"
            },
            {
                "set": [
                    "Code red"
                ],
                "service": other_permission_service,
                "external_user_id": "17"
            },
            # One test-collection for different user
            {
                "set": [
                    "Test3",
                ],
                "service": other_permission_service,
                "external_user_id": "5"
            },
            # Collection with anonymous user
            {
                "set": [
                    "ano-1",
                    "ano-2"
                ],
                "service": other_permission_service
            },
            # Collection of service with delete rights
            {
                "set": [
                    "Test5",
                ],
                "service": delete_permission_service
            }
        ]

        for entry in collection_test_data:
            serializer = CollectionSerializer(
                data=entry
            )
            if serializer.is_valid():
                self.generated_collections.append(serializer.save())

    def test_delete_collection_of_others_with_permission(self):
        test_id = str(self.generated_collections[0].id)
        response = self.api_client.delete(
            f'/api/collections/{test_id}/',
            HTTP_AUTHORIZATION=self.deleteOfOthers_token
        )

        self.assertEqual(204, response.status_code)

    def test_delete_collection_of_others_missing_permission(self):
        test_id = str(self.generated_collections[0].id)
        response = self.api_client.delete(
            f'/api/collections/{test_id}/',
            HTTP_AUTHORIZATION=self.delete_token
        )

        self.assertEqual(403, response.status_code)

    def test_delete_own_collection_with_permission(self):
        test_id = str(self.generated_collections[4].id)
        response = self.api_client.delete(
            f'/api/collections/{test_id}/',
            HTTP_AUTHORIZATION=self.delete_token
        )

        self.assertEqual(204, response.status_code)

    def test_delete_own_collection_missing_permission(self):
        test_id = str(self.generated_collections[1].id)
        response = self.api_client.delete(
            f'/api/collections/{test_id}/',
            HTTP_AUTHORIZATION=self.other_token
        )

        self.assertEqual(403, response.status_code)

    def test_delete_collection_missing_auth(self):
        test_id = str(self.generated_collections[1].id)
        response = self.api_client.delete(f'/api/collections/{test_id}/')

        self.assertEqual(403, response.status_code)

    def test_delete_missing_collection_fails(self):
        test_id = str("Non-Exsiting")
        response = self.api_client.delete(
            f'/api/collections/{test_id}/',
            HTTP_AUTHORIZATION=self.deleteOfOthers_token
        )

        self.assertEqual(404, response.status_code)
