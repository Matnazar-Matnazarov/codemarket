from rest_framework import serializers
from ..models.model_project import Project
from .serializer_database import ProjectBaseSerializer
from .serializer_image import ProjectImageSerializer
from .serializer_language import ProjectLanguageSerializer
from accounts.serializers.accounts import CustomUserSerializer


#serializers Project
class ProjectSerializer(serializers.ModelSerializer):
    technology = ProjectLanguageSerializer(read_only=True, many=True)
    database = ProjectBaseSerializer(read_only=True, many=True)
    images = ProjectImageSerializer(read_only=True, many=True)
    likes = CustomUserSerializer(read_only=True, many=True)
    likes_count = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()

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
            "likes",
            "zip_file",
            "guid",
            "likes_count",
            "main_image",
        ]
        read_only_fields = ["created_at", "updated_at", "slug"]

    @staticmethod
    def get_likes_count(obj):
        return obj.likes_count

    @staticmethod
    def get_main_image(obj):
        main_image = obj.main_image
        return ProjectImageSerializer(main_image).data if main_image else None

