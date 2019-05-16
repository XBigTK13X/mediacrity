import os
import django
from django.conf import settings
from web import settings as config
from common import ioutil

def job_log(job,message):
    job.logs = job.logs + '\n' + message
    job.save()

def job_fail(result, job, error):
    from media.models import JobStatus
    if result != 0:
        job_status = JobStatus.objects.get(name="failed")
        job.status_id = job_status.id
        job.save()
        orm.job_log(job, error)
        raise Exception(error)

def extract_dir(subdir, hash):
    from media.models import Storage
    storage = Storage.objects.first()
    path = f"{storage.path}/{config.EXTRACT_DIR}/{subdir}/{hash}"
    path = ioutil.path_compact(path)
    ioutil.mkdir(path)
    return path

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
