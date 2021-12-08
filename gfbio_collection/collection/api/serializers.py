from gfbio_collection.collection.models import Collection
from rest_framework import serializers
from gfbio_collection.utils.schema_validator import CollectionValidator

class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='collection:collection-detail')
    # owner = serializers.HyperlinkedRelatedField(view_name='collection:user-detail', lookup_field='username', many=False, read_only=True)

    class Meta:
        model = Collection
        fields = ['url',
                  'collection_name',
                  'collection_identifier',
                  'collection_payload',
                  # 'owner'
                  ]

    # item must have the attribute collection_payload, which pertains to collection_data
    def validate(self, collection_data):
        validator = CollectionValidator()
        if collection_data.get('collection_payload',False):
            payload = collection_data.get('collection_payload', {})
            valid, errors = validator.validate_data(data=payload)
        else:
            raise serializers.ValidationError('NO_PAYLOAD')

