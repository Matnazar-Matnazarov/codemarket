from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from .model_language import ProjectLanguage
from .model_project_image import ProjectImage
from .model_database import ProjectBase
from accounts.models import CustomUser
from .model_base import ModelBase
from hitcount.models import HitCount
from django.contrib.contenttypes.fields import GenericRelation
from .model_stars import Stars
import uuid


class Project(ModelBase):
    title = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    about = models.TextField(null=True, blank=True)
    price = models.FloatField(
        null=True,
        blank=True,
    )
    url = models.URLField(
        null=True,
        blank=True,
        unique=True,
    )
    technology = models.ManyToManyField(
        ProjectLanguage, blank=True, related_name="project_many_to_many_technology"
    )
    database = models.ManyToManyField(
        ProjectBase, blank=True, related_name="projects_many_to_many_database"
    )
    images = models.ManyToManyField(
        ProjectImage, blank=True, related_name="projects_many_to_many_images"
    )
    star = models.ManyToManyField(
        Stars, blank=True, related_name="projects_many_to_many_stars"
    )
    zip_file = models.FileField(
        upload_to="projects/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["zip", "rar", "7zip",'webp'])],
    )
    guid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        blank=True,
    )
    hit_count_generic = GenericRelation(
        HitCount,
        object_id_field="object_pk",
        related_query_name="hit_count_generic_relation",
    )

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        db_table = "projects"
        indexes = [
            models.Index(fields=["guid", "title", "created_at"]),
            models.Index(fields=["name", "title", "created_at", "about"]),
            models.Index(fields=["name", "title", "created_at"]),
            models.Index(fields=["title", "about", "created_at"]),
            models.Index(fields=["price", "name", "title", "about", "created_at"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{str(self.guid)[:8]}-{self.url}")
        super().save(*args, **kwargs)

    @property
    def main_image(self):
        if self.images.exists():
            return self.images.first()
        return None

    @property
    def all_comments(self):
        return self.modelprojectcomment_set.select_related("projects").all()
