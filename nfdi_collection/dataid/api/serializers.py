from nfdi_collection.dataid.models import DataId
from rest_framework import serializers

class DataIdSerializer(serializers.HyperlinkedModelSerializer):
    reporter = serializers.ReadOnlyField(source='reporter.username')
    #id = serializers.HyperlinkedRelatedField(many=False, view_name='api:dataid-detail', read_only=True)
    url = serializers.HyperlinkedIdentityField(many=False, view_name='dataid:dataid-detail', read_only=True)

    class Meta:
        model = DataId
        fields = ['url', 'id', 'reporter',
                  'id_of_data', 'id_unique_of_data',
                  'id_of_schema', 'id_of_type',
                  'url_of_data', 'data'
                  ]
