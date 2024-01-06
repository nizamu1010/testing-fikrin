
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-rsucr37x(waygjv&w@+jdp!qlu$$d&d$%@5$gbho$(#u3765)2"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['16.171.140.206', 'fikr.in', 'www.fikr.in', '*']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "FknAp",
    "pwa",
    "fcm_django",
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

ROOT_URLCONF = "FknPj.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = "FknPj.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'fkrndb',
#         'USER': 'postgres',
#         'PASSWORD': 'FnKi@10$NiFk',
#         'HOST': 'localhost',  # or the database server host
#         'PORT': '5432',       # the default port for PostgreSQL
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'FknAp.CustomUser'


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


LOGIN_URL = '/accounts/login/'


# ----------------------------------------------------------------------------------------------------------------



# Define PWA settings
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static/js', 'serviceworker.js')

PWA_APP_NAME = 'Fikrin'
# PWA_APP_DESCRIPTION = "🌟 Welcome to Fikrin, an innovative social platform that promises to redefine your reading experience and ignite your passion for literature. 📚✨"
PWA_APP_THEME_COLOR = '#ffffff'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'portrait'
# PWA_APP_ORIENTATION = 'landscape'  # Commented out one orientation
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'


PWA_APP_ICONS = [
    {
        'src': '/static/img/fkr.png',
        'sizes': '160x160'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/img/fkr.png',
        'sizes': '160x160'
    }
]

PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'

# Define FCM settings
FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": "AAAAkV-gc5c:APA91bF4PJPVDpihuGhCzMljtG1RjI-ZOn0xLr8UscqsQGw6nPZ7mDz9ttTeXZUj6LHjT1fdwkhUEdXYa22jR-dJ-OEr3_MDwTbVNUsTB8Wofl8H8ApQ8Sbo8dkEnFNTR5OXeOIrtKTS",
    "DEFAULT_FIREBASE_APP": None,
    "APP_VERBOSE_NAME": "Fikrin-Thoughts",
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": True,
    "TOPIC_PREFIX": None,
    "ANDRO_ID_MESSAGE_KEY": "data_message",
    "APNS_ID_MESSAGE_KEY": "data_message",
    "CUSTOM_PAYLOAD": {
        "key1": "value1",
        "key2": "value2",
        # Add more custom data here
    },
    "ANDROID_NOTIFICATION_CHANNELS": {
        "channel_id_1": {
            "name": "Channel 1",
            "importance": "high",
            "vibration_pattern": [100, 200, 300],
        },
        # Define more channels as needed
    },
    "MESSAGE_TTL_SECONDS": 3600,  # 1 hour (adjust as needed)
    "ERRORS_KEEP_UNSENT": True,
    "ERRORS_MAX_AGE": 604800,  # Maximum age of unsent messages (adjust as needed)
}
