from django.contrib import admin
from blog.models.model_blog_post import Post
from simple_history.admin import SimpleHistoryAdmin


# Customize the Post Admin
@admin.register(Post)
class PostAdmin(SimpleHistoryAdmin):
    # List view customization
    list_display = ("name", "user", "created_at", "is_active", "is_deleted")
    list_filter = ("is_active", "is_deleted", "created_at")
    search_fields = ("name", "user__username", "body", "comment")
    ordering = ("-created_at",)

    # Detail view customization
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "user",
                    "body",
                    "comment",
                    "is_active",
                    "is_deleted",
                )
            },
        ),
        (
            "Advanced options",
            {
                "classes": ("collapse",),
                "fields": ("created_at", "updated_at", "history"),
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at")

    # Save slug automatically based on the name
    prepopulated_fields = {"slug": ("name",)}

    # Add history for the model
    history_list_display = ["status"]

    # Pagination in admin view
    list_per_page = 25
