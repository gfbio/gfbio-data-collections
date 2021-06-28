from nfdi_collection.dataid.models import DataId
from rest_framework import serializers

class DataIdSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    id = serializers.HyperlinkedRelatedField(many=False, view_name='api:dataid-detail', read_only=True)

    class Meta:
        model = DataId
        fields = ['id', 'owner',
                  'data_id', 'unique_id',
                  'id_of_schema', 'id_of_type',
                  'url', 'data'
                  ]
