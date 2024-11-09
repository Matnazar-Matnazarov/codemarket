from ..models.model_comment_on_blog_post import Comment
from django import forms
from django.core.exceptions import ValidationError
from ..models.model_blog_post import Post
from accounts.models import CustomUser


class CommentForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter comment title"}
        ),
    )
    body = forms.CharField(
        max_length=500,
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Write your comment here",
                "rows": 3,
            }
        ),
    )
    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_active=True),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    post = forms.ModelChoiceField(
        queryset=Post.objects.filter(is_active=True),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Comment
        fields = ["name", "body", "user", "post"]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        body = cleaned_data.get("body")
        user = cleaned_data.get("user")
        post = cleaned_data.get("post")

        if not name:
            raise ValidationError("Comment title is required")
        if not body:
            raise ValidationError("Comment content is required")
        if not user:
            raise ValidationError("User is required")
        if not post:
            raise ValidationError("Post is required")

        return cleaned_data
