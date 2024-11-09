from rest_framework import serializers

from ..models.model_project import Project
from .serializer_database import ProjectBaseSerializer
from .serializer_image import ProjectImageSerializer
from .serializer_language import ProjectLanguageSerializer
from accounts.serializers.accounts import CustomUserSerializer
from blog.serializers.serializer_comment import CommentSerializer
from ..models.model_project_comment import ModelProjectComment

# serializers Project
class ProjectSerializer(serializers.ModelSerializer):
    technology = ProjectLanguageSerializer(read_only=True, many=True)
    database = ProjectBaseSerializer(read_only=True, many=True)
    # images = ProjectImageSerializer(read_only=True, many=True)
    star = serializers.SerializerMethodField("get_star")
    # first_page = serializers.SerializerMethodField("get_main_image")
    # get_comments = serializers.SerializerMethodField("get_all_comments")

    class Meta:
        model = Project
        fields = [
            "pk",
            "name",
            "created_at",
            "updated_at",
            "slug",
            "is_active",
            "is_deleted",
            "title",
            "about",
            "price",
            "url",
            "technology",
            "database",
            "images",
            "zip_file",
            "guid",
            "star",
            # "first_page",
            # "get_comments",
        ]
        read_only_fields = ["created_at", "updated_at", "slug"]

    @staticmethod
    def get_star(obj):
        return obj.star.count()

    # @staticmethod
    # def get_main_image(obj):
    #     main_image = obj.main_image
    #     return ProjectImageSerializer(main_image).data if main_image else None

