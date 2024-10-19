from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.i18n import set_language
import debug_toolbar

urlpatterns = [
    # secret admin URL
    path("secret/admin/", admin.site.urls),  # Django admin
    path(
        "admin/", include("admin_honeypot.urls", namespace="admin_honeypot")
    ),  # Honeypot
    path("__debug__/", include(debug_toolbar.urls)),  # Debug toolbar
    path("i18n/", set_language, name="set_language"),  # Language change
    path("accounts/", include("django.contrib.auth.urls")),  # Authentication
    path("projects/", include("projects.urls")),  # Your app URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
