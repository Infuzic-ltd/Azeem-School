from .base import *
import os
import dj_database_url

# ── Security ──────────────────────────────────────────────────────────────────
DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-build-placeholder")

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("ALLOWED_HOSTS", "").split(",")
    if h.strip()
] or ["*"]

CSRF_TRUSTED_ORIGINS = [
    "https://*.vercel.app",
]
custom_domain = os.environ.get("CUSTOM_DOMAIN")
if custom_domain:
    CSRF_TRUSTED_ORIGINS.append(f"https://{custom_domain}")

# ── PostgreSQL apps ───────────────────────────────────────────────────────────
INSTALLED_APPS = list(INSTALLED_APPS) + ["django.contrib.postgres"]

# ── Database ──────────────────────────────────────────────────────────────────
database_url = os.environ.get("DATABASE_URL")
if database_url:
    DATABASES = {
        "default": dj_database_url.parse(
            database_url,
            conn_max_age=600,
        )
    }

# ── Static files (served by Vercel edge — no WhiteNoise needed) ───────────────
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# STATIC_ROOT = BASE_DIR / "staticfiles"
# STATIC_URL = "/static/"

STATIC_ROOT = PROJECT_DIR.parent / "home" / "assets"
STATIC_URL = "/static/"

# ── Cloudinary (override base.py with env vars if set) ───────────────────────
_cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
_api_key    = os.environ.get("CLOUDINARY_API_KEY")
_api_secret = os.environ.get("CLOUDINARY_API_SECRET")
if _cloud_name and _api_key and _api_secret:
    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": _cloud_name,
        "API_KEY":    _api_key,
        "API_SECRET": _api_secret,
    }

# ── Wagtail ───────────────────────────────────────────────────────────────────
WAGTAILADMIN_BASE_URL = os.environ.get(
    "WAGTAILADMIN_BASE_URL", "https://your-app.vercel.app"
)

# ── Email (Gmail SMTP) ────────────────────────────────────────────────────────
EMAIL_BACKEND    = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST       = "smtp.gmail.com"
EMAIL_PORT       = 587
EMAIL_USE_TLS    = True
EMAIL_HOST_USER  = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL  = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

try:
    from .local import *
except ImportError:
    pass
