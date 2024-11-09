from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.validators import ValidationError
from projects.models.model_project_image import ProjectImage
from projects.serializers.serializer_image import ProjectImageSerializer
from datetime import datetime
from django.utils import timezone


class ProjectImageViewSet(viewsets.ModelViewSet):
    """ViewSet for handling ProjectImage operations efficiently"""

    queryset = ProjectImage.objects.filter(is_active=True, is_deleted=False)
    serializer_class = ProjectImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return super().get_permissions()

    def get_response_data(self, serializer_data=None, message="success", success=True):
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "success": success,
            "message": message,
            "data": serializer_data,
        }

    def validate_image_file(self, image_file):
        """Validate image file size and format"""
        if not image_file:
            raise ValidationError("Image file is required")

        # Check file size (max 5MB)
        if image_file.size > 5 * 1024 * 1024:
            raise ValidationError("Image file size must be less than 5MB")

        # Check file extension
        allowed_extensions = [".jpg", ".jpeg", ".png", ".gif"]
        ext = image_file.name.lower().split(".")[-1]
        if f".{ext}" not in allowed_extensions:
            raise ValidationError(
                f"Invalid image format. Allowed formats: {', '.join(allowed_extensions)}"
            )

    def perform_create(self, serializer):
        """Validate and create image"""
        image_file = self.request.FILES.get("image")
        self.validate_image_file(image_file)
        serializer.save()

    def perform_update(self, serializer):
        """Validate and update image"""
        image_file = self.request.FILES.get("image")
        if image_file:
            self.validate_image_file(image_file)
        serializer.save()

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(self.get_response_data(serializer_data=response.data))

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            self.get_response_data(
                serializer_data=response.data, message="Image created successfully"
            ),
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            self.get_response_data(
                serializer_data=response.data, message="Image updated successfully"
            )
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            self.get_response_data(message="Image deleted successfully"),
            status=status.HTTP_204_NO_CONTENT,
        )
