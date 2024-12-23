from django.contrib import admin
from projects.models.model_project_comment import ModelProjectComment
from simple_history.admin import SimpleHistoryAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# class ModelProjectCommentResource(resources.ModelResource):
#     class Meta:
#         model = ModelProjectComment
#         fields = "__all__"


@admin.register(ModelProjectComment)
class ModelProjectCommentAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    model = ModelProjectComment
    # resource_class = ModelProjectCommentResource
    list_filter = ("created_at", "updated_at", "is_active", "is_deleted")
    list_display = (
        "id",
        "project",
        "comments",
        "created_at",
        "updated_at",
        "likes_count",
    )

    def comments(self, obj):
        return obj.comment[:50] + "..." if len(obj.comment) > 50 else obj.comment

    def likes_count(self, obj):
        return obj.likes.count()
