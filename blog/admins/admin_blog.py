from django.contrib import admin
from blog.models.model_blog_post import Post, Tags
from simple_history.admin import SimpleHistoryAdmin
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.admin import GenericTabularInline


class TagsInline(GenericTabularInline):
    model = Tags
    extra = 1


@admin.register(Post)
class PostAdmin(SimpleHistoryAdmin):
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
                "classes": ("collapse",),
                "fields": ("created_at", "updated_at"),
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at")

    # Add history for the model
    history_list_display = ["status"]

    # Pagination in admin view
    list_per_page = 25


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "content_type", "object_id", "content_object")
    search_fields = ("name", "slug")
    list_filter = ("content_type",)
    ordering = ("name",)
    list_per_page = 25
