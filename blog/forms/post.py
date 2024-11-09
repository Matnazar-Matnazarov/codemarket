from ..models.model_blog_post import Post
from django import forms
from accounts.models import CustomUser


class PostForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter post title"}
        ),
    )
    body = forms.CharField(
        max_length=500,
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Write your post content here",
                "rows": 5,
            }
        ),
    )
    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_active=True),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Post
        fields = ["name", "body", "user", "slug"]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        body = cleaned_data.get("body")
        user = cleaned_data.get("user")
        slug = cleaned_data.get("slug")

        if not name:
            raise forms.ValidationError("Post title is required")
        if not body:
            raise forms.ValidationError("Post content is required")

        return cleaned_data
