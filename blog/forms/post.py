from ..models.model_blog_post import Post
from django import forms
from accounts.models import CustomUser


class PostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter post title"}
        ),
    )
    body = forms.CharField(
        max_length=1000,
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Write your post content here",
                "rows": 5,
            }
        ),
    )
    author = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_active=True),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Post
        fields = ["title", "body", "author"]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        body = cleaned_data.get("body")
        author = cleaned_data.get("author")

        if not title:
            raise forms.ValidationError("Post title is required")
        if not body:
            raise forms.ValidationError("Post content is required")

        return cleaned_data
