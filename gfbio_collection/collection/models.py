from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Collection(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    collection_identifier = models.CharField(max_length=128, blank=True)
    collection_name = models.CharField(max_length=128, blank=True)
    payload = models.JSONField(default=dict)
    # owner = models.ForeignKey(User, related_name='collection', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        """
        save a representation of the collection.
        """
        super(Collection, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % (self.collection_identifier) # display the default attribute
