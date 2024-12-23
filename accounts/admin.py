from django.contrib import admin
from .models.accounts import CustomUser
from django.contrib.auth.admin import UserAdmin
from simple_history.admin import SimpleHistoryAdmin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ExportMixin
from import_export.admin import ImportExportModelAdmin


# class CustomUserResource(resources.ModelResource):
#     class Meta:
#         model = CustomUser
#         fields = "__all__"


@admin.register(CustomUser)
class CustomUserAdmin(ImportExportModelAdmin, SimpleHistoryAdmin, UserAdmin):
    model = CustomUser
    # resource_class = CustomUserResource
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "phone", "picture", "codecoins")},
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
                    "role",
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
                "fields": ("email", "password1", "password2", "codecoins"),
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "codecoins",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "codecoins")
    search_fields = ("username", "email", "first_name", "last_name", "codecoins")
    ordering = (
        "username",
        "email",
    )

    def profile_picture_tag(self, obj):
        if obj.picture:
            return format_html(
                '<img src="{}" style="width: 100px; height: 100px; border-radius: 10%;" />',
                obj.picture.url,
            )
        return "-"

    def set_coins(self, obj):
        return obj.codecoins

    profile_picture_tag.short_description = "Profile Picture"

    profile_picture_tag.allow_tags = True
