from django.contrib import admin
from django.utils.safestring import mark_safe
from projects.models.model_project_image import ProjectImage
from simple_history.admin import SimpleHistoryAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ProjectImageResource(resources.ModelResource):
    class Meta:
        model = ProjectImage
        fields = "__all__"


@admin.register(ProjectImage)
class ProjectImageAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    """ProjectImage modelining admin interfeysi."""

    model = ProjectImage
    resource_class = ProjectImageResource

    list_display = ("name", "image_preview", "created_at", "is_active", "is_deleted")
    list_filter = ("is_active", "is_deleted", "created_at", "updated_at")
    search_fields = ("name", "slug")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 25
    prepopulated_fields = {"slug": ("name",)}

    fieldsets = (
        (
            "Asosiy ma'lumotlar",
            {"fields": ("name", "slug", "image", "is_active", "is_deleted")},
        ),
        (
            "Qo'shimcha ma'lumotlar",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    def image_preview(self, obj):
        """Rasmni admin panelda ko'rsatish uchun HTML teg qaytaradi."""
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-width: 100px; height: auto;" />'
            )
        return "Rasm yo'q"

    image_preview.short_description = "Rasm ko'rinishi"

    actions = ["mark_active", "mark_inactive", "mark_deleted", "mark_undeleted"]

    def mark_active(self, request, queryset):
        """Tanlangan rasmlarni faollashtirish."""
        queryset.update(is_active=True)
        self.message_user(request, "Tanlangan rasmlar faollashtirildi.")

    def mark_inactive(self, request, queryset):
        """Tanlangan rasmlarni nofaollashtirish."""
        queryset.update(is_active=False)
        self.message_user(request, "Tanlangan rasmlar nofaollashtirildi.")

    def mark_deleted(self, request, queryset):
        """Tanlangan rasmlarni o'chirish."""
        queryset.update(is_deleted=True)
        self.message_user(request, "Tanlangan rasmlar o'chirildi.")

    def mark_undeleted(self, request, queryset):
        """Tanlangan rasmlarni qayta tiklash."""
        queryset.update(is_deleted=False)
        self.message_user(request, "Tanlangan rasmlar qayta tiklandi.")

    mark_active.short_description = "Tanlangan rasmlarni faollashtirish"
    mark_inactive.short_description = "Tanlangan rasmlarni nofaollashtirish"
    mark_deleted.short_description = "Tanlangan rasmlarni o'chirish"
    mark_undeleted.short_description = "Tanlangan rasmlarni qayta tiklash"
