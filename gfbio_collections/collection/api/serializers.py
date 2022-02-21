from gfbio_collections.collection.models import Collection
from rest_framework import serializers
from gfbio_collections.utils.schema_validator import CollectionValidator

class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='collection:collection-detail')
    # collection_owner = serializers.ReadOnlyField(source='collection_owner.username')
    # collection_owner = serializers.HyperlinkedRelatedField(view_name='collection:users-detail', lookup_field='username', many=False, read_only=True)
    #collection_owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Collection
        fields = ['url',
                  'collection_name',
                  'collection_owner',
                  'collection_payload',
                  ]
        read_only_fields = ['collection_owner']

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
