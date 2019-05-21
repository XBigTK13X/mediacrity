from django.core.exceptions import ObjectDoesNotExist
from media.models import *
from extract import reddit
from common import file_cache, orm, ioutil
import message.write
import datetime, json
from web import settings
import subprocess, os
from transform import transcode, thumbnail

def handle(job, payload):
    source_id = payload['source_id']
    source = Source.objects.select_related().get(id=source_id)
    job.source_id = source
    print(f"Tracking progress in job {job.id} for source {source_id}")
    orm.job_log(job,f"Beginning media transform for {source.legacy_v1_id} - {source.name}.")

    if not os.path.exists(source.content_path):
        error = f"Unable to process source, because {source.content_path} does not exist!"
        orm.job_log(job, error)
        job_status = JobStatus.objects.get(name="failed")
        job.status_id = job_status.id
        job.save()
        raise Exception(error)
    else:
        for root, dirs, files in os.walk(source.content_path):
            if len(files) == 0:
                orm.job_log(job, f"No files found at {source.content_path}")
            for file in files:
                extract_path = ioutil.path(root, file)
                extension = ioutil.extension(extract_path)
                if extension in settings.TRANSFORM_IGNORE_EXTENTIONS:
                    orm.job_log(job,f"Ignoring file {extract_path}")
                    continue
                content_hash = file_cache.content_hash(extract_path)
                orm.job_log(job,f"Converting file {root}/{file} with hash {content_hash}")
                media = None
                try:
                    media = Media.objects.get(content_hash=content_hash, source_id=source_id)
                    orm.job_log(job, f"Updating existing media {media.id} - {media.content_hash} - {source_id}")
                except ObjectDoesNotExist:
                    media = Media.objects.create(
                        source_id=source.id,
                        content_hash=content_hash
                    )
                    orm.job_log(job, f"Creating new media {content_hash} - {source_id}")
                if media.extract_path != extract_path:
                    media.extract_path = extract_path
                    media.save()
                if transcode.is_video(media.extract_path) and ioutil.extension(media.extract_path) != 'webm':
                    transform_dir = orm.transform_dir(source.kind.name, source.legacy_v1_id)
                    transform_path = ioutil.path(transform_dir, f"{media.content_hash}.mp4")
                    if not ioutil.cached(transform_path):
                        media.transform_path = transcode.video(job, media.extract_path, transform_path)
                        media.save()
                media.byte_size = os.path.getsize(media.server_path)
                determine_order(media, file)
                media.save()
                thumbnail.generate(job, source, media)

    job_status = JobStatus.objects.get(name="success")
    job.status_id = job_status.id
    job.save()

def determine_order(media, file):
    sort_index = 0
    if '-' in file:
        first_part = file.split('-')[0]
        try:
            sort_index = int(first_part)
            media.sort_order = sort_index
        except:
            swallow = True
    if '_' in file:
        first_part = file.split('_')[0]
        try:
            sort_index = int(first_part)
            media.sort_order = sort_index
        except:
            swallow = True
