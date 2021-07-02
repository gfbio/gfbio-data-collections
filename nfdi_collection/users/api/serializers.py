from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    # url = serializers.HyperlinkedIdentityField(many=False, view_name='dataid:user-detail', "lookup_field": "username", read_only=True)
    # dataid = serializers.HyperlinkedRelatedField(many=True, view_name='dataid:dataid-detail', read_only=True)

    class Meta:
        model = User
        fields = ["username", "name", "url", "dataid"]

        extra_kwargs = {
            "url": {"view_name": "dataid:user-detail", "lookup_field": "username"},
            "dataid": {"view_name": "dataid:dataid-detail", "many":True, "read_only":True}

        }
