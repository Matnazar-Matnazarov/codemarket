from django.contrib import admin
from django.utils.html import mark_safe
from projects.models.model_project import Project
from simple_history.admin import SimpleHistoryAdmin
from django.utils.text import slugify
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# class ProjectResource(resources.ModelResource):
#     class Meta:
#         model = Project
#         fields = "__all__"


class ProjectTechnologyInline(admin.TabularInline):
    model = Project.technology.through
    extra = 1
    verbose_name = "Technology"
    verbose_name_plural = "Technologies"


class ProjectDatabaseInline(admin.TabularInline):
    model = Project.database.through
    extra = 1
    verbose_name = "Database"
    verbose_name_plural = "Databases"


class ProjectImageInline(admin.TabularInline):
    model = Project.images.through
    extra = 1
    verbose_name = "Image"
    verbose_name_plural = "Images"


class ProjectStarInline(admin.TabularInline):
    model = Project.star.through
    extra = 1
    verbose_name = "Star"
    verbose_name_plural = "Stars"


@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    """
    Admin interface for managing Project instances.
    Provides comprehensive project management functionality with advanced features.
    """

    model = Project
    # resource_class = ProjectResource

    list_display = (
        "user",
        "name",
        "title",
        "price",
        "url",
        "created_at",
        "updated_at",
        "is_active",
        "is_deleted",
        "star_count",
        "display_technologies",
        "display_databases",
        "is_check_admin",
    )
    list_filter = (
        "is_active",
        "is_deleted",
        "created_at",
        "updated_at",
        "technology",
        "database",
        "is_check_admin",
    )
    search_fields = ("title", "name", "about", "url", "guid")
    readonly_fields = (
        "guid",
        "created_at",
        "updated_at",
    )
    inlines = [
        ProjectTechnologyInline,
        ProjectDatabaseInline,
        ProjectImageInline,
        ProjectStarInline,
    ]
    exclude = ("technology", "database", "images", "star")

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("title", "name", "about", "price", "url", "slug", "user")},
        ),
        ("Media", {"fields": ("zip_file",)}),
        ("Status", {"fields": ("is_active", "is_deleted", "is_check_admin")}),
        (
            "System Fields",
            {"classes": ("collapse",), "fields": ("guid", "created_at", "updated_at")},
        ),
    )

    def display_technologies(self, obj) -> str:
        return ", ".join([tech.technology for tech in obj.technology.all()])

    display_technologies.short_description = "Technologies"

    def display_databases(self, obj) -> str:
        return ", ".join([db.name for db in obj.database.all()])

    display_databases.short_description = "Databases"

    def star_count(self, obj):
        return obj.star.count()

    star_count.short_description = "Stars"

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(f"{obj.title}-{obj.name}")
        super().save_model(request, obj, form, change)

    list_per_page = 25
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
