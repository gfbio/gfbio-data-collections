from rest_framework import serializers
from collection_service.collection.models import Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'external_user_id', 'origin', 'set', 'created']
