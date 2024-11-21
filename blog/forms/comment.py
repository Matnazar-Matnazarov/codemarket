from django import forms
from django.core.exceptions import ValidationError


class CommentForm(forms.Form):
    comment = forms.CharField(
        max_length=500,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter comment"}
        ),
    )
