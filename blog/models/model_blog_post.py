from django.db import models
from .manager_post import PostManager
from django.core.validators import validate_image_file_extension
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import uuid
from .model_blog_base import ModelBlogBase
from accounts.models import CustomUser
from hitcount.models import HitCount
from django_ckeditor_5.fields import CKEditor5Field

class Tags(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=300, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Post(ModelBlogBase):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    body = CKEditor5Field(max_length=1000, null=True, blank=True)
    hit_count_generic = GenericRelation(
        HitCount,
        object_id_field="object_pk",
        related_query_name="hit_count_generic_relation",
    )
    image = models.ImageField(
        upload_to="blog/",
        null=True,
        blank=True,
        validators=[validate_image_file_extension],
    )
    objects = PostManager()
    tags = GenericRelation(Tags)
    icon_name = models.CharField(
        max_length=100, null=True, blank=True, default="Python"
    )
    hit_count_generic = GenericRelation(
        HitCount,
        object_id_field="object_pk",
        related_query_name="hit_count_generic_relation",
    )

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        db_table = "blog_post"
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["body"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
