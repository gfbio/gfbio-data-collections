from gfbio_collections.collections.models import Collection
from rest_framework import serializers


class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='collections:collections-detail')

    # owner = serializers.HyperlinkedRelatedField(view_name='collections:user-detail', lookup_field='username',
    # many=False, read_only=True)

    class Meta:
        model = Collection
        fields = ['url', 'id',
                  'collection_name', 'payload',
                  # 'owner'
                  ]
