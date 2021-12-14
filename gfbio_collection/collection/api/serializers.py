from gfbio_collection.collection.models import Collection
from rest_framework import serializers
from gfbio_collection.utils.schema_validator import CollectionValidator


class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='collection:collection-detail')
    collection_owner = serializers.ReadOnlyField(source='collection_owner.username')
    # owner = serializers.HyperlinkedRelatedField(view_name='collection:user-detail', lookup_field='username', many=False, read_only=True)

    class Meta:
        model = Collection
        fields = ['url',
                  'collection_name',
                  'collection_owner',
                  'collection_payload',
                  #'owner'
                  ]

    # item must have the attribute collection_payload, which pertains to collection_to_validate
    def validate(self, collection_to_validate):
        validator = CollectionValidator()
        if collection_to_validate:
            valid, errors = validator.validate_collection(data=collection_to_validate.get('collection_payload', {}))
        else:
            raise serializers.ValidationError('NO_DATA')
        if not valid:
            raise serializers.ValidationError(
                {'collection_to_validate': [e.message for e in errors]})

        return collection_to_validate

    # todo: validate payload
    # def validate(self, collection_payload):
    # if collection_to_validate.get('collection_payload',False):
    #     payload = collection_to_validate.get('collection_payload', {})
    #     valid, errors = validator.validate_payload(data=payload)
    # else:
    #     raise serializers.ValidationError('NO_PAYLOAD')
    # if not valid:
    #     raise serializers.ValidationError(
    #         {'collection_payload': [e.message for e in errors]})
