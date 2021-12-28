from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet, ModelViewSet

from gfbio_collections.users.api.serializers import UserSerializer
from gfbio_collections.users.models import User

# User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        if self.action == 'list':
            return User.objects.all()
        else:
            assert isinstance(self.request.user.id, int)
            return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

# class UserList(ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
# class UserDetail(RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     lookup_field = "username"

# users_list_view = UserList.as_view()
# users_detail_view = UserDetail.as_view()

users_list_view = UserViewSet.as_view({
    'get': 'list'
})
users_detail_view = UserViewSet.as_view({
    'get': 'retrieve'
})

#fixme: how to retrieve the current user?
# how to correctly associate views with the app_name? (e.g. collections in urls.py)
# how are these related to the association in api_router? (e.g. app_name = "api")

users_me_view = UserViewSet.as_view({'get': 'retrieve'}
                                    # ,**{'name' : 'collection_owner'}
                                    )
