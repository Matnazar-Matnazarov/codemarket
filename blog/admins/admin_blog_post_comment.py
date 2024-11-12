from django.contrib import admin
from blog.models.model_comment_on_blog_post import Comment
from simple_history.admin import SimpleHistoryAdmin


@admin.register(Comment)
class CommentAdmin(SimpleHistoryAdmin):
    list_display = (
        "comment",
        "post",
        "user",
        "created_at",
        "updated_at",
        "is_active",
    )
    list_filter = ("post", "user__email", "is_active", "created_at")
    search_fields = ("comment", "user__email")
    ordering = ("-created_at",)
    readonly_fields = (
        "created_at",
        "updated_at",
        "history",
    )
    list_per_page = 25

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "comment",
                    "user",
                    "post",
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

    history_list_display = ["status"]
