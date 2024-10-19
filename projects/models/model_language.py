from django.db import models
from django.utils.text import slugify
from .model_base import ModelBase
from django.core.validators import FileExtensionValidator


# Create your models here.
class ProjectLanguage(ModelBase):
    technology = models.CharField(
        max_length=50, null=True, blank=True, db_index=True, unique=True
    )
    language = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    language_image = models.ImageField(
        upload_to="project_language/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpg"])],
    )
    technology_image = models.ImageField(
        upload_to="project_technology/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpg"])],
    )

    class Meta:
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"
        db_table = "projects_project_language"
        indexes = [
            models.Index(fields=["technology"]),
            models.Index(fields=["language"]),
            models.Index(fields=["name", "technology", "language", "created_at"]),
        ]

    def __str__(self):
        return self.language

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.language}-{self.technology}")
        super().save(*args, **kwargs)
