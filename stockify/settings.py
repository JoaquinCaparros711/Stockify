"""
Django settings for stockify project.
"""

from pathlib import Path
from datetime import timedelta
import dj_database_url
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta desde variable de entorno
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "insecure-secret-key")

# DEBUG configurable
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Railway genera dominios *.railway.app
ALLOWED_HOSTS = [
    ".railway.app",
    "localhost",
]

# Para CSRF (si usás formularios/cookies)
CSRF_TRUSTED_ORIGINS = [
    "https://*.railway.app",
]

# Apps instaladas
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "control",
    "user_control",
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "rest_framework_simplejwt.token_blacklist",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # para archivos estáticos en prod
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "stockify.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "stockify.wsgi.application"

# Base de datos (Railway inyecta DATABASE_URL automáticamente)
DATABASES = {
    "default": dj_database_url.config(conn_max_age=600)
}

# Validadores de password
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internacionalización
LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Config para servir estáticos comprimidos con WhiteNoise
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Clave primaria por defecto
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

# Usuario custom
AUTH_USER_MODEL = "user_control.Users"

# JWT Config
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://stockify-front-end-production.up.railway.app",  # sin / final
]
CORS_ALLOW_CREDENTIALS = True
