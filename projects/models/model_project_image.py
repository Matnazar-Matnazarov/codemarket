from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from .model_base import ModelBase


class ProjectImage(ModelBase):
    image = models.ImageField(
        upload_to="project_images/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpg"])],
        unique=True,
        db_index=True,
    )

    class Meta:
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"
        db_table = "projects_project_image"
        indexes = [
            models.Index(fields=["image", "created_at", "name"]),
            models.Index(fields=["image", "name"]),
            models.Index(fields=["image", "name", "slug"]),
        ]

    def __str__(self):
        return str(self.image)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.image}")
        super().save(*args, **kwargs)
