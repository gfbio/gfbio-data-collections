from django.db import models
from uuid import uuid4


class Collection(models.Model):
    id = models.UUIDField(default=uuid4, auto_created=True, primary_key=True)
    set = models.JSONField()
    created = models.DateTimeField(auto_now_add=True)
    external_user_id = models.CharField(max_length=255, null=True, blank=True)
    origin = models.CharField(max_length=255)

    class Meta:
        ordering = ['created']

    def __str__(self) -> str:
        return 'collection_{}'.format(self.id)
