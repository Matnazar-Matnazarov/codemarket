from django.db import models
from accounts.models import CustomUser
from blog.models.model_comment import ModelComment
from .model_project import Project


class ModelProjectComment(ModelComment):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    likes = models.ManyToManyField(
        CustomUser, related_name="model_project_comment_likes", blank=True
    )

    class Meta:
        verbose_name = "Model Project Comment"
        verbose_name_plural = "Model Project Comments"
        db_table = "model_project_comment"

    def __str__(self):
        return f"{self.project_name}"
