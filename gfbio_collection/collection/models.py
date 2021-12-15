from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Collection(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    collection_name = models.CharField(max_length=128, blank=True)
    collection_payload = models.JSONField(default=dict, null=False)
    collection_user = models.ForeignKey('users.User', null=True, blank=True, related_name='user_collection', on_delete=models.SET_NULL)
    collection_owner = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        """
        save a representation of the collection.
        """
        super(Collection, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % (self.created) # display the default attribute
