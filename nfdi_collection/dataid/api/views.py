from nfdi_collection.dataid.models import DataId
from .serializers import DataIdSerializer
from nfdi_collection.dataid.permissions import IsOwnerOrReadOnly

from rest_framework import permissions
from rest_framework import viewsets

class DataIdViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = DataId.objects.all()
    serializer_class = DataIdSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)

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

    def pre_save(self, obj):
        obj.owner = self.request.user
