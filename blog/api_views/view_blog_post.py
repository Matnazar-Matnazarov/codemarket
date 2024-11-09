from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.validators import ValidationError
from blog.models.model_blog_post import Post
from ..serializers.serializer_blog_post import BlogPostSerializer
from datetime import datetime, timezone


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for handling Blog Post operations efficiently"""

    queryset = Post.objects.select_related("author").prefetch_related("comments").all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    swagger_tags = ["Blog Posts"]

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

    def validate_post_data(self, data):
        """Validate post data"""
        # Validate title
        title = data.get("title", "")
        if not title:
            raise ValidationError("Title is required")
        if len(title) < 5:
            raise ValidationError("Title must be at least 5 characters long")
        if len(title) > 200:
            raise ValidationError("Title must not exceed 200 characters")

        # Validate content
        content = data.get("content", "")
        if not content:
            raise ValidationError("Content is required")
        if len(content) < 50:
            raise ValidationError("Content must be at least 50 characters long")

        # Validate tags if present
        tags = data.get("tags", [])
        if tags and len(tags) > 10:
            raise ValidationError("Maximum 10 tags are allowed")

    def perform_create(self, serializer):
        """Validate and create post"""
        self.validate_post_data(self.request.data)
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Validate and update post"""
        self.validate_post_data(self.request.data)
        serializer.save()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(self.get_response_data(serializer_data=response.data))

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            self.get_response_data(
                serializer_data=response.data, message="Post created successfully"
            ),
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            self.get_response_data(
                serializer_data=response.data, message="Post updated successfully"
            )
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            self.get_response_data(message="Post deleted successfully"),
            status=status.HTTP_204_NO_CONTENT,
        )

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        return Response(
            self.get_response_data(message=str(exc), success=False),
            status=response.status_code,
        )
