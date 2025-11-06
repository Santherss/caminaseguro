from pathlib import Path
import os
from dotenv import load_dotenv
import mongoengine

# Define the project's base directory.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from a .env file located in the base directory.
load_dotenv(os.path.join(BASE_DIR, ".env"))

# SECRET_KEY: A long, random string used for cryptographic signing (e.g., sessions, password resets).
#             It is critical that this key is kept secret. It is loaded from environment
#             variables for security.
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# DEBUG: A boolean that toggles debug mode.
#        - True: Shows detailed error pages. Useful for development.
#        - False: Hides detailed errors. This is a critical security setting for production.
#        WARNING: Never run a production server with DEBUG = True.
DEBUG = True

# ALLOWED_HOSTS: A list of strings representing the host/domain names that this Django
#                site can serve. This is a security measure to prevent HTTP Host header attacks.
#                It is required when DEBUG is False.
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'ddd.dominio.usuarios',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Points to the root URLconf file, which maps URLs to views.
ROOT_URLCONF = "caminaseguro.urls"

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

WSGI_APPLICATION = "caminaseguro.wsgi.application"

# Mongodb configurations
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
mongoengine.connect(db=DB_NAME, host=MONGO_URI)

# A "dummy" relational database for Django's internal apps
# (like contrib.auth and contrib.sessions) which require a
# SQL database to function.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-es"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# STATIC FILES & DEPLOYMENT SECURITY

# --- Static Files Configuration ---
# URL to use when referring to static files (CSS, JavaScript, Images).
STATIC_URL = "static/"

# --- Deployment Security Options ---
# These settings are critical for a secure production environment.
# They are currently commented out and should be enabled when deploying
# your application over HTTPS/SSL.
# WARNING: Do not enable these until you have correctly configured an SSL certificate.

# SECURE_SSL_REDIRECT = True       # Redirects all HTTP traffic to HTTPS.
# SESSION_COOKIE_SECURE = True     # Ensures the session cookie is only sent over HTTPS.
# CSRF_COOKIE_SECURE = True        # Ensures the CSRF cookie is only sent over HTTPS.

# --- HTTP Strict Transport Security (HSTS) ---
# Tells browsers to only communicate with your site via HTTPS.
# This prevents downgrade attacks. Start with a small value for testing.
# A common production value is 31536000 (1 year).
# SECURE_HSTS_SECONDS = 3600
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
