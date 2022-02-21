from django.contrib.auth import get_user_model
from rest_framework import serializers
from gfbio_collections.collection.models import Collection
User = get_user_model()

#class UserSerializer(serializers.HyperlinkedModelSerializer):
class UserSerializer(serializers.ModelSerializer):
    # me = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # collections = serializers.HyperlinkedRelatedField(many=True, view_name='collection-detail', read_only=True)
    #collections = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # collections = serializers.PrimaryKeyRelatedField(many=True, read_only=True) #todo: queryset=Collection.objects.filter(pk=User.id))
    # url = serializers.HyperlinkedIdentityField(view_name='collection:collection-list')

    class Meta:
        model = User
        fields = ["username", "name", "url"] #, "collections"]

        extra_kwargs = {
            "url": {"view_name": "collection:collection-list", "lookup_field": "username"},
            # "collection": {"view_name": "collection:collection-detail", "many":True, "read_only":True}
        }
