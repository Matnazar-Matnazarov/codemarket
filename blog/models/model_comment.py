from django.db import models
from accounts.models import CustomUser
from projects.models.model_base import ModelBase


class ModelComment(ModelBase):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["comment"]),
        ]
