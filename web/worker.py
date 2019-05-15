import orm_setup

orm_setup.connect()

import queue.connect

import json

from media.models import Source, SourceKind, Storage, StorageKind, Job, JobStatus

def extract_callback(channel, method, properties, body):
    payload = json.loads(body)
    job_id = payload['job_id']
    source_id = payload['source_id']
    source = Source.objects.get(id=source_id)
    job = Job.objects.get(id=job_id)
    job_status = JobStatus.objects.get(name="running")
    job.status_id = job_status.id
    job.logs += f"Beginning extract of reddit saves for {source.name}."
    job.save()

connection, channel = queue.connect.create('extract')
channel.basic_consume(queue='extract', on_message_callback=extract_callback, auto_ack=True)

print('Waiting for messages.')
channel.start_consuming()
