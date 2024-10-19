import uuid

from django.db import models
from .model_project import Project
from .model_comment import ModelComment


class ModelProjectBuy(ModelComment):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        db_table = "model_project_buy"
        indexes = [
            models.Index(fields=["user", "project"]),
            models.Index(fields=["token", "created_at", "updated_at"]),
            models.Index(fields=["user", "created_at", "token"]),
            models.Index(fields=["comment", "name", "token"]),
        ]

    def __str__(self):
        return f"{self.user.email} {self.project.name}"
