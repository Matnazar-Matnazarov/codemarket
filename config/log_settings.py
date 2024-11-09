# settings.py ichida
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Log fayli saqlanadigan joy
LOG_FILE_PATH = os.path.join(BASE_DIR, "django_errors.txt")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",  # Faqat ERROR va undan yuqori darajadagi loglarni yozish
            "class": "logging.FileHandler",
            "filename": LOG_FILE_PATH,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
    "formatters": {
        "verbose": {
            "format": "{asctime} {levelname} {name} {message}",
            "style": "{",
        },
    },
}
