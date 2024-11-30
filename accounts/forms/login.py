from django import forms
from ..models.accounts import CustomUser


class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=254)
    password = forms.CharField(max_length=128)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("picture", "first_name", "last_name")


class EditPasswordForm(forms.Form):
    old_password = forms.CharField(max_length=128)
    new_password = forms.CharField(max_length=128)
    confirm_new_password = forms.CharField(max_length=128)
