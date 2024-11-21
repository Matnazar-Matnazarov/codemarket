from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count, Prefetch, F, Case, When, FloatField
from django.utils import timezone
from datetime import timedelta

from ..models.model_project import Project
from ..models.model_project_image import ProjectImage
from ..models.model_language import ProjectLanguage
from ..models.model_database import ProjectBase
from ..models.model_stars import Stars


class ProjectJsonAPIView(APIView):
    def get(self, request):
        # Define cutoff date for "new" projects (last 7 days)
        cutoff_date = timezone.now() - timedelta(days=7)

        # Optimize query with select_related and prefetch_related
        projects = (
            Project.objects.prefetch_related(
                Prefetch("images", queryset=ProjectImage.objects.only("image")),
                Prefetch(
                    "technology", queryset=ProjectLanguage.objects.only("technology")
                ),
                Prefetch("database", queryset=ProjectBase.objects.only("name")),
                Prefetch("star", queryset=Stars.objects.only("stars")),
            )
            .filter(is_active=True)
            .annotate(
                total_stars=Sum("star__stars", default=0),
                total_users=Count("star"),
                rating=Case(
                    When(total_users=0, then=0.0),
                    default=F("total_stars") * 1.0 / F("total_users"),
                    output_field=FloatField(),
                ),
                is_new=Case(
                    When(created_at__gte=cutoff_date, then=True),
                    default=False,
                    output_field=FloatField(),
                ),
            )
            .only("slug", "title", "about", "price", "created_at")
            # .iterator()  # Use iterator() for memory efficiency
        )

        # Process and format the data
        project_list = []
        for project in projects:
            all_technologies = [
                tech.technology for tech in project.technology.all()
            ] + [db.name for db in project.database.all()]

            main_image = project.images.first()

            project_dict = {
                "slug": str(project.slug),
                "title": project.title,
                "description": project.about,
                "image": str(main_image.image) if main_image else None,
                "price": float(project.price) if project.price else 0.0,
                "rating": round(project.rating or 0, 1),
                "category": "new" if project.is_new else "popular",
                "technologies": all_technologies,
                "uploadDate": (
                    project.created_at.strftime("%Y-%m-%d")
                    if project.created_at
                    else None
                ),
                "badge": "New" if project.is_new else "Popular",
            }
            project_list.append(project_dict)

        return Response({"products": project_list}, status=status.HTTP_200_OK)
