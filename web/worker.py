from common import orm
orm.connect()

import json
import message.read
from message.handler import extract_reddit_saves, extract_imgur_link, extract_ripme_link, transform_media
from media.models import Job, JobStatus

default_status = JobStatus.objects.get(name="running")
failed_status = JobStatus.objects.get(name="failed")

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
        try:
            handler = payload['handler']
            if handler == 'extract-reddit-saves':
                extract_reddit_saves.handle(job, payload)
            elif handler == 'extract-imgur-link':
                extract_imgur_link.handle(job, payload)
            elif handler == 'extract-ripme-link':
                extract_ripme_link.handle(job, payload)
            elif handler == 'transform-media':
                transform_media.handle(job, payload)
            else:
                print(f"Unknown handler [{handler}]")
        except Exception as e:
            job.status_id = failed_status.id
            orm.job_log(job, f"{e}")
    else:
        print(f"No handler provided")

message.read.watch(callback)
