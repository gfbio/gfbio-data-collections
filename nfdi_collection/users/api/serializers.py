from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    dataid = serializers.HyperlinkedRelatedField(many=True, view_name='api:dataid-detail', read_only=True)

    class Meta:
        model = User
        fields = ["username", "name", "url", "dataid"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }
