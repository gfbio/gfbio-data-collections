from rest_framework import serializers
# from gfbio_collections.users.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    collection = serializers.HyperlinkedRelatedField(many=True, view_name='collections:collections-detail', read_only=True)

    class Meta:
        model = User
        fields = ["username", "name", "url", "collections"]

        extra_kwargs = {
            "url": {"view_name": "collections:user-detail", "lookup_field": "username"},
            "collections": {"view_name": "collections:collections-detail", "many":True, "read_only":True}

        }
