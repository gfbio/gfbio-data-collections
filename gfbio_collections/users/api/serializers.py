from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

# class UserSerializer(serializers.HyperlinkedModelSerializer):
class UserSerializer(serializers.ModelSerializer):
    # me = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
            # "collection": {"view_name": "collection:collection-detail", "many":True, "read_only":True}
        }
