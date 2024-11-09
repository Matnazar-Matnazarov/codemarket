from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, Count, Q, Prefetch, Avg, F, Aggregate
from ..models.model_project import Project
from ..models.model_database import ProjectBase
from ..models.model_language import ProjectLanguage
from ..models.model_project_buy import ModelProjectBuy


class ProjectAllView(View):
    def get(self, request):
        projects = (
            Project.objects.select_related("user")
            .prefetch_related("images", "technology", "database", "main_image", "stars")
            .annotate(average_stars=Avg("stars__stars"))
        ).filter(is_active=True)
        technologies = ProjectLanguage.objects.all()
        databases = ProjectBase.objects.all()
        context = {
            "projects": projects,
            "technologies": technologies,
            "databases": databases,
        }
        return render(request, "project.html", context)


class ProjectDetailView(View):
    def get(self, request, slug):
        project = Project.objects.prefetch_related("images", "technology", "database", "main_image", "stars").filter(slug=slug).first()
        if not project:
            return redirect(
                reverse("projects:project_all") + "?error=project_not_found"
            )
        context = {"project": project}
        return render(request, "project_detail.html", context)

    def post(self, request, slug):
        if request.user.is_authenticated:
            project = Project.objects.filter(slug=slug).first()
            if not project:
                return redirect(
                    reverse("projects:project_all") + "?error=project_not_found"
                )
            check = ModelProjectBuy.objects.create(project=project, user=request.user)
            if check:
                return redirect(
                    reverse("projects:project_detail", kwargs={"slug": slug})
                    + "?success=project_bought"
                )
            else:
                return redirect(
                    reverse("projects:project_detail", kwargs={"slug": slug})
                    + "?error=project_already_bought"
                )
        else:
            return redirect(
                reverse("accounts:login")
                + "?next="
                + reverse("projects:project_detail", kwargs={"slug": slug})
            )
