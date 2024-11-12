from rest_framework.routers import DefaultRouter
from ..api_views.views_project import ProjectViewSet
from ..api_views.views_image import ProjectImageViewSet

# Separate routers for each logical group
project_router = DefaultRouter()

# Projects API
project_router.register(r"projects", ProjectViewSet, basename="project")
project_router.register(
    r"project-images", ProjectImageViewSet, basename="project-image"
)
