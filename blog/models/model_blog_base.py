from simple_history.models import HistoricalRecords
from django.db import models

class ModelBlogBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords(inherit=True)

    class Meta:
        ordering = ["-created_at"]
        abstract = True
        indexes = [
            models.Index(
                fields=[
                    "created_at",
                    "is_active",
                ]
            ),
        ]
