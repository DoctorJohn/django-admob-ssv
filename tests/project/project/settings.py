from datetime import timedelta

DEBUG = True

SECRET_KEY = "fake-key"

ALLOWED_HOSTS = ["*"]

ROOT_URLCONF = "tests.project.project.urls"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite"}}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

USE_TZ = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "tests.project.verifications",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    },
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

STATIC_URL = "static/"

# Optional advanced settings
ADMOB_SSV_KEYS_SERVER_URL = "https://www.gstatic.com/admob/reward/verifier-keys.json"
ADMOB_SSV_KEYS_CACHE_TIMEOUT = timedelta(days=1)
ADMOB_SSV_KEYS_CACHE_KEY = "admob_ssv.public_keys"
