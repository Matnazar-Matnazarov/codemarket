from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    IsAdminUser,
)
from blog.models.model_comment_on_blog_post import Comment
from ..serializers.serializer_comment import CommentSerializer
from datetime import datetime, timezone


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling all Comment operations efficiently.
    Provides standardized CRUD functionality with proper permissions and optimized queries.
    """

    queryset = Comment.objects.select_related("user", "post").all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "pk"
    swagger_tags = ["Comments"]

    def get_queryset(self):
        """Filter active comments for specific post if post_id provided"""
        queryset = super().get_queryset()
        post_id = self.kwargs.get("post_id")
        if post_id:
            return queryset.filter(post_id=post_id, is_active=True)
        return queryset

    def get_permissions(self):
        """
        Custom permissions:
        - GET: Anyone can read
        - POST: Must be authenticated
        - PUT/DELETE: Must be admin
        """
        if self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]

    def get_response_data(self, serializer_data=None, message="success", success=True):
        """Standardized response format"""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "success": success,
            "message": message,
            "data": serializer_data,
        }

    def perform_create(self, serializer):
        """Auto-assign current user and post_id on creation"""
        post_id = self.kwargs.get("post_id")
        serializer.save(user=self.request.user, post_id=post_id)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            self.get_response_data(serializer_data=response.data),
            status=status.HTTP_200_OK,
        )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            self.get_response_data(
                serializer_data=response.data, message="Comment created successfully"
            ),
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            self.get_response_data(
                serializer_data=response.data, message="Comment updated successfully"
            ),
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            self.get_response_data(message="Comment deleted successfully"),
            status=status.HTTP_204_NO_CONTENT,
        )

    def handle_exception(self, exc):
        """Standardized error handling"""
        response = super().handle_exception(exc)
        return Response(
            self.get_response_data(
                serializer_data=None, message=str(exc), success=False
            ),
            status=response.status_code,
        )
