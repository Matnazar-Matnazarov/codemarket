from django.urls import path, include
from .routers import *
from .views.home import ProjectAnalysisView, HomeView
from .views.project import ProjectView, ProjectJsonView, ProjectDetailView
from .utils.check_post_tags import check_post_tags
# app_name = "api-projects"

urlpatterns = [
    path("", HomeView.as_view(), name="homeview"),
    path("project-analysis/", ProjectAnalysisView.as_view(), name="project-analysis"),
    path("products/", ProjectView.as_view(), name="products"),
    path("products/json/", ProjectJsonView.as_view(), name="project-json"),
    path(
        "products/detail/<slug:slug>/",
        ProjectDetailView.as_view(),
        name="project-detail",
    ),
    path("check-post-tags/", check_post_tags, name="check-post-tags"),
    path("project-api/", include(project_router.urls)),  # Project related endpoints
]
