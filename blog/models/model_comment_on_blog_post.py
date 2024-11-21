from django.db import models
from .model_blog_post import Post
from .model_blog_base import ModelBlogBase
from accounts.models import CustomUser


class Comment(ModelBlogBase):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments_post_model"
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        db_table = "comments"
        indexes = [
            models.Index(fields=["post"]),
        ]

    def __str__(self):
        return f"{self.comment}"

    def get_queryset(self):
        return super().get_queryset().select_related("user", "post")
