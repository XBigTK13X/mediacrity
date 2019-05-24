import os
import django
from django.conf import settings
from web import settings as config
from common import ioutil

CONNECTED=False

def job_log(job,message):
    job.logs = job.logs + '\n' + message
    job.save()

def job_fail(result, job, error):
    from media.models import JobStatus
    if result != 0:
        job_status = JobStatus.objects.get(name="failed")
        job.status_id = job_status.id
        job.save()
        job_log(job, error)
        raise Exception(error)

def extract_dir(subdir, hash):
    from media.models import Storage
    storage = Storage.objects.first()
    path = f"{storage.path}/{config.EXTRACT_DIR}/{subdir}/{hash}"
    path = ioutil.path_compact(path)
    ioutil.mkdir(path)
    return path

def transform_dir(subdir, hash):
    from media.models import Storage
    storage = Storage.objects.first()
    path = f"{storage.path}/{config.TRANSFORM_DIR}/{subdir}/{hash}"
    path = ioutil.path_compact(path)
    ioutil.mkdir(path)
    return path

def connect():
    global CONNECTED
    if not CONNECTED:
        settings.configure(
            DATABASES=config.DATABASES,
            INSTALLED_APPS = config.INSTALLED_APPS
        )
        django.setup()
        CONNECTED = True
