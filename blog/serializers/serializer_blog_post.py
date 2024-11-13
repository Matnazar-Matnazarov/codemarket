from rest_framework import serializers
from accounts.serializers.accounts import CustomUserSerializer
from ..models.model_blog_post import Post


class BlogPostSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    hit_count = serializers.IntegerField(
        source="hit_count_generic.count", read_only=True
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "body",
            "title",
            "created_at",
            "is_active",
            "is_deleted",
            "hit_count",
        ]
        read_only_fields = ["hit_count"]
