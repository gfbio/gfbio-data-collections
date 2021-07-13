from django.db import models
# from nfdi_collection.users.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class Collection(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    collection_name = models.CharField(max_length=100, blank=True, default='')
    payload = models.JSONField(blank=True, null=True)
    owner = models.ForeignKey(User, related_name='collection', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        """
        save a representation of the collection.
        """
        super(Collection, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % (self.collection_name) # display the default attribute
