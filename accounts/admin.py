from django.contrib import admin
from .models.accounts import CustomUser
from django.contrib.auth.admin import UserAdmin
from simple_history.admin import SimpleHistoryAdmin
from django.utils.html import format_html


@admin.register(CustomUser)
class CustomUserAdmin(SimpleHistoryAdmin, UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "phone", "picture")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

    def profile_picture_tag(self, obj):
        if obj.picture:
            return format_html(
                '<img src="{}" style="width: 100px; height: 100px; border-radius: 10%;" />',
                obj.picture.url,
            )
        return "-"

    profile_picture_tag.short_description = "Profile Picture"

    profile_picture_tag.allow_tags = True
