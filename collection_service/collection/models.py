from django.db import models
from model_utils.models import TimeStampedModel
from uuid import uuid4
from collection_service.users.models import Service


class Collection(TimeStampedModel):
    id = models.UUIDField(default=uuid4, auto_created=True, primary_key=True, editable=False)
    set = models.JSONField()
    external_user_id = models.CharField(max_length=255, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)

    class Meta:
        ordering = ['created']

    def __str__(self) -> str:
        return 'collection_{}'.format(self.id)
