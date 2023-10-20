from django.db import models
from django.utils import timezone


class BaseModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_archived=False)


class ArchivedModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_archived=True)


class AllModelManager(models.Manager):
    pass


class BaseModel(models.Model):
    """
    Base model that supports archiving and created/updated timestamps
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Set archived_at when is_archived is set to True
        """
        if self.is_archived and not self.archived_at:
            self.archived_at = timezone.now()
        super().save()
