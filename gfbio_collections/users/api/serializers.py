from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "collections:user-detail", "lookup_field": "username"},
            "collections": {"view_name": "collections:collections-detail", "many":True, "read_only":True}
        }
