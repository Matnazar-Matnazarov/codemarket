from django.db import models
from .model_comment import ModelComment
from .model_blog_post import Post


class Comment(ModelComment):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments_post_model"
    )

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        db_table = "comments"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["post"]),
        ]

    def __str__(self):
        return f"{self.name}"

    def get_queryset(self):
        return super().get_queryset().select_related("user", "post")
