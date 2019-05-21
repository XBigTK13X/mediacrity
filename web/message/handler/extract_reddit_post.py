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
    orm.job_log(job,f"Beginning extract of URL using reddit post downloader for {source.name}.")

    extract_dir = orm.extract_dir('reddit', source.legacy_v1_id)
    source.content_path = extract_dir
    source.save()

    orm.job_log(job, f"Downloading image from link {source.origin_path}")
    image = reddit.get_media(source)
    media = None
    try:
        media = Media.objects.get(content_hash=image['content_hash'], source_id=source_id)
        orm.job_log(job, f"Updating existing media {media.id} - {media.content_hash} - {source_id}")
    except ObjectDoesNotExist:
        media = Media.objects.create(
            source_id=source.id,
            content_hash=image['content_hash']
        )
        orm.job_log(job, f"Creating new media {media.content_hash} - {source_id}")
    media.origin_path=source.origin_path
    media.extract_path=image['extract_path']
    media.save()

    orm.job_log(job, "Completed reddit post download")
    job_status = JobStatus.objects.get(name="success")
    job.status_id = job_status.id
    job.save()
    child_job_id = message.write.send(
        source_id=source.id,
        handler='transform-media'
    )
    orm.job_log(job, f"Created child job {child_job_id}")
