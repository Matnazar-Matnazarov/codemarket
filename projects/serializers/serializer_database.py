from rest_framework import serializers
from ..models.model_database import ProjectBase


class ProjectBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectBase
        fields = "__all__"
