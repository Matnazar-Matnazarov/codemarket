from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from projects.models.model_project import Project
from projects.models.model_project_buy import ModelProjectBuy


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        my_project = Project.objects.filter(user=user, )
        buy_project = ModelProjectBuy.objects.filter(user=user.id)
        context = {"user": user, "user_apps": my_project, "buy_projects": buy_project}
        return render(request, "profile.html", context)

    def post(self, request):
        pass
