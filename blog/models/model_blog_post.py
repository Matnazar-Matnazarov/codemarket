from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount
from .model_comment import ModelComment
from .manager_post import PostManager


class Post(ModelComment):
    body = models.TextField(max_length=500, null=True, blank=True)
    hit_count_generic = GenericRelation(
        HitCount,
        object_id_field="object_pk",
        related_query_name="hit_count_generic_relation",
    )
    objects = PostManager()

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        db_table = "blog_post"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["body"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.name
