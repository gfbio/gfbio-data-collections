from gfbio_collection.collection.models import Collection
from rest_framework import serializers

class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='collection:collection-detail')
    # owner = serializers.HyperlinkedRelatedField(view_name='collection:user-detail', lookup_field='username', many=False, read_only=True)

    class Meta:
        model = Collection
        fields = ['url', 'id',
                  'collection_name', 'payload',
                  # 'owner'
                  ]

    def validate(self, payload):
        if bool(payload['payload']):
            target = []
            id_list = ['id', 'uuid', 'url']
            content = payload.get('payload')
            for id in id_list:
                target.append(content.get(id, 'NO_' + id + '_PROVIDED'))
        else:
            raise serializers.ValidationError(
                    'No payload')
        return payload
