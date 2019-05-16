from common import orm
orm.connect()

import json
import message.read
from message.handler import extract_reddit_saves, extract_ripme_link
from media.models import Job, JobStatus

default_status = JobStatus.objects.get(name="running")

def callback(channel, method, properties, body):
    print(f"Message received {body}")
    payload = json.loads(body)
    if 'handler' in payload:
        job_id = payload['job_id']
        job = Job.objects.get(id=job_id)
        job.logs = payload['log_entry'];
        job.logs += f"\n{body}"
        job.status_id = default_status.id
        job.save()
        handler = payload['handler']
        if handler == 'extract-reddit-saves':
            extract_reddit_saves.handle(job, payload)
        elif handler == 'extract-ripme-link':
            extract_ripme_link.handle(job, payload)
        else:
            print(f"Unknown handler [{handler}]")
    else:
        print(f"No handler provided")

message.read.watch(callback)
