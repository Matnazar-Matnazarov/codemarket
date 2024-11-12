from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from ..models.model_project import Project
from django.db.models import Sum, Count
from django.utils import timezone
from accounts.models import CustomUser
from rest_framework import status
from django.db.models import F


class HomeView(View):
    def get(self, request):
        current_date = timezone.now()

        # Optimize query with prefetch_related for better performance and related data
        project_stats = (
            Project.objects.prefetch_related("technology", "database", "images", "star")
            .filter(
                is_active=True,
                created_at__year=current_date.year,
                created_at__month=current_date.month,
            )
            .aggregate(total_sales=Sum("price"), total_projects=Count("pk"))
        )

        # Get active users count in single query
        active_users = CustomUser.objects.filter(is_active=True).count()

        # Calculate conversion rate
        total_sales = project_stats["total_sales"] or 0
        total_projects = project_stats["total_projects"]
        conversion_rate = (
            (total_projects / active_users * 100) if active_users > 0 else 0
        )

        context = {
            "summary_stats": {
                "total_sales": total_sales,
                "active_users": active_users,
                "conversion_rate": round(conversion_rate, 1),
            }
        }

        return render(request, "home.html", context)


class ProjectAnalysisView(View):
    def get(self, request):
        current_year = timezone.now().year
        years = [str(year) for year in range(current_year - 2, current_year + 1)]
        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]

        # Single optimized query to get all required data
        sales_data = (
            Project.objects.filter(is_active=True)
            .annotate(year=F("created_at__year"), month=F("created_at__month"))
            .values("name", "year", "month")
            .annotate(total_sales=Sum("price"))
            .order_by("name", "year", "month")
        )
        # Process data efficiently
        projects_data = {}
        for record in sales_data:
            name = record["name"]
            year = str(record["year"])
            month = record["month"] - 1  # Convert to 0-based index
            sales = record["total_sales"] or 0

            if name not in projects_data:
                projects_data[name] = {
                    "name": name,
                    "sales": {year: [0] * 12 for year in years},
                }

            if year in years:
                projects_data[name]["sales"][year][month] = sales

        response_data = {
            "years": years,
            "months": months,
            "projects": list(projects_data.values()),
        }

        return JsonResponse(response_data, status=status.HTTP_200_OK)
