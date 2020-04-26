from django.core.exceptions import ObjectDoesNotExist
from media.models import *
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
    dir_path = source.origin_path
    orm.job_log(job,f"Beginning extract of file system dir for {dir_path}.")
    orm.job_log(job, f"dirs: {dir_path}")
    dir_slug = f"file-system-dir-{dir_path}"
    dir_hash = file_cache.hash(dir_slug)
    source.legacy_v1_id = dir_hash
    source.name = source.name
    source.description="Auto generated source based on file system root."
    source.origin_path = dir_path
    source.content_path = dir_path
    source.save()

    job_status = JobStatus.objects.get(name="success")
    job.status_id = job_status.id
    job.save()
    child_job_id = message.write.send(
        source_id=source.id,
        handler='transform-media'
    )
    orm.job_log(job, f"Created child job {child_job_id}")
