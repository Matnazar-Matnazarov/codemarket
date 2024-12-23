from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError

# from ..models.model_project import Project
# from ..models.model_project_image import ProjectImage
# from ..models.model_database import ProjectBase
# from ..models.model_language import ProjectLanguage
from ..forms.project import ProjectForm
# from accounts.models.accounts import Role


# class AddProjectView(LoginRequiredMixin, View):
#     template_name = "add_project.html"

#     def get(self, request):
#         context = {
#             "form": ProjectForm(),
#             "databases": ProjectBase.objects.values_list("name", flat=True),
#             "technologies": ProjectLanguage.objects.values_list(
#                 "technology", flat=True
#             ),
#         }
#         return render(request, self.template_name, context)

#     def post(self, request):
#         form = ProjectForm(request.POST, request.FILES)

#         if not form.is_valid():
#             messages.error(request, "Invalid form data")
#             return redirect("add_project")

#         try:
#             return self._handle_project_creation(request, form)
#         except ValidationError as e:
#             messages.error(request, str(e))
#             return redirect("add_project")
#         except Exception as e:
#             messages.error(request, f"Error occurred: {str(e)}")
#             return redirect("add_project")

#     def _handle_project_creation(self, request, form):
#         with transaction.atomic():
#             self._validate_project_limits(request)

#             images = request.FILES.getlist("images")
#             databases = self._get_validated_items(
#                 ProjectBase,
#                 request.POST.getlist("databases"),
#                 "name",
#                 limit=3,
#                 error_msg="Maximum 3 databases allowed",
#             )

#             technologies = self._get_validated_items(
#                 ProjectLanguage,
#                 request.POST.getlist("technology"),
#                 "technology",
#                 limit=7,
#                 error_msg="Maximum 7 technologies allowed",
#             )

#             self._validate_images(request, images)

#             # Bulk create project images efficiently
#             project_images = ProjectImage.objects.bulk_create(
#                 [
#                     ProjectImage(image=image, name=form.cleaned_data["name"])
#                     for image in images
#                 ]
#             )

#             # Create project with all fields in one go
#             project = Project.objects.create(
#                 user=request.user,
#                 **{
#                     field: form.cleaned_data[field]
#                     for field in [
#                         "name",
#                         "title",
#                         "description",
#                         "zip_file",
#                         "url",
#                         "price",
#                     ]
#                 },
#             )

#             # Bulk add relationships
#             project.images.add(*project_images)
#             if databases:
#                 project.database.add(*databases)
#             if technologies:
#                 project.technology.add(*technologies)

#             messages.success(request, "Project created successfully!")
#             return redirect("add_project")

#     def _validate_project_limits(self, request):
#         project_count = Project.objects.filter(user=request.user).count()
#         max_projects = 10 if request.user.role != Role.BASIC else 1

#         if project_count >= max_projects:
#             raise ValidationError(
#                 f"Maximum {max_projects} projects allowed for your account type"
#             )

#     def _validate_images(self, request, images):
#         image_limit = 10 if request.user.role != Role.BASIC else 5
#         if len(images) > image_limit:
#             raise ValidationError(f"Maximum {image_limit} images allowed")

#     def _get_validated_items(self, model, items, field, limit, error_msg):
#         filtered_items = set(
#             model.objects.filter(**{field: item}).first()
#             for item in items
#             if model.objects.filter(**{field: item}).exists()
#         )
#         if len(filtered_items) > limit:
#             raise ValidationError(error_msg)
#         return filtered_items


class AddProjectView(LoginRequiredMixin, View):
    template_name = "add_project.html"

    def get(self, request):
        context = {
            "form": ProjectForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("add_project")
        return render(request, self.template_name, {"form": form})
