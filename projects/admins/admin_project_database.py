from django.contrib import admin
from projects.models.model_database import ProjectBase
from simple_history.admin import SimpleHistoryAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ProjectBaseResource(resources.ModelResource):
    class Meta:
        model = ProjectBase
        fields = "__all__"


@admin.register(ProjectBase)
class ProjectBaseAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    """
    ProjectBase modelining admin interfeysi.
    Ushbu klass ProjectBase admin panelini boshqarish va foydalanish uchun moslashtirilgan.
    """

    model = ProjectBase
    resource_class = ProjectBaseResource

    list_display = ("name", "slug", "image", "created_at", "is_active", "is_deleted")
    list_filter = ("is_active", "is_deleted", "created_at", "updated_at")
    search_fields = ("name", "slug", "image")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("-created_at",)
    list_per_page = 25
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            "Asosiy ma'lumotlar",
            {
                "fields": (
                    "name",
                    "slug",
                    "image",
                    "is_active",
                    "is_deleted",
                )
            },
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

    actions = ["mark_active", "mark_inactive", "mark_deleted", "mark_undeleted"]

    def mark_active(self, request, queryset):
        """Tanlangan proyektlarni faollashtirish."""
        queryset.update(is_active=True)
        self.message_user(request, "Tanlangan proyektlar faollashtirildi.")

    def mark_inactive(self, request, queryset):
        """Tanlangan proyektlarni nofaollashtirish."""
        queryset.update(is_active=False)
        self.message_user(request, "Tanlangan proyektlar nofaollashtirildi.")

    def mark_deleted(self, request, queryset):
        """Tanlangan proyektlarni o'chirish."""
        queryset.update(is_deleted=True)
        self.message_user(request, "Tanlangan proyektlar o'chirildi.")

    def mark_undeleted(self, request, queryset):
        """Tanlangan proyektlarni qayta tiklash."""
        queryset.update(is_deleted=False)
        self.message_user(request, "Tanlangan proyektlar qayta tiklandi.")

    mark_active.short_description = "Tanlangan proyektlarni faollashtirish"
    mark_inactive.short_description = "Tanlangan proyektlarni nofaollashtirish"
    mark_deleted.short_description = "Tanlangan proyektlarni o'chirish"
    mark_undeleted.short_description = "Tanlangan proyektlarni qayta tiklash"
