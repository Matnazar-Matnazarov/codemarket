from rest_framework import serializers
from .serializer_blog_post import BlogPostSerializer
from accounts.serializers.accounts import CustomUserSerializer
from blog.models.model_comment_on_blog_post import Comment
from .serializer_blog_post import BlogPostSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    post = BlogPostSerializer(read_only=True)
    comment = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Comment
        fields = [
            "user",
            "post",
            "comment",
            "created_at",
            "updated_at",
            "is_active",
        ]
