from rest_framework import generics, mixins, permissions
from collection_service.collection.api.serializers import CollectionSerializer
from collection_service.collection.models import Collection
from collection_service.users.models import Service
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator


def user_is_service(user):
    service = Service.objects.filter(pk=user.id).first()
    if not (service and service.origin):
        raise PermissionDenied
    return True

class GenericCollectionView(generics.GenericAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]


class CollectionDetailView(GenericCollectionView, mixins.RetrieveModelMixin):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='id',
                description='Id of the collection to retrieve.',
                required=True,
                location="path",
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
    @method_decorator(permission_required(perm='collection.view_collection', raise_exception=True))
    @method_decorator(user_passes_test(test_func=user_is_service))
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
                location="path",
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
                description="All collections that are stored for the user. For unknown external user ids, it's empty."
            )
        }
    )
    @method_decorator(permission_required(perm='collection.view_collection', raise_exception=True))
    @method_decorator(user_passes_test(test_func=user_is_service))
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
                description='Bad request'
            )
        }
    )
    @method_decorator(permission_required(perm='collection.add_collection', raise_exception=True))
    @method_decorator(user_passes_test(test_func=user_is_service))
    def post(self, request, *args, **kwargs):
        """
        Adds the given collection to the data store.
        The set is are mandatory. The origin is retrieved from the given user.
        """
        origin_service = Service.objects.get(pk=self.request.user.id)
        request.data["service"] = origin_service.id

        return self.create(request, *args, **kwargs)
