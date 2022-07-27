from django.db import models
from django_extensions.db.models import TimeStampedModel
from uuid import uuid4


class Collection(TimeStampedModel):
    id = models.UUIDField(default=uuid4, auto_created=True, primary_key=True, editable=False)
    set = models.JSONField()
    external_user_id = models.CharField(max_length=255, null=True, blank=True)
    origin = models.CharField(max_length=255)

    class Meta:
        ordering = ['created']

    def __str__(self) -> str:
        return 'collection_{}'.format(self.id)
