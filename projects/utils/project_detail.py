from django.db.models import (
    Sum,
    Count,
    Prefetch,
    F,
    Case,
    When,
    FloatField,
)
from ..models.model_project import Project
from ..models.model_database import ProjectBase
from ..models.model_language import ProjectLanguage
from ..models.model_project_image import ProjectImage
from ..models.model_stars import Stars


def ProjectDetailFunc(slug):
    # Optimize query with select_related and prefetch_related
    project = (
        Project.objects.prefetch_related(
            Prefetch("images", queryset=ProjectImage.objects.only("image")),
            Prefetch("technology", queryset=ProjectLanguage.objects.only("technology")),
            Prefetch("database", queryset=ProjectBase.objects.only("name")),
            Prefetch("star", queryset=Stars.objects.only("stars")),
        )
        .filter(slug=str(slug), is_active=True, is_check_admin=True)
        .annotate(
            total_stars=Sum("star__stars", default=0),
            total_users=Count("star"),
            rating=Case(
                When(total_users=0, then=0.0),
                default=F("total_stars") * 1.0 / F("total_users"),
                output_field=FloatField(),
            ),
        )
        .only("id","guid", "title", "about", "price", "url", "zip_file", "images")
        .first()
    )
    return project
