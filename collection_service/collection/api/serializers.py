from rest_framework import serializers
from collection_service.collection.models import Collection
from collection_service.collection.utils.schema_validation import validate_json_not_trivial, validate_origin_format


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'external_user_id', 'origin', 'set', 'created']

    def validate(self, attrs):
        validate_origin_format(attrs['origin'])
        validate_json_not_trivial(attrs['set'])
        return super().validate(attrs)
