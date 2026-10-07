import uuid
from django.db import models


class TimeStampedModel(models.Model):
    """
    Abstract base model providing an immutable UUID primary key
    and auto-managed timestamp audit fields.
    Foundation for all e-commerce domain models.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']
