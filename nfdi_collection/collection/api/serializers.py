from nfdi_collection.collection.models import Collection
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
