"""
Development settings for local engineering.
"""

from .base import *

DEBUG = True

# Database
# Uses DATABASE_URL from .env or defaults to SQLite
DATABASES = {
    "default": env.db("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Static files storage in development: no manifest hashing needed
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

WHITENOISE_AUTOREFRESH = True
