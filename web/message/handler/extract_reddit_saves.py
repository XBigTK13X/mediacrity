import json

from django.core.exceptions import ObjectDoesNotExist

from media.models import Source, SourceKind, Storage, StorageKind, Job, JobStatus, Album

from extract import reddit

from common import file_cache,orm

import datetime

def handle(payload):
    job_id = payload['job_id']
    source_id = payload['source_id']
    source = Source.objects.get(id=source_id)
    job = Job.objects.get(id=job_id)
    job.logs = "";
    job.save()
    job_status = JobStatus.objects.get(name="running")
    job.status_id = job_status.id
    print(f"Tracking progress in job {job_id} for source {source_id}")
    orm.job_log(job,f"Beginning extract of reddit saves for {source.name}.")
    album_slug = f"reddit-saves-{source.name}-generated"
    album = None
    try:
        album = Album.objects.get(name=album_slug)
        orm.job_log(job, f"Updating existing reddit saves album {album_slug}")
    except ObjectDoesNotExist:
        album = Album.objects.create(name=album_slug)
        orm.job_log(job, f"Creating new reddit saves album {album_slug}")
    saves = reddit.get_saves(source)
    orm.job_log(job, f"Retrieved {len(saves)} saves for {source.name}")
    for key, save in saves.items():
        save_slug = save['reddit_link']
        save_hash = file_cache.hash(save_slug)
        save_title = save['reddit_link']
        if 'title' in save:
            save_title = save['title']
        save_source = None
        save_created = datetime.datetime.fromtimestamp(save['created'])
        try:
            save_source = Source.objects.get(legacy_v1_id=save_hash)
            orm.job_log(job, f"Updating existing source {save_source.id} for reddit save {save_title}")
            save_source.title = save_title
            save_source.created = save_created
            save_source.save()
        except ObjectDoesNotExist:
            save_source = Source.objects.create(
                legacy_v1_id=save_hash,
                name=save_title,
                kind_id=source.kind_id,
                description="Auto generated source based on reddit saves.",
                legacy_order=save['sort_index'],
                created=save_created
            )
            orm.job_log(job, f"Created a new source {save_source.id} for reddit save {save_title}")
        album.sources.add(save_source)
    orm.job_log(job, f"Ensuring all generated sources are in the album {album_slug}")
    album.save()
    job_status = JobStatus.objects.get(name="success")
    job.status_id = job_status.id
    job.save()
    print(f"Finished updating source {source_id}")
