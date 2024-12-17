from django.db import models

class ProjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_check_admin=True)

class ProjectBuyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(done=True)
