from django.contrib.auth import get_user_model
from rest_framework import serializers
from gfbio_collection.collection.models import Collection

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    #collections_list = serializers.PrimaryKeyRelatedField(many=True, queryset=Collection.objects.all())

    class Meta:
        model = User
        fields = ["username", "name", "url"] #, "collections_list"

        extra_kwargs = {
            "url": {"view_name": "collection:user-detail", "lookup_field": "username"},
            "collection": {"view_name": "collection:collection-detail", "many":True, "read_only":True}
        }
