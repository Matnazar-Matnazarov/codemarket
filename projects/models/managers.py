from django.db import models


class ProjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class ProjectBuyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
