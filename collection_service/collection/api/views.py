from celery import uuid
from rest_framework import generics, mixins
from collection_service.collection.api.serializers import CollectionSerializer
from collection_service.collection.models import Collection
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse


class GenericCollectionView(generics.GenericAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = []


class CollectionDetailView(mixins.RetrieveModelMixin, GenericCollectionView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='id', 
                description='Id of the collection to retrieve.', 
                required=True, 
                location = "path",
                examples=[
                    OpenApiExample(
                        'Sample id',
                        value="00c0ffee-c0ff-c0ff-c0ff-c0ffeec0ffee"
                    )
                ],
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=CollectionSerializer(many=False),
                description='The collection with the given id.'
            ),
            404: OpenApiResponse(
                description='Not found.'
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """Returns the collection with the given id."""
        return self.retrieve(request, *args, **kwargs)


class UserCollectionListView(mixins.ListModelMixin, GenericCollectionView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='external_user_id', 
                description='Exteral id of the user whos data are requested', 
                required=True, 
                location = "path",
                examples=[
                    OpenApiExample(
                        'Sample id',
                        description='The id is a freely choosable string.',
                        value="XY-4999233348"
                    )
                ],
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=CollectionSerializer(many=True),
                description='All collections that are stored for the user. If the external user id is unknown, the resulting set is empty.'
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Returns a list of all collections for the given user/external_user-id.
        If the user-id is not assigned to any user or there are no collections for this user, the result is empty.
        """
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        external_user_id_from_path = self.kwargs.get('external_user_id')
        return super().get_queryset().filter(
            external_user_id=external_user_id_from_path
        )


class CollectionListView(mixins.CreateModelMixin, GenericCollectionView):
    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=CollectionSerializer(many=False),
                description='The newly generated object, with its generated fields id and created set.',
            ),
            400: OpenApiResponse(
                description='Bad request',
                examples=[
                    OpenApiExample('Set is missing',
                        value={
                            "set": [
                                "This field may not be null."
                            ]
                        }
                    ),
                    OpenApiExample('Origin is missing',
                        value={
                            "origin": [
                                "This field is required."
                            ]
                        }
                    )
                ]
            )
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Adds the given collection to the data store.
        Set and origin are mandatory.
        """
        return self.create(request, *args, **kwargs)
