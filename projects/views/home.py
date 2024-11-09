from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from ..models.model_project import Project
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from accounts.models import CustomUser
from rest_framework import status

class HomeView(View):
    def get(self, request):
        current_year = timezone.now().year

        # Get sales data for each project
        current_month = timezone.now().month
        total_sales = Project.objects.filter(
            is_active=True,
            created_at__year=current_year,
            created_at__month=current_month
        ).aggregate(total=Sum('price'))['total'] or 0

        active_users = CustomUser.objects.filter(
            is_active=True
        ).distinct().count()

        total_projects = Project.objects.filter(
            is_active=True,
            created_at__year=current_year,
            created_at__month=current_month
        ).count()
        print(total_sales,total_projects)
        conversion_rate = (total_projects / active_users * 100) if active_users > 0 else 0

        context = {
            "summary_stats": {
                "total_sales": total_sales,
                "active_users": active_users,
                "conversion_rate": round(conversion_rate, 1)
            }
        }

        return render(request, "home.html", context)

class ProjectAnalysisView(View):
    def get(self, request):
        # Get unique project names
        project_names = Project.objects.filter(is_active=True).values_list('name', flat=True).distinct()
        
        # Setup years and months
        current_year = timezone.now().year
        years = [str(year) for year in range(current_year-2, current_year+1)]
        months = [
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ]

        projects_data = []
        
        # For each project, get sales data by year and month
        for project_name in project_names:
            project_sales = {'name': project_name, 'sales': {}}
            
            for year in years:
                monthly_sales = []
                for month in range(1, 13):
                    sales = Project.objects.filter(
                        is_active=True,
                        name=project_name,
                        created_at__year=year,
                        created_at__month=month
                    ).aggregate(total=Sum('price'))['total'] or 0
                    monthly_sales.append(sales)
                
                project_sales['sales'][year] = monthly_sales
            
            projects_data.append(project_sales)

        response_data = {
            'years': years,
            'months': months,
            'projects': projects_data
        }
        # print(response_data)
        return JsonResponse(response_data, status=status.HTTP_200_OK)
