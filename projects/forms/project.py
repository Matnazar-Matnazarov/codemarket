from django import forms
from ..models.model_project import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "name",
            "title",
            "about",
            "technology",
            "database",
            "price",
            "url",
            "zip_file",
            "images",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["zip_file"].widget.attrs.update({"accept": ".zip"})
