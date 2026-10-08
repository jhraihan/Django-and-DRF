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


class ActiveQuerySet(models.QuerySet):
    """Custom queryset providing helper filters for active entities."""
    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)


class ActiveManager(models.Manager):
    """Custom manager exposing active filter helpers on model classes."""
    def get_queryset(self):
        return ActiveQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def inactive(self):
        return self.get_queryset().inactive()


class ActivatableModel(models.Model):
    """
    Abstract model adding an active status flag with an active-aware manager.
    Useful for enabling/disabling products, categories, or accounts.
    """
    is_active = models.BooleanField(default=True, db_index=True)

    objects = ActiveManager()

    class Meta:
        abstract = True


class SluggedModel(models.Model):
    """
    Abstract model adding a unique slug and auto-generating it from 'name'
    if left blank.
    """
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        abstract = True

    def get_slug_source(self):
        return getattr(self, 'name', '') or str(self)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.get_slug_source())
        super().save(*args, **kwargs)


class BaseModel(TimeStampedModel, ActivatableModel):
    """
    Composite base model combining UUID primary key, timestamps,
    and activation state. Foundation for core domain entities.
    """
    class Meta:
        abstract = True
        ordering = ['-created_at']

