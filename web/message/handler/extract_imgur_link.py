from django.core.exceptions import ObjectDoesNotExist
from media.models import Source, SourceKind, Storage, StorageKind, Job, JobStatus, Album, Media
from extract import reddit
from common import file_cache, orm, ioutil
import message.write
import datetime, json
from web import settings
import subprocess, os
from extract import imgur

def handle(job, payload):
    source_id = payload['source_id']
    source = Source.objects.get(id=source_id)
    job.source_id = source
    print(f"Tracking progress in job {job.id} for source {source_id}")
    orm.job_log(job,f"Beginning extract of URL using imgur downloader for {source.name}.")

    extract_dir = orm.extract_dir('imgur', source.legacy_v1_id)
    source.content_path = extract_dir
    source.save()

    orm.job_log(job, f"Downloading images from link {source.origin_path}")
    images = imgur.download(source)
    for image in images:
        orm.job_log(job, f"Storing image {image['origin_path']} at {image['extract_path']}")
        Media.objects.create(
            source_id=source.id,
            order=image['sort_index'],
            origin_path=image['origin_path'],
            extract_path=image['extract_path'],
            content_hash=image['content_hash']
        )

    orm.job_log(job, "Completed imgur download")
    job_status = JobStatus.objects.get(name="success")
    job.status_id = job_status.id
    job.save()
