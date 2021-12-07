from gfbio_collection.collection.models import Collection
from rest_framework import serializers

class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='collection:collection-detail')
    # owner = serializers.HyperlinkedRelatedField(view_name='collection:user-detail', lookup_field='username', many=False, read_only=True)

    class Meta:
        model = Collection
        fields = ['url', 'id'
                  'collection_name',
                  'collection_identifier',
                  'payload',
                  # 'owner'
                  ]

    # item must have the attribute payload, which includes a payload
    def validate(self, payload):
        return bool(payload['payload'])
        # if bool(payload['payload']):
        #     id_provided = []
        #     id_list = ['id', 'uuid', 'url', 'dataid']
        #     content = payload.get('payload')
        #     for id in id_list:
        #         id_provided.append(content.get(id, 'NO_' + id + '_PROVIDED'))
        # else:
        #     raise serializers.ValidationError(
        #             'No payload')
        # return payload
