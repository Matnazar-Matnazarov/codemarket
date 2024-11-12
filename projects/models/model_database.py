from django.db import models
from django.utils.text import slugify
from .model_base import ModelBase
from django.core.validators import FileExtensionValidator


class ProjectBase(ModelBase):
    image = models.ImageField(
        upload_to="project_base/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpg", "webp"])],
    )

    class Meta:
        verbose_name = "Project Database"
        verbose_name_plural = "Project Databases"
        indexes = [
            models.Index(fields=["name", "created_at"]),
        ]
        db_table = "databases"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
