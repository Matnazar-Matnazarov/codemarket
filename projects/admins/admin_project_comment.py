from django.contrib import admin
from projects.models.model_project_comment import ModelProjectComment


@admin.register(ModelProjectComment)
class ModelProjectCommentAdmin(admin.ModelAdmin):
    pass
