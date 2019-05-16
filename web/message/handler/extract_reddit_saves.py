from django.core.exceptions import ObjectDoesNotExist
from media.models import Source, SourceKind, Storage, StorageKind, Job, JobStatus, Album
import message.write
from extract import reddit
from common import file_cache,orm
import datetime, json

default_source_kind = SourceKind.objects.get(name="ripme")

def handle(job, payload):
    source_id = payload['source_id']
    source = Source.objects.get(id=source_id)
    job.source_id = source
    print(f"Tracking progress in job {job.id} for source {source_id}")
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
    orm.job_log(job, f"Retrieved saves for {source.name}")
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
        except ObjectDoesNotExist:
            save_source = Source.objects.create()
            orm.job_log(job, f"Created a new source {save_source.id} for reddit save {save_title}")
        save_source.title = save_title
        save_source.created = save_created
        save_source.origin_path = save['reddit_link']
        reddit_link = f"https://old.reddit.com{save['reddit_link']}"
        if 'internet_link' in save:
            save_source.origin_path = save['internet_link']
            save_source.discussion_path = reddit_link
        else:
            save_source.origin_path = reddit_link
            save_source.discussion_path = reddit_link

        save_source.legacy_order = save['sort_index']
        save_source.kind_id = default_source_kind.id
        save_source.legacy_v1_id = save_hash
        save_source.name = save_title
        save_source.description="Auto generated source based on reddit saves."
        save_source.save()
        message.write.send(
            source_id=save_source.id,
            handler='extract-ripme-link'
        )
        album.sources.add(save_source)
    orm.job_log(job, f"Ensuring all generated sources are in the album {album_slug}")
    album.save()
    job_status = JobStatus.objects.get(name="success")
    job.status_id = job_status.id
    job.save()
    print(f"Finished updating source {source_id}")
