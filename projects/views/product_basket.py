from django.shortcuts import render, redirect
from django.db.models import Sum, Count, F, FloatField
from django.db.models import Q
from ..models.model_project_buy import ModelProjectBuy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
from django.contrib import messages

class ProductBasketView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        products = None
        try:
            products = (
                ModelProjectBuy.objects.select_related("project", "user")
                .filter(user=request.user)
                .annotate(
                    project_count=Count(
                        "project__modelprojectbuy",
                        filter=Q(project__modelprojectbuy__done=True),
                    )
                )
            )

            totals = products.aggregate(
                total_investment=Sum("project__price", default=0),
                total_downloads=Count("pk", filter=Q(done=True)),
            )

            # print(products.first().project.images.first())
            context = {
                "products": products,
                "total_investment": totals["total_investment"] or 0,
                "total_downloads": totals["total_downloads"],
            }
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect("home")
        return render(request, "product_purchases.html", context)
