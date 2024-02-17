"""
Django settings for localroyalrent project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from website.dynamic_schedule import dynamic_schedule
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f+*9f8_b(j^%2!q9gk2s-xsy9^72t*=#a3w(7cn0j8o9yez*i*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # "django.contrib.gis",
    # 'leaflet',
    'main_app',
    'website',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_countries',
    'widget_tweaks',
    "rest_framework",
    "django_filters",
    "djstripe",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'localroyalrent.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'website.context_processor.cities',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_USER_MODEL = 'main_app.CustomUser'
ACCOUNT_FORMS = {
    'signup': 'main_app.forms.RentalCompanyRegistrationView',
}

WSGI_APPLICATION = 'localroyalrent.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'localrentdb',
        'USER': 'postgres',
        'PASSWORD': 'Bhimber786---',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'website/locale'),
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ACCOUNT_EMAIL_VERIFICATION = 'None'
LOGIN_REDIRECT_URL = '/'

# STRIPE SETTING
# STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY", "<your secret key>")
# STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY", "sk_test_51KZDfdAKoNfiT1qbdxqcZCEtvY1Oxa6Ot01Kqr7q6zYsyuJhUUhWFcuk6GeivTkQQYt9Ismh6eOANtC6a4fQ0glT00TwFonfpm")
# STRIPE_LIVE_MODE = False  # Change to True in production
# DJSTRIPE_WEBHOOK_SECRET = "whsec_xxx"  # Get it from the section in the Stripe dashboard where you added the webhook endpoint
# DJSTRIPE_USE_NATIVE_JSONFIELD = True  # We recommend setting to True for new installations
# DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"

#DEPLOYMENT SETTING
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_REFERRER_POLICY = "strict-origin"

STRIPE_PUBLIC_KEY = 'pk_test_51OL3NULW8TXmjJXuYR63Zpefw9PpQCFfwhZkMhsDMKBlaXMT421bRotLJ4Zqs63mjnAXArmTYz8aAP7hB5zsjNbA00D8EB9DcB'
STRIPE_SECRET_KEY = 'sk_test_51OL3NULW8TXmjJXuTD4QizPe7nHXyvvGun6zV3FnPHM8RsCtZ378hfarx1lHyCUwsdeS71IaAyUpm6bts8kfYZu700sSal4MEU'
STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY", "<your secret key>")
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY", "sk_test_51OL3NULW8TXmjJXuTD4QizPe7nHXyvvGun6zV3FnPHM8RsCtZ378hfarx1lHyCUwsdeS71IaAyUpm6bts8kfYZu700sSal4MEU")
STRIPE_LIVE_MODE = False  # Change to True in production
DJSTRIPE_WEBHOOK_SECRET = "whsec_xxx"  # Get it from the section in the Stripe dashboard where you added the webhook endpoint
DJSTRIPE_USE_NATIVE_JSONFIELD = True  # We recommend setting to True for new installations
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"


TBC_API_KEY = 'V6H7jBcqhu9lXinbldkAHG0cYysXZMMP'


GDAL_LIBRARY_PATH = r'C:\Users\MR LAPTOP\PycharmProjects\localroyalrent\venv\Lib\site-packages\osgeo\gdal304.dll'
GEOS_LIBRARY_PATH = r'C:\Users\MR LAPTOP\PycharmProjects\localroyalrent\venv\Lib\site-packages\osgeo\geos_c.dll'

# Celery Configuration
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'UTC'
# CELERY_BEAT_SCHEDULE = dynamic_schedule

# LEAFLET_CONFIG = {
#     'DEFAULT_CENTER': (0, 0),
#     'DEFAULT_ZOOM': 2,
#     'MIN_ZOOM': 2,
#     'MAX_ZOOM': 18,
#     'PLUGINS': {
#         'geocoder': {
#             'provider': 'google',
#             'view': 'satellite',
#         },
#     },
# }


# Set your commission percentage
COMMISSION_PERCENTAGE = 0.15

