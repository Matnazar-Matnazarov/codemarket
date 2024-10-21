from rest_framework import serializers
from ..models.model_language import ProjectLanguage


class ProjectLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectLanguage
        fields = "__all__"
