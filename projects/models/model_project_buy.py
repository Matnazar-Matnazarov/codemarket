import uuid

from django.db import models
from .model_project import Project
from blog.models.model_blog_base import ModelBlogBase
from accounts.models import CustomUser


class ModelProjectBuy(ModelBlogBase):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
    token = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, db_index=True, primary_key=True
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = "model_project_buy"
        indexes = [
            models.Index(fields=["user", "project"]),
            models.Index(fields=["token", "created_at", "updated_at"]),
            models.Index(fields=["user", "created_at", "token"]),
            models.Index(fields=["comment", "token"]),
        ]

    def __str__(self):
        return f"{self.user.email} {self.project.name}"
