from datetime import datetime, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from projects.models.model_project import Project
from projects.serializers import ProjectSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend


class ProjectPagination(PageNumberPagination):
    page_size = 20  # Increased for better performance
    page_size_query_param = "page_size"
    max_page_size = 100


class ProjectViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling all Project CRUD operations efficiently.
    Combines list and detail views into a single class.
    """

    queryset = Project.objects.prefetch_related(
        "database", "technology", "images", "star"
    ).select_related("user").all()
    serializer_class = ProjectSerializer
    pagination_class = ProjectPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "about", "technology__name", "database__name"]
    ordering_fields = ["created_at", "price"]
    ordering = ["-created_at"]  # Default to newest first
    permission_classes = [IsAuthenticatedOrReadOnly]
    swagger_tags = ["Projects"]
    swagger_operation_summary = "Project CRUD operations"
    swagger_response = {
        200: "Success",
        201: "Created",
        204: "No Content",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        500: "Internal Server Error",
    }

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return super().get_permissions()

    def get_response_data(self, serializer_data, response=None):
        """Standardized response format"""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status_code": response.status_code if response else 200,
            "success": True,
            "message": "success",
            "data": serializer_data,
        }

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = self.get_response_data(
            serializer_data=response.data, response=response
        )
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data = self.get_response_data(serializer_data=response.data)
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = self.get_response_data(
            serializer_data=response.data, message="Project created successfully"
        )
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = self.get_response_data(
            serializer_data=response.data, message="Project updated successfully"
        )
        return response

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            self.get_response_data(
                message="Project deleted successfully", serializer_data=None
            ),
            status=status.HTTP_204_NO_CONTENT,
        )

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        response.data = self.get_response_data(
            serializer_data=response.data, message="Error occurred", success=False
        )
        return response
