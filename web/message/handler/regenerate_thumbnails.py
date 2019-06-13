from django.core.exceptions import ObjectDoesNotExist
from media.models import *
from extract import reddit
from common import file_cache, orm, ioutil
import message.write
import datetime, json
from web import settings
import subprocess, os
from transform import thumbnail

def handle(job, payload):
    print(f"Tracking progress in job {job.id} for thumbnail regen")
    orm.job_log(job,f"Beginning regeneration of all thumbnails.")

    media_list = Media.objects.select_related().all()
    count = len(media_list)
    orm.job_log(job, f"Regenerating {count} thumbnails")
    for index,media in enumerate(media_list):
        orm.job_log(job, f"Updating thumbnail for media id {media.id} ({index + 1}/{count})")
        thumbnail.generate(job, media.source, media, force=True)

    job_status = JobStatus.objects.get(name="success")
    job.status_id = job_status.id
    job.save()
