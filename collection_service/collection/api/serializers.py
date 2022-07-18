import re
from rest_framework import serializers
from collection_service.collection.models import Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'external_user_id', 'origin', 'set', 'created']

    def validate(self, attrs):
        if(not re.match(r"^[\w\d\_]+(\.[\w\d\_]+)*$", attrs['origin'])):
            raise serializers.ValidationError("The origin needs to consist of namespaces separated by dots.")
        if(not isinstance(attrs["set"], (dict, list))):
            type_name = type(attrs["set"]).__name__
            error_message = "The set is '{}', but it needs to be given as list or dictionary.".format(type_name)
            raise serializers.ValidationError(error_message)
        if(len(attrs["set"]) < 1):
            raise serializers.ValidationError("The given set is empty.")
        return super().validate(attrs)
