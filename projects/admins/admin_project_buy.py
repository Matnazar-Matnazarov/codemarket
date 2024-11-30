from django.contrib import admin
from ..models.model_project_buy import ModelProjectBuy


@admin.register(ModelProjectBuy)
class AdminProjectBuy(admin.ModelAdmin):
    list_display = (
        "project",
        "user",
        "done",
        "created_at",
        "updated_at",
        "comment",
        "project__price",
    )
    list_display_links = ("project", "user")
    search_fields = ("project__name", "user__email", "user__username", "comment")
    list_filter = ("done", "created_at", "updated_at", "project", "user")
    readonly_fields = ("token", "created_at", "updated_at")
    list_per_page = 25
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        ("Project Information", {"fields": ("project", "user", "done")}),
        (
            "Additional Information",
            {"fields": ("comment", "token"), "classes": ("collapse",)},
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
