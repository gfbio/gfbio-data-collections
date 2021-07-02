from nfdi_collection.dataid.models import DataId
from rest_framework import serializers

class DataIdSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='dataid:dataid-detail')
    reporter = serializers.HyperlinkedRelatedField(view_name='dataid:user-detail', lookup_field='username', many=False, read_only=True)

    class Meta:
        model = DataId
        fields = ['url', 'id', 'reporter',
                  'id_of_data', 'id_unique_of_data',
                  'id_of_schema', 'id_of_type',
                  'url_of_data', 'data'
                  ]
