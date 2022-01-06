from django.db import models
from django.conf import settings

class Collection(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    collection_name = models.CharField(max_length=128, blank=True)
    collection_payload = models.JSONField(default=dict, null=False)
    collection_owner = models.CharField(max_length=128, blank=True)
    # collection_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='collection')

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        """
        save a representation of the collection.
        """
        super(Collection, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % (self.created) # display the default attribute
