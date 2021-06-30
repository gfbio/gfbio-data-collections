from nfdi_collection.dataid.models import DataId
from .serializers import DataIdSerializer
from nfdi_collection.dataid.permissions import IsReporterOrReadOnly

from rest_framework import permissions

from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse


class RootView(APIView):
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
                          IsReporterOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

dataid_detail_view = DataIdDetail.as_view()
