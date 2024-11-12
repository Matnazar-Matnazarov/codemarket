from ..models.model_comment_on_blog_post import Comment
from django import forms
from django.core.exceptions import ValidationError
from ..models.model_blog_post import Post
from accounts.models import CustomUser


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        max_length=500,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter comment"}
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
        fields = ["comment", "user", "post"]

    def clean(self):
        cleaned_data = super().clean()
        comment = cleaned_data.get("comment")
        user = cleaned_data.get("user")
        post = cleaned_data.get("post")

        if not comment:
            raise ValidationError("Comment is required")
        if not user:
            raise ValidationError("User is required")
        if not post:
            raise ValidationError("Post is required")

        return cleaned_data
