from pathlib import Path
from datetime import timedelta
import environ
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True

# SSL CONFIG 
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#SECURE_SSL_REDIRECT     = True
#SECURE_SSL_CERTIFICATE  = '/etc/letsencrypt/live/pricing.infinitytech.dev/fullchain.pem'
#SECURE_SSL_KEY          = '/etc/letsencrypt/live/pricing.infinitytech.dev/privkey.pem'

# Number Format
USE_DECIMAL_SEPARATOR  = True
USE_THOUSAND_SEPARATOR = True
DECIMAL_SEPARATOR      = ","
THOUSAND_SEPARATOR     = "."

# Application definition
BASE_APPS        = ['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions',
                    'django.contrib.messages','django.contrib.staticfiles','django.contrib.humanize']

LOCAL_APPS       = ['apps.base', 'apps.authentication', 'apps.misc']

THIRD_PARTY_APPS = ['rest_framework', 'corsheaders', 'gunicorn', 'django_seed', 'django_filters', 'django_crontab']

INSTALLED_APPS   = BASE_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'apps.base.middlewares.authMiddleware.AuthMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['apps.base.templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'core.wsgi.application'

if DEBUG:
    DATABASES = {
            'default': {
                'ENGINE': env('ENGINE'),
                'NAME': env('DB_NAME'),
                'USER': env('TEST_DB_USER'),
                'PASSWORD': env('TEST_DB_PASSWORD'),
                'HOST': env('TEST_DB_HOST'),
                'PORT': 3306,
                'OPTIONS':{
                    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
                }
            },
        }
else:
    DATABASES = {
            'default': {
                'ENGINE': env('ENGINE'),
                'NAME': env('DB_NAME'),
                'USER': env('DB_USER'),
                'PASSWORD': env('DB_PASSWORD'),
                'HOST': env('DB_HOST'),
                'PORT': 3306,
                'OPTIONS':{
                    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
                }
            },
        }



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE     = 'UTC'

USE_I18N      = True

USE_TZ        = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL  = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Date Format
USE_L10N = True
DATE_INPUT_FORMATS = ['%d-%m-%Y']


# Django Rest Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES'    : [],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'EXCEPTION_HANDLER': 'apps.base.exceptions.custom_exception_handler',
    'PAGE_SIZE': 30,
}


# SMTP settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = f'{env("EMAIL_HOST_PASSWORD")}'

# S3 settings
#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
#AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
#AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
#AWS_REGION = 'us-east-1'
#AWS_QUERYSTRING_AUTH = False