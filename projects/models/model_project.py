from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from .model_language import ProjectLanguage
from .model_project_image import ProjectImage
from .model_database import ProjectBase
from .model_base import ModelBase
from hitcount.models import HitCount, HitCountMixin
from django.contrib.contenttypes.fields import GenericRelation
from .model_stars import Stars
from ..utils.generator_id import generate_id
import uuid
from accounts.models.accounts import CustomUser
from .managers import ProjectManager
from ..utils.validators import file_size_validator


class Project(ModelBase):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    about = models.TextField(null=True, blank=True)
    price = models.IntegerField(
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
        validators=[
            FileExtensionValidator(allowed_extensions=["zip", "rar", "7zip", "webp"]),
        ],
    )
    guid = models.UUIDField(
        default=uuid.uuid4, null=True, blank=True, unique=True, db_index=True
    )

    # guid = models.CharField(null=True, blank=True, unique=True, db_index=True, max_length=250)
    hit_count_generic = GenericRelation(
        HitCount,
        object_id_field="object_pk",
        related_query_name="hit_count_generic_relation",
    )
    is_check_admin = models.BooleanField(default=False)
    objects = ProjectManager()

    class Mata:
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
        try:
            # self.guid = generate_id(20, False,False)
            self.slug = slugify(
                f"{'-'.join(map(str, list(self.name.strip())[:2]))}-{'-'.join(map(str, list(self.title.strip())[:2]))}-{self.guid}"[
                    :100
                ]
            )
        except:
            self.slug = slugify(f"{self.name}-{self.guid}"[:100])
        super().save(*args, **kwargs)

    @property
    def main_image(self) -> str | None:
        image = self.images.first()
        if image:
            return str(image.image)
        return None

    # @property
    # def average_stars(self):
    #     return self.star.aggregate(Avg("stars"))["stars__avg"] or 0
