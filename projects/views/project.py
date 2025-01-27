from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
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
from django.utils import timezone
from datetime import timedelta
from ..models.model_project_image import ProjectImage
from hitcount.models import HitCount
from hitcount.views import (
    HitCountMixin,
)
from django.contrib import messages
from ..models.model_stars import Stars
from rest_framework import status
from ..utils.project_detail import ProjectDetailFunc
from ..models.model_project_buy import ModelProjectBuy

class ProjectView(View):
    def get(self, request):
        technologies = (
            ProjectLanguage.objects.filter(technology__isnull=False)
            .order_by("created_at")
            .values_list("technology", flat=True)
            .distinct()
        )
        return render(request, "product.html", {"technologies": technologies})


class ProjectJsonView(View):
    def get(self, request):
        # Yangi loyiha deb hisoblanadigan sanani o'rnatish
        cutoff_date = timezone.now() - timedelta(days=7)

        # Loyihalarni oldindan yuklash va agregatsiya qilish
        projects = (
            Project.objects.prefetch_related(
                Prefetch("images", queryset=ProjectImage.objects.only("image")),
                Prefetch(
                    "technology", queryset=ProjectLanguage.objects.only("technology")
                ),
                Prefetch("database", queryset=ProjectBase.objects.only("name")),
                Prefetch("star", queryset=Stars.objects.only("stars")),
            )
            .filter(is_active=True, is_check_admin=True)
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
        )

        project_list = []
        for project in projects:
            all_technologies = [
                tech.technology for tech in project.technology.all()
            ] + [db.name for db in project.database.all()]
            main_image_url = project.images.first()

            project_dict = {
                "slug": str(project.slug),
                "title": project.title,
                "description": project.about,
                "image": str(main_image_url.image) if main_image_url else None,
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

        return JsonResponse(
            {"products": project_list}, safe=False, status=status.HTTP_200_OK
        )


class ProjectDetailView(View):
    def get(self, request, slug):
        context = {}
        done = False
        project = ProjectDetailFunc(slug=slug)
        if request.user.is_authenticated:
            done=True
        if done:
            done = ModelProjectBuy.objects.filter(project= project, user = request.user, done= True).select_related('project','user').first()
        if not project: 
            messages.error(request, "Project not found")
            return redirect("products")

        context["project"] = project
        context["main_image"] = (
            project.images or None
        ) 

        # Cache  hit count
        hitcount = HitCount.objects.get_for_object(project)
        hits = hitcount.hits
        context["hitcount"] = {"pk": hitcount.pk}
        context["done"] = done
        # CountMixin to count  hits
        hitcount_mixin = HitCountMixin()
        hitcount_response = hitcount_mixin.hit_count(request, hitcount)
        if hitcount_response.hit_counted:
            hits += 1  # hits count +1
            context["hitcount"].update(
                {"hit_counted": hitcount_response.hit_counted, "total_hits": hits}
            )

        return render(request, "project_detail.html", context)
