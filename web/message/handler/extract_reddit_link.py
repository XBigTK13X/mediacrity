from django.core.exceptions import ObjectDoesNotExist
from media.models import Source, SourceKind, Storage, StorageKind, Job, JobStatus, Album
from extract import reddit
from common import file_cache,orm
import message.write
import datetime, json

def handle(job, payload):
        source_id = payload['source_id']
        source = Source.objects.get(id=source_id)
        job.source_id = source
        print(f"Tracking progress in job {job.id} for source {source_id}")
        orm.job_log(job,f"Beginning extract of reddit saves for {source.name}.")
