from rest_framework import generics, mixins
from collection_service.collection.api.serializers import CollectionSerializer
from collection_service.collection.models import Collection


class GenericCollectionView(generics.GenericAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class CollectionDetailView(mixins.RetrieveModelMixin, GenericCollectionView):
    def get(self, request, *args, **kwargs):
        """Returns the collection with the given id."""
        return self.retrieve(request, *args, **kwargs)


class UserCollectionListView(mixins.ListModelMixin, GenericCollectionView):
    def get(self, request, *args, **kwargs):
        """
        Returns a list of all collections for the given user/user-id.
        If the user-id is not assigned to any user or there are no collections for this user, the result is empty.
        """
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        external_user_id_from_path=self.kwargs.get('external_user_id')
        return super().get_queryset().filter(
            external_user_id=external_user_id_from_path
        )
