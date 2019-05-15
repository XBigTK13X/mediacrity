import os
import django
from django.conf import settings

def job_log(job,message):
    job.logs += message + '\n'
    job.save()

def connect():
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ.get('MEDIACRITY_DB_NAME'),
                'USER': os.environ.get('MEDIACRITY_DB_USER'),
                'PASSWORD': os.environ.get('MEDIACRITY_DB_PASSWORD'),
                'HOST': '0.0.0.0',
                'PORT': '5432'
            }
        },
        INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'media.apps.MediaConfig'
        ]
    )
    django.setup()
