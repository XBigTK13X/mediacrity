from django.core.exceptions import ObjectDoesNotExist
from media.models import Source, SourceKind, Storage, StorageKind, Job, JobStatus, Album
from extract import reddit
from common import file_cache, orm, ioutil
import message.write
import datetime, json
from web import settings
import subprocess, os

def handle(job, payload):
    source_id = payload['source_id']
    source = Source.objects.get(id=source_id)
    job.source_id = source
    print(f"Tracking progress in job {job.id} for source {source_id}")
    orm.job_log(job,f"Beginning media transform for {source.name}.")

    if not os.path.exists(source.content_path):
        error = f"Unable to process source, because {source.content_path} does not exist!"
        orm.job_log(job, error)
        job_status = JobStatus.objects.get(name="failed")
        job.status_id = job_status.id
        job.save()
        raise Exception(error)
    else:
        for root, dirs, files in os.walk(source.content_path):
            for file in files:
                orm.job_log(job,f"Found file {{file}}")

    job_status = JobStatus.objects.get(name="success")
    job.status_id = job_status.id
    job.save()
