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

# ── Database ──────────────────────────────────────────────────────────────────
database_url = os.environ.get("DATABASE_URL")
if database_url:
    DATABASES = {
        "default": dj_database_url.parse(
            database_url,
            conn_max_age=600,
        )
    }

# ── Static files (WhiteNoise) ─────────────────────────────────────────────────
# Insert WhiteNoise right after SecurityMiddleware
_middleware = list(MIDDLEWARE)
_sec_idx = _middleware.index("django.middleware.security.SecurityMiddleware")
_middleware.insert(_sec_idx + 1, "whitenoise.middleware.WhiteNoiseMiddleware")
MIDDLEWARE = _middleware

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

STATIC_ROOT = BASE_DIR / "staticfiles"
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

try:
    from .local import *
except ImportError:
    pass
