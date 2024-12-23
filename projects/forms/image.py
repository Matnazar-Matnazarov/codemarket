from django import forms
from ..models.model_project import ProjectImage


class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ["name", "image"]
