from django.contrib import admin
from blog.models.model_blog_post import Post, Tags
from simple_history.admin import SimpleHistoryAdmin
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.admin import GenericTabularInline
from django_ckeditor_5.widgets import CKEditor5Widget
from import_export import resources
from django.core.exceptions import ValidationError
from import_export.admin import ImportExportModelAdmin


class TagsResource(resources.ModelResource):
    class Meta:
        model = Tags
        fields = "__all__"


class TagsInline(GenericTabularInline):
    model = Tags
    extra = 1


class PostResource(resources.ModelResource):
    class Meta:
        model = Post
        fields = "__all__"


@admin.register(Post)
class PostAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    model = Post
    resource_class = PostResource
    # List view customization
    list_display = (
        "title",
        "created_at",
        "is_active",
        "is_deleted",
        "image",
        "icon_name",
        "get_tags",
    )
    list_filter = ("is_active", "is_deleted", "created_at")
    search_fields = ("title", "body", "icon_name")
    ordering = ("-created_at",)
    inlines = [TagsInline]

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="150" />')
        return ""

    def get_tags(self, obj):
        return ", ".join(o.name for o in obj.tags.all())

    # Detail view customization
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "author",
                    "title",
                    "body",
                    "is_active",
                    "is_deleted",
                    "image",
                    "icon_name",
                )
            },
        ),
        (
            "Advanced options",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at")

    # Add history for the model

    # Pagination in admin view
    list_per_page = 25

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "body":
            return db_field.formfield(
                widget=CKEditor5Widget(
                    attrs={"class": "django_ckeditor_5"}, config_name="extends"
                )
            )
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(Tags)
class TagsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = Tags
    resource_class = TagsResource
    list_display = ("name", "slug", "content_type", "object_id", "content_object")
    search_fields = ("name", "slug")
    list_filter = ("content_type",)
    ordering = ("name",)
    list_per_page = 25
