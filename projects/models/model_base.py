from django.db import models
from simple_history.models import HistoricalRecords


class ModelBase(models.Model):
    name = models.CharField(
        max_length=50, null=True, blank=True, unique=True, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(
        max_length=120, null=True, blank=True, unique=True, db_index=True
    )
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords(inherit=True)

    class Meta:
        ordering = ["-created_at"]
        abstract = True
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
            models.Index(
                fields=[
                    "created_at",
                    "is_active",
                    "name",
                ]
            ),
        ]

        unique_together = (("name", "slug"),)
