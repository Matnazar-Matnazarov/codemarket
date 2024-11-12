from rest_framework import serializers
from accounts.serializers.accounts import CustomUserSerializer
from ..models.model_blog_post import Post
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)



class BlogPostSerializer(TaggitSerializer, serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    hit_count = serializers.IntegerField(
        source="hit_count_generic.count", read_only=True
    )
    tags = TagListSerializerField()
    class Meta:
        model = Post
        fields = [
            "id",
            "name",
            "author",
            "body",
            "comment",
            "created_at",
            "is_active",
            "is_deleted",
            "slug",
            "comment",
            "hit_count",
            "tags",
        ]
        read_only_fields = ["hit_count"]
