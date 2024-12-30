from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
from django.core.exceptions import ValidationError
from ..models.model_project import Project
from ..models.model_project_image import ProjectImage


# Project modelidagi zip fayl hajmini tekshirish
@receiver(post_delete, sender=Project)
def delete_project(sender, instance, **kwargs):
    project = instance
    project_images = project.images.all().delete()
    print(project_images)
