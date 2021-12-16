from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    collections = serializers.HyperlinkedRelatedField(many=True, view_name='collection:collection-detail', read_only=True)

    class Meta:
        model = User
        fields = ["username", "name", "url", "collections"]

        extra_kwargs = {
            "url": {"view_name": "collection:user-detail", "lookup_field": "username"},
            "collection": {"view_name": "collection:collection-detail", "many":True, "read_only":True}
        }
