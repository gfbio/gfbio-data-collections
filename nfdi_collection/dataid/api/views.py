from nfdi_collection.dataid.models import DataId
from .serializers import DataIdSerializer
from nfdi_collection.dataid.permissions import IsOwnerOrReadOnly

from rest_framework import permissions

from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework import viewsets


class RootView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        return Response(
            {
             'users': reverse('dataid:user-list', request=request, format=format),
             'dataid': reverse('dataid:dataid-list', request=request, format=format)
             }
        )

root_view = RootView.as_view()

class DataIdList(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = DataId.objects.all()
    serializer_class = DataIdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

dataid_view = DataIdList.as_view()

class DataIdDetail(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = DataId.objects.all()
    serializer_class = DataIdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

dataid_detail_view = DataIdDetail.as_view()

# rewriting as viewset

class DataIdViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = DataId.objects.all()
    serializer_class = DataIdSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    #
    # def pre_save(self, obj):
    #     obj.owner = self.request.user
