from django.contrib import admin
from projects.models.model_language import ProjectLanguage
from simple_history.admin import SimpleHistoryAdmin
from .admin_project import ProjectTechnologyInline
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# class ProjectLanguageResource(resources.ModelResource):
#     class Meta:
#         model = ProjectLanguage
#         fields = "__all__"


@admin.register(ProjectLanguage)
class ProjectLanguageAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    model = ProjectLanguage
    # resource_class = ProjectLanguageResource
    list_display = ("name", "technology", "language", "created_at", "is_active")
    list_filter = ("technology", "language", "is_active", "created_at")
    search_fields = ("name", "technology", "language")
    ordering = ("-created_at",)
    inlines = [ProjectTechnologyInline]
    readonly_fields = ("created_at", "updated_at", "history")
    list_per_page = 25

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "technology",
                    "language",
                    "technology_image",
                    "language_image",
                    "is_active",
                    "is_deleted",
                )
            },
        ),
        (
            "Advanced options",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                    "history",
                ),
            },
        ),
    )

    prepopulated_fields = {"slug": ("name", "technology", "language")}
    readonly_fields = ("created_at", "updated_at", "history")
    list_per_page = 25
