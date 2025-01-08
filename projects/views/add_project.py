from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
import uuid
from ..models.model_project_image import ProjectImage
from ..models.model_database import ProjectBase
from ..models.model_language import ProjectLanguage
from ..forms.project import ProjectForm
from accounts.models.accounts import Role
from ..forms.project import ProjectForm, ProjectImageForm


class CreateProjectView(LoginRequiredMixin, View):
    def post(self, request):
        form = ProjectForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            max_file_size = 10 * 1024 * 1024  # 10 MB
            zip_file = form.cleaned_data.get("zip_file")
            print(zip_file, zip_file.size)
            if zip_file and zip_file.size > max_file_size:
                messages.error(request, "Fayl hajmi 10MB dan oshmasligi kerak")
                context = {
                    "form": ProjectForm(),
                    "form_image": ProjectImageForm(),
                    "form_language": ProjectLanguage.objects.all()
                    .order_by("name")
                    .only("name", "id"),
                    "form_base": ProjectBase.objects.all()
                    .order_by("name")
                    .only("name", "id"),
                }
                return render(request, "add_project.html", context)
            project = form.save(commit=False)
            project.user = user
            project.save()
            images = request.FILES.getlist("image")
            images_num = len(images)
            if images_num > 4:
                if user.role == Role.BASIC:
                    images_num = 4
                    messages.warning(
                        request,
                        "Standart tarifda maksimak 4 ta rasm qabul qilinadi\n4 tasi olindi",
                    )
                elif user.role == Role.PREMIUM and images_num > 8:
                    images_num = 8
                    messages.warning(
                        request,
                        "Premium tarifda maksimak 8 ta rasm qabul qilinadi\n8 tasi olindi",
                    )
            image_objects = [
                ProjectImage(
                    image=image, name=f"{project.name}_{i}_{str(uuid.uuid4())}"
                )
                for i, image in enumerate(images[:images_num])
            ]
            print(image_objects)
            ProjectImage.objects.bulk_create(image_objects)
            project.images.add(*image_objects)
            print("Barcha images-list fayllar:", images)
            selected_technologies = request.POST.getlist("technology[]")
            technologies = [int(i) for i in selected_technologies[0].split(",")]
            print(technologies)
            project.technology.set(technologies)
            print(project)
            # Tanlangan texnologiyalarni ko'rish uchun
            selected_database = request.POST.getlist("database[]")
            print(selected_database[0].split(","))
            databases = [int(i) for i in selected_database[0].split(",")]
            print(databases)
            project.database.set(databases)
            messages.success(
                request,
                "Ma'lumotlar muvaffaqiyatli qo'shildi, admin tomonidan tekshiriladi",
            )
            return redirect("homeview")
        context = {
            "form": ProjectForm(),
            "form_image": ProjectImageForm(),
            "form_language": ProjectLanguage.objects.all()
            .order_by("name")
            .only("name", "id"),
            "form_base": ProjectBase.objects.all().order_by("name").only("name", "id"),
        }
        return render(request, "add_project.html", context)

    def get(self, request):
        context = {
            "form": ProjectForm(),
            "form_image": ProjectImageForm(),
            "form_language": ProjectLanguage.objects.all()
            .order_by("name")
            .only("name", "id"),
            "form_base": ProjectBase.objects.all().order_by("name").only("name", "id"),
        }
        return render(request, "add_project.html", context)


"""
['6,10,1,4,5,7,3,11']
['2,1']
"""
