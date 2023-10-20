import os
import sys
from pathlib import Path

import environ
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()

ENV = env.str("ENV", default="local")

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)

if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    settings_module = env.str("DJANGO_SETTINGS_MODULE")
    if settings_module == "config.settings.production" and (BASE_DIR / ".env").exists():
        env.read_env(str(BASE_DIR / ".env"))
    elif (
        settings_module == "config.settings.test" and (BASE_DIR / ".env.test").exists()
    ):
        env.read_env(str(BASE_DIR / ".env.test"))
    elif settings_module == "config.settings.local" and (BASE_DIR / ".env").exists():
        env.read_env(str(BASE_DIR / ".env"))
    else:
        raise RuntimeError(
            f"Cannot find .env file for DJANGO_SETTINGS_MODULE={settings_module}"
        )

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG", False)
LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Europe/London"
USE_I18N = True
USE_L10N = True
USE_TZ = True
WSGI_APPLICATION = "config.wsgi.application"

# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# DB BACKUP
# ------------------------------------------------------------------------------
DBBACKUP_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
DBBACKUP_STORAGE_OPTIONS = {
    "bucket_name": env.str("GOOGLE_DB_BACKUP_BUCKET_NAME", default=""),
    "project_id": env.str("GOOGLE_STORAGE_PROJECT_ID", default=""),
    "blob_chunk_size": 1024 * 1024,
}

# CELERY
# ------------------------------------------------------------------------------
CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", default="redis://localhost:6379")
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE


# URLS
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"

# APPS
# ------------------------------------------------------------------------------
# add app folder to path
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

INSTALLED_APPS = []

DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
]

THIRD_PARTY_APPS = [
    "anymail",
    "compressor",
    "crispy_forms",
    "crispy_tailwind",
    "dbbackup",
    "django_celery_results",
    "django_filters",
    "tailwind",
]

LOCAL_APPS = [
    "apps.core",
    "apps.dashboard",
    "apps.users",
    "theme",
]

INSTALLED_APPS.extend(DJANGO_APPS)
INSTALLED_APPS.extend(THIRD_PARTY_APPS)
INSTALLED_APPS.extend(LOCAL_APPS)

# PASSWORDS
# ------------------------------------------------------------------------------
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "dashboard:home"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url

AUTH_USER_MODEL = "users.User"

# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# TEMPLATES
# ------------------------------------------------------------------------------
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
                "apps.core.context_processors.site",
                "django.template.context_processors.i18n",
            ],
        },
    },
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# STATIC FILES
# ------------------------------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = str(BASE_DIR / "staticfiles")

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # other finders
    "compressor.finders.CompressorFinder",
)

# COMPRESSOR
COMPRESS_ENABLED = not DEBUG
COMPRESS_CSS_HASHING_METHOD = "content"
COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ],
    "js": [
        "compressor.filters.jsmin.JSMinFilter",
    ],
}

HTML_MINIFY = True

# MEDIA
# ------------------------------------------------------------------------------
MEDIA_ROOT = str(BASE_DIR / "media")
MEDIA_URL = "/media/"


# TRANSLATIONS
# ------------------------------------------------------------------------------
LOCALE_PATHS = [BASE_DIR / "locale"]

LANGUAGES = (("en", _("English")),)

# EMAIL
# ------------------------------------------------------------------------------
ANYMAIL = {
    "SENDGRID_API_KEY": env.str("SENDGRID_API_KEY"),
}

EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="anymail.backends.sendgrid.EmailBackend",
)

DEFAULT_FROM_EMAIL = env.str("EMAIL_FROM_ADDRESS")
SERVER_EMAIL = env.str("EMAIL_FROM_ADDRESS")

EMAIL_TIMEOUT = 5
EMAIL_HOST = env("EMAIL_HOST", default="localhost")
EMAIL_PORT = env("EMAIL_PORT", default=25)

# ADMIN
# ------------------------------------------------------------------------------
ADMINS = [
    ("Howie Weiner", "hello@builtbyhowie.co.uk"),
]
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

TAILWIND_APP_NAME = "theme"

# CUSTOM
# ------------------------------------------------------------------------------
NEW_USER_PASSWORD = env("NEW_USER_PASSWORD", default="changeme")
SITE_ADDRESS = env("SITE_ADDRESS")
