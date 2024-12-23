from django.shortcuts import render
from ..forms.login import UserLoginForm, EditProfileForm
from django.contrib.auth import login as login_auth, logout
from django.contrib import messages
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from ..forms.login import EditPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# from rest_framework.authtoken.models import Token
# from rest_framework_simplejwt.models import Token


class LoginView(View):
    def get(self, request):
        user = UserLoginForm()
        return render(request, "registration/login.html", {"user": user})

    def post(self, request):
        check = AuthenticationForm(data=request.POST)
        if check.is_valid():
            user = check.get_user()
            login_auth(request, user)
            next_url = request.GET.get(
                "next", "homeview"
            )  # `next` mavjud bo‘lsa, o‘sha yerga yo‘naltiradi
            try:
                print(next_url)
                if next_url == "":
                    messages.success(request, "You are logged in!")
                    redirect("homeview")
                messages.success(request, "You are logged in!")
                return redirect(next_url)
            except:
                messages.success(request, "You are logged in!")
                redirect("homeview")
        else:
            return redirect("login")


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, "You are logged out!")
        return redirect("homeview")


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = EditProfileForm(instance=request.user)
        return render(request, "registration/edit_profile.html", {"form": form})

    def post(self, request):
        form = EditProfileForm(
            instance=request.user, data=request.POST, files=request.FILES
        )
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully changed your information!")
            return redirect("profile")
        return render(request, "registration/edit_profile.html", {"form": form})


class EditPasswordView(LoginRequiredMixin, View):
    def get(self, request):
        return render(
            request, "registration/edit_password.html", {"form": EditPasswordForm()}
        )

    def post(self, request):
        form = EditPasswordForm(data=request.POST)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data["old_password"]
            if user.check_password(old_password):
                new_password = form.cleaned_data["new_password"]
                confirm_new_password = form.cleaned_data["confirm_new_password"]
                if new_password == confirm_new_password:
                    if new_password == old_password:
                        messages.error(
                            request,
                            "Your new password cannot be the same as your old password!",
                        )
                        return redirect("edit_password")
                    try:
                        validate_password(new_password)
                    except ValidationError as e:
                        try:
                            s = "\n".join(e)
                            messages.error(request, s)
                        except Exception as t:
                            messages.error(request, t)
                        return redirect("edit_password")
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(
                        request, "You have successfully changed your password!"
                    )
                    return redirect("profile")
                else:
                    messages.error(
                        request,
                        "Your new password and confirm new password do not match!",
                    )
                    return redirect("edit_password")

            else:
                messages.error(request, "Your old password is incorrect!")
                return redirect("edit_password")
        return render(request, "registration/edit_password.html", {"form": form})
