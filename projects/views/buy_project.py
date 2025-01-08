from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models.model_project_buy import ModelProjectBuy
from accounts.models.accounts import CustomUser
from ..models.model_project import Project
from django.views.generic import View
from django.contrib import messages


class BuyProjectView(LoginRequiredMixin, View):
    def get(self, request, slug):
        project = Project.objects.filter(slug=slug).first()
        if project is None:
            messages.error(request, "Project not found")
            return redirect("products")
        buy_project = ModelProjectBuy.objects.filter(
            project=project.id, user=request.user.id
        ).first()
        context = {"project": project, "done": None}
        if buy_project:
            context["done"] = buy_project.done
        return render(request, "buy_project.html", context)

    def post(self, request, slug):
        user = CustomUser.objects.filter(username=request.user.username).first()
        project = Project.objects.filter(slug=slug, is_check_admin=True).first()
        if project is None:
            messages.error(request, "Project not found")
            return redirect("products")
        if project.price > user.codecoins:
            messages.error(request, "Buy project failed")
            return redirect("products")
        buy_project = ModelProjectBuy.objects.create(
            user=user, project=project, codecoins=project.price, done=True
        )
        buy_project.save()
        user.codecoins -= project.price
        user.save()
        messages.success(request, "Buy project successful")
        return redirect("profile")
