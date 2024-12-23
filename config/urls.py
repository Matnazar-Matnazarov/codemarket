from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.i18n import set_language
import debug_toolbar
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView,
    TokenBlacklistView,
)
from django.views.generic import RedirectView
from django.http import HttpResponse
from django_ckeditor_5.views import upload_file

# API documentation schema configuration
schema_view = get_schema_view(
    openapi.Info(
        title="CodeMarket REST API",
        default_version="v1",
        description="""
        Complete API documentation for the CodeMarket project.
        Includes authentication, projects, blog posts and comments endpoints.
        """,
        terms_of_service="https://www.codemarket.com/terms/",
        contact=openapi.Contact(
            name="CodeMarket Support",
            email="support@codemarket.com",
            url="https://www.codemarket.com",
        ),
        license=openapi.License(
            name="BSD License", url="https://opensource.org/licenses/BSD-3-Clause"
        ),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Main URL patterns
urlpatterns = [
    # Admin URLs
    path("secret/admin/", admin.site.urls, name="admin"),  # Secure admin interface
    path(
        "admin/", include("admin_honeypot.urls", namespace="admin_honeypot")
    ),  # Security honeypot/
    # Development & Debug Tools
    path("__debug__/", include(debug_toolbar.urls)),  # Debug toolbar
    # Internationalization
    path("i18n/", set_language, name="set_language"),
    # CKEditor 5
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("upload/", upload_file, name="custom_upload_file"),
    # Application URLs
    path("", include("projects.urls")),
    # Authentication URLs
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    # path("accounts/", include("django.contrib.auth.urls")),
    path("api/v1/drf-auth/", include("rest_framework.urls")),
    # JWT Token Management
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    # hitcount
    path("hitcount/", include("hitcount.urls", namespace="hitcount")),
    # API Documentation
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc-ui"
    ),
    path(
        "api-docs/",
        RedirectView.as_view(url="/swagger/", permanent=True),
        name="api-docs",
    ),
    path("blog/", include("blog.urls")),
    # Default redirect
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
