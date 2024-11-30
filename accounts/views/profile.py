from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, "profile.html", {"user": user})
