import orm_setup

orm_setup.connect()

import message.connect

import json

from django.core.exceptions import ObjectDoesNotExist

from media.models import Source, SourceKind, Storage, StorageKind, Job, JobStatus, Album

from extract import reddit

from common import file_cache

import datetime

def log(job, message):
    job.logs += message + '\n'
    job.save()

def extract_callback(channel, method, properties, body):
    payload = json.loads(body)
    job_id = payload['job_id']
    source_id = payload['source_id']
    source = Source.objects.get(id=source_id)
    job = Job.objects.get(id=job_id)
    job.logs = "";
    job.save()
    job_status = JobStatus.objects.get(name="running")
    job.status_id = job_status.id
    print(f"Tracking progress in job {job_id} for source {source_id}")
    log(job,f"Beginning extract of reddit saves for {source.name}.")
    album_slug = f"reddit-saves-{source.name}-generated"
    album = None
    try:
        album = Album.objects.get(name=album_slug)
        log(job, f"Updating existing reddit saves album")
    except ObjectDoesNotExist:
        album = Album.objects.create(name=album_slug)
        log(job, f"Creating new reddit saves album")
    saves = reddit.get_saves(source)
    log(job, f"Retrieved {len(saves)} saves for {source.name}")
    for key, save in saves.items():
        save_slug = save['reddit_link']
        save_hash = file_cache.hash(save_slug)
        save_title = save['reddit_link']
        if hasattr(save,'title'):
            save_title = save['title']
        save_source = None
        save_created = datetime.datetime.fromtimestamp(save['created'])
        print(save_created)
        try:
            save_source = Source.objects.get(legacy_v1_id=save_hash)
            log(job, f"Updating existing source {save_source.id} for reddit save {save_title}")
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
            log(job, f"Created a new source {save_source.id} for reddit save {save_title}")
        album.sources.add(save_source)
    log(job, "Ensuring all generated sources are in the album")
    album.save()
    job_status = JobStatus.objects.get(name="success")
    job.status_id = job_status.id
    job.save()
    print(f"Finished updating source {source_id}")

connection, channel = message.connect.create('extract')
channel.basic_consume(queue='extract', on_message_callback=extract_callback, auto_ack=True)

print('Waiting for messages.')
channel.start_consuming()
