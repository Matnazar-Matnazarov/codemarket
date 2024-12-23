from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError
from ..models.model_project import Project

# Project modelidagi zip fayl hajmini tekshirish
# @receiver(pre_save, sender=Project)
# def update_project_zip_file(sender, instance, **kwargs):
#     """
#     Project modelidagi zip faylni saqlashdan oldin uning hajmini tekshirish.
#     Fayl hajmi 10 MB dan oshmasligi kerak.
#     """
#     if instance.zip_file:  # Agar zip fayl mavjud bo'lsa
#         max_file_size = 10 * 1024 * 1024  # 10 MB
#         if instance.zip_file.size > max_file_size:
#             raise ValidationError("Fayl hajmi 10 MB dan oshmasligi kerak.")
#     # Fayl hajmi tekshirilganidan keyin save() ni chaqirish kerak emas, chunki pre_save signalida save avtomatik bo'ladi.
