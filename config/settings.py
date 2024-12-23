"""
Django settings for CodeMarket project.

For detailed settings documentation, see:
https://docs.djangoproject.com/en/5.1/topics/settings/
"""

import os
from pathlib import Path
from datetime import timedelta
import dj_database_url
from .jazzmin import JAZZMIN_SETTINGS
from .ckeditor_settings import (
    CKEDITOR_5_CONFIGS,
    CKEDITOR_5_CUSTOM_CSS,
    CKEDITOR_5_FILE_STORAGE,
)
from environs import Env


env = Env()
env.read_env()

# from .log_settings import LOG_FILE_PATH, LOGGING

# Core Settings
BASE_DIR = Path(__file__).resolve().parent.parent
# load_dotenv()

SECRET_KEY = (
    env.str("SECRET_KEY")
    or "django-insecure-scy6y3q5p0ha_e=l679pbvd+v@cfzyl44(5zr2#)kmzmt50c8n"
)

DEBUG = True  # env.bool("DEBUG") or True
ALLOWED_HOSTS = ["*"]  # env.list("ALLOWED_HOSTS", default="*")

# CSRF_TRUSTED_ORIGINS = [
#     "http://127.0.0.1:8000",
#     "https://670a-95-214-211-136.ngrok-free.app/",
# ]
# Logging Configuration
# LOG_FILE_PATH = LOG_FILE_PATH
# LOGGING = LOGGING

# Application Definition
DJANGO_APPS = [
    "jazzmin",  # Admin theme
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

THIRD_PARTY_APPS = [
    "debug_toolbar",
    "hitcount",
    "simple_history",
    "admin_honeypot",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",
    "django_filters",
    "rest_framework.authtoken",
    "django_ckeditor_5",
    "import_export",
    "compressor",
    # Allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",  # Google oauth
]

LOCAL_APPS = [
    "projects",
    "accounts",
    "blog",
]


INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middleware Configuration
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Whitenoise ni qo'shish
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # Allauth middleware
    "config.middlewares.admin_toolbar.AdminDebugToolbarMiddleware",
]

# URL Configuration
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# Template Configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Database Configuration
DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "db.sqlite3",
    # }
    "default": dj_database_url.parse(
        "postgresql://matnazar:zR1xKluz8tFxLNzDGQiSHrLK9diBueMw@dpg-ctgkpql2ng1s738k2q6g-a.oregon-postgres.render.com/codemarket_a9sm"
    )
}


SITE_ID = 1

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]
ACCOUNT_SIGNUP_REDIRECT_URL = "/"
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "METHOD": "oauth2",
        "VERIFIED_EMAIL": True,
    }
}


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ("en", "English"),
    ("uz", "Uzbek"),
    ("ru", "Russian"),
]
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # other finders..
    "compressor.finders.CompressorFinder",
)
# Static Files Configuration
STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


COMPRESS_ENABLED = True  # Ishlab chiqarish uchun True qiling
COMPRESS_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
# COMPRESS_OFFLINE = True  # HTML shablonlarni oldindan siqish
# # COMPRESS_FILTERS = {
#     'css': ['compressor.filters.css_default.CssAbsoluteFilter'],
#     'js': ['compressor.filters.js_default.JSMinFilter'],
# }
# Default Primary Key Field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication
AUTH_USER_MODEL = "accounts.CustomUser"

# REST Framework Settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}

# JWT Settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

# Admin Interface
JAZZMIN_SETTINGS = JAZZMIN_SETTINGS
JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "navbar_fixed": True,
    "show_ui_builder": True,
    "layout_fixed": False,
    "custom_css": "css/custom_admin_1.css",
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}

# Debug Toolbar
INTERNAL_IPS = ["127.0.0.1", "*"]
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: request.user.is_staff,
}


IMPORT_EXPORT_TMP_STORAGE_CLASS = "import_export.tmp_storages.MediaStorage"


# # Celery settings
# CELERY_BROKER_URL = config("REDIS_URL", default="redis://localhost:6379/0")
# CELERY_RESULT_BACKEND = config("REDIS_URL", default="redis://localhost:6379/0")
# CELERY_ACCEPT_CONTENT = ["json"]
# CELERY_TASK_SERIALIZER = "json"
# CELERY_RESULT_SERIALIZER = "json"
# CELERY_TIMEZONE = "UTC"


# Google OAuth settings
# GOOGLE_OAUTH2_CLIENT_ID = env.str("GOOGLE_OAUTH2_CLIENT_ID")
# GOOGLE_OAUTH2_CLIENT_SECRET = env.str("GOOGLE_OAUTH2_CLIENT_SECRET")


LOGIN_URL = "/accounts/login/"  # Login talab qilinadigan sahifalar uchun yo‘naltirish

LOGOUT_REDIRECT_URL = "/"
