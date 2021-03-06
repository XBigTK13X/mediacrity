from django.core.exceptions import ObjectDoesNotExist
from media.models import *
from extract import reddit
from common import file_cache, orm, ioutil
import message.write
import datetime, json
from web import settings
import subprocess, os
from transform import transcode, thumbnail, metadata

VIDEO_KIND = MediaKind.objects.get(name="video")
ANIMATION_KIND = MediaKind.objects.get(name="animation")
IMAGE_KIND = MediaKind.objects.get(name="image")

# os.walk was missing recursion into some ripme directories.
# This method ensures all files are found
def search(results, path):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = ioutil.path(root, file)
            results[file_path] = file_path
        for dir in dirs:
            results = search(results, ioutil.path(root, dir))
    return results

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
        file_lookup = search({}, source.content_path)
        files = list(file_lookup.keys())
        files.sort()
        if len(files) == 0:
            orm.job_log(job, f"No files found at {source.content_path}")
        else:
            for file in files:
                extract_path = file
                extension = ioutil.extension(extract_path)
                if extension in settings.TRANSFORM_IGNORE_EXTENTIONS:
                    orm.job_log(job,f"Ignoring file {extract_path}")
                    continue
                content_hash = file_cache.content_hash(extract_path)
                orm.job_log(job,f"Converting file {extract_path} with hash {content_hash}")
                media = None
                try:
                    media = Media.objects.get(content_hash=content_hash, source_id=source_id)
                    orm.job_log(job, f"Updating existing media {media.id} - {media.content_hash} - {source_id}")
                except ObjectDoesNotExist:
                    media = Media.objects.create(
                        source_id=source.id,
                        content_hash=content_hash
                    )
                    orm.job_log(job, f"Created new media for content {content_hash} under source {source_id}")
                if media.extract_path != extract_path:
                    media.extract_path = extract_path
                    media.save()
                if transcode.is_video(extract_path):
                    transform_dir = orm.transform_dir(source.kind.name, source.legacy_v1_id)
                    transform_path = ioutil.path(transform_dir, f"{media.content_hash}.mp4")
                    transform_cached = ioutil.cached(transform_path)
                    orm.job_log(job, f"Was the transform cached for {transform_path}? {transform_cached}")
                    if not transform_cached:
                        media.transform_path = transcode.video(job, media.extract_path, transform_path)
                    else:
                        media.transform_path = transform_path
                    media.save()
                elif transcode.is_image(extract_path):
                    transform_dir = orm.transform_dir(source.kind.name, source.legacy_v1_id)
                    transform_path = ioutil.path(transform_dir, f"{media.content_hash}.jpg")
                    transform_cached = ioutil.cached(transform_path)
                    orm.job_log(job, f"Was the transform cached for {transform_path}? {transform_cached}")
                    if not transform_cached:
                        media.transform_path = transcode.image(job, media.extract_path, transform_path)
                    else:
                        media.transform_path = transform_path
                    media.save()
                if media.extension == "mp4":
                    media.kind = VIDEO_KIND
                elif media.extension == "webm":
                    media.kind = ANIMATION_KIND
                else:
                    media.kind = IMAGE_KIND
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
