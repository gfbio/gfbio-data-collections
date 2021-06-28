import uuid
from django.db import models
from nfdi_collection.users.models import User

class DataId(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    data_id = models.CharField(max_length=100, blank=True, default='')
    unique_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=True)
    id_of_schema = models.CharField(max_length=100, blank=True, default='')
    id_of_type = models.CharField(max_length=100, blank=True, default='')
    url = models.URLField(blank=True,null=True)
    data = models.JSONField(blank=True,null=True)
    owner = models.ForeignKey(User, related_name='dataid', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        """
        save a representation of the dataid.
        """
        super(DataId, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % (self.data_id)
