from gfbio_collections.collection.models import Collection
from gfbio_collections.collection.api.serializers import CollectionSerializer
from gfbio_collections.collection.permissions import IsOwnerOrReadOnly

from rest_framework import permissions

from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse


class RootView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        return Response(
            {
             'users': reverse('collection:user-list', request=request, format=format),
             'collection': reverse('collection:collection-list', request=request, format=format)
             }
        )

root_view = RootView.as_view()

class CollectionList(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer, **kwargs):
        kwargs['collection_owner'] = self.request.user
        collection = serializer.save(**kwargs)
        # print(repr(serializer))
        pass

collection_view = CollectionList.as_view()

class CollectionDetail(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly
                          ]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

collection_detail_view = CollectionDetail.as_view()
