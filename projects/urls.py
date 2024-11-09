from django.urls import path
from .routers.api import urlpatterns
from .views.home import ProjectAnalysisView, HomeView
from .views.project import ProjectDetailView, ProjectAllView

app_name = "api-projects"

urlpatterns = urlpatterns
urlpatterns += [
    path("", HomeView.as_view(), name="home"),
    path("project-analysis/", ProjectAnalysisView.as_view(), name="project-analysis"),
    path("products/", ProjectAllView.as_view(), name="project-all"),
    path("project-detail/<slug:slug>/", ProjectDetailView.as_view(), name="project-detail"),
]
