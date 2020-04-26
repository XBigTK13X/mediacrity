from django.core.exceptions import ObjectDoesNotExist
from media.models import *
import message.write
from extract import reddit
from common import file_cache, orm, ioutil
import datetime, json, os

directory_source_kind = SourceKind.objects.get(name="file-system-directory")


def handle(job, payload):
    source_id = payload['source_id']
    source = Source.objects.get(id=source_id)
    job.source_id = source
    print(f"Tracking progress in job {job.id} for source {source_id}")
    orm.job_log(job,f"Beginning extract of file system for {source.name}.")
    album_slug = f"file-system-{source.name}-generated"
    album = None
    try:
        album = Album.objects.get(name=album_slug)
        orm.job_log(job, f"Updating existing file system album {album_slug}")
    except ObjectDoesNotExist:
        album = Album.objects.create(name=album_slug)
        orm.job_log(job, f"Creating newfile system album {album_slug}")

    source.legacy_v1_id = file_cache.hash(album_slug)
    source.save()

    album.generated_by_source_v1_id = source.legacy_v1_id
    album.save()

    for root, dirs, files in os.walk(source.origin_path):
        for dir in dirs:
            dir_path = ioutil.path(root,dir)
            orm.job_log(job, f"dirs: {dir_path}")
            dir_slug = f"file-system-dir-{dir_path}"
            dir_hash = file_cache.hash(dir_slug)
            dir_source = None
            try:
                dir_source = Source.objects.get(legacy_v1_id=dir_hash)
                orm.job_log(job, f"Updating existing source {dir_source.id} for dir {dir_path}")
            except ObjectDoesNotExist:
                dir_source = Source.objects.create(kind_id=directory_source_kind.id)
                orm.job_log(job, f"Created a new source {dir_source.id} for dir {dir_path}")

            dir_source.legacy_v1_id = dir_hash
            dir_source.name = dir_path
            dir_source.description="Auto generated source based on file system root."
            dir_source.origin_path = dir_path
            dir_source.content_path = dir_path
            dir_source.save()

            message.write.send(
                source_id=dir_source.id,
                handler='extract-file-system-directory'
            )
            album.sources.add(dir_source)
    orm.job_log(job, f"Ensuring all generated sources are in the album {album_slug}")
    album.save()
    job_status = JobStatus.objects.get(name="success")
    job.status_id = job_status.id
    job.save()
    print(f"Finished updating source {source_id}")
