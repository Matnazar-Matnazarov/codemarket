from django.urls import path, include
from .routers import *
from .views.home import ProjectAnalysisView, HomeView
from .views.project import ProjectView, ProjectJsonView, ProjectDetailView
from .utils.check_post_tags import check_post_tags
from .api_views.views_json_project import ProjectJsonAPIView
from .views.product_basket import ProductBasketView
from .views.add_project import CreateProjectView

# app_name = "api-projects"

urlpatterns = [
    path("", HomeView.as_view(), name="homeview"),
    path("project-analysis/", ProjectAnalysisView.as_view(), name="project-analysis"),
    path("products/", ProjectView.as_view(), name="products"),
    path("products/json/", ProjectJsonView.as_view(), name="project-json"),
    path(
        "products/detail/<slug:slug>/",
        ProjectDetailView.as_view(),
        name="project_detail",
    ),
    path("check-post-tags/", check_post_tags, name="check-post-tags"),
    path("project-api/", include(project_router.urls)),  # Project related endpoints
    path("project-json/", ProjectJsonAPIView.as_view(), name="project-json"),
    path("product-purchases/", ProductBasketView.as_view(), name="product_basket"),
    path("add-project/", CreateProjectView.as_view(), name="create_project"),
]
