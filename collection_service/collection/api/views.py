from rest_framework import viewsets
from rest_framework.response import Response
from collection_service.collection.api.serializers import CollectionSerializer
from collection_service.collection.models import Collection


class CollectionAPIView(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def retrieve(self, request, *args, **kwargs):
        """Returns the collection with the given id."""
        return super().retrieve(request, *args, **kwargs)

    def get_collections_for_user(self, request, external_user_id):
        """
        Returns a list of all collections for the given user/user-id.
        If the user-id is not assigned to any user or there are no collections for this user, the result is empty.
        """
        collections_of_the_user = self.get_queryset().filter(
            external_user_id=external_user_id
        ).values('id', 'created', 'origin', 'set')
        return Response(collections_of_the_user)
