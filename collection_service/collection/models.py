from django.db import models
from uuid import uuid4

class Collection(models.Model):
    id = models.UUIDField(default=uuid4, auto_created=True, primary_key=True)
    set = models.JSONField()
    created = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['created']

    def __str__(self) -> str:
        return str(id)