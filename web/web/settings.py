"""
Django settings for web project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('MEDIACRITY_DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('MEDIACRITY_DJANGO_DEBUG')

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'media.apps.MediaConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('MEDIACRITY_DB_NAME'),
        'USER': os.environ.get('MEDIACRITY_DB_USER'),
        'PASSWORD': os.environ.get('MEDIACRITY_DB_PASSWORD'),
        'HOST': os.environ.get('MEDIACRITY_DB_HOST'),
        'PORT': os.environ.get('MEDIACRITY_DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

FILE_UPLOAD_HANDLERS = [
 "django.core.files.uploadhandler.TemporaryFileUploadHandler"
]

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

SCRIPT_DIR = os.environ.get('MEDIACRITY_SCRIPT_DIR')

REDDIT_CLIENT_ID=os.environ.get('MEDIACRITY_REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET=os.environ.get('MEDIACRITY_REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT=os.environ.get('MEDIACRITY_REDDIT_USER_AGENT')
REDDIT_SAVE_READ_LIMIT=1000

TEMP_DIR=os.environ.get('MEDIACRITY_TEMP_DIR')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(TEMP_DIR,'django.log'),
        },
    },
    'loggers': {
        'debug': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

REDDIT_SAVES_DIR=os.path.join(TEMP_DIR,'reddit','saves')

IMGUR_CLIENT_ID=os.environ.get('MEDIACRITY_IMGUR_CLIENT_ID')
IMGUR_CLIENT_SECRET=os.environ.get('MEDIACRITY_IMGUR_CLIENT_SECRET')

FILE_CACHE_ENABLED=True
ENABLE_DEBUG_LOGGING=True
EXTRACT_DIR="mediacrity/01-extract"
TRANSFORM_DIR="mediacrity/02-transform"
LOAD_DIR="mediacrity/03-load"

MESSAGE_QUEUE='mediacrity'

TRANSFORM_IGNORE_EXTENTIONS = [
    "txt",
    "json",
    "py"
]

VIDEO_FORMATS = [
    '3gp',
    'avi',
    'flv',
    'gif',
    'mkv',
    'mov',
    'mp4',
    'mpg',
    'webm',
    'wmv'
]

IMAGE_FORMATS = [
    'png',
    'jpg',
    'jpeg',
    'bmp'
]

SUPPRESS_TRANSCODE_LOGGING=1

MESSAGE_HOST=os.environ.get('MEDIACRITY_MESSAGE_HOST')
MESSAGE_PORT=os.environ.get('MEDIACRITY_MESSAGE_PORT')
MESSAGE_USER=os.environ.get('MEDIACRITY_MESSAGE_USER')
MESSAGE_PASS=os.environ.get('MEDIACRITY_MESSAGE_PASSWORD')

CONTENT_SERVER_HOST=os.environ.get('MEDIACRITY_CONTENT_SERVER_HOST')
CONTENT_SERVER_PORT=os.environ.get('MEDIACRITY_CONTENT_SERVER_PORT')

MEDIA_LIST_PAGE_SIZE=44

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600 # One hour
SESSION_SAVE_EVERY_REQUEST = True
