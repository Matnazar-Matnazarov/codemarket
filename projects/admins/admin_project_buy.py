from django.contrib import admin
from ..models.model_project_buy import ModelProjectBuy
from simple_history.admin import SimpleHistoryAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ModelProjectBuyResource(resources.ModelResource):
    class Meta:
        model = ModelProjectBuy
        fields = "__all__"


@admin.register(ModelProjectBuy)
class AdminProjectBuy(ImportExportModelAdmin, SimpleHistoryAdmin):
    model = ModelProjectBuy
    resource_class = ModelProjectBuyResource
    list_display = (
        "project",
        "user",
        "done",
        "created_at",
        "updated_at",
        "comment",
        "project__price",
        "codecoins",
    )
    list_display_links = ("project", "user")
    search_fields = ("project__name", "user__email", "user__username", "comment")
    list_filter = ("done", "created_at", "updated_at", "project", "user", "codecoins")
    readonly_fields = ("token", "created_at", "updated_at")
    list_per_page = 25
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        ("Project Information", {"fields": ("project", "user", "done")}),
        (
            "Additional Information",
            {"fields": ("comment", "token", "codecoins"), "classes": ("collapse",)},
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
