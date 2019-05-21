import traceback
from common import orm
orm.connect()

import json
import message.read
from message.handler import extract_file_system_root
from message.handler import extract_file_system_directory
from message.handler import extract_reddit_saves
from message.handler import extract_imgur_link
from message.handler import extract_ripme_link
from message.handler import extract_youtube_dl_link
from message.handler import transform_media
from message.handler import extract_reddit_post
from media.models import Job, JobStatus

default_status = JobStatus.objects.get(name="running")
failed_status = JobStatus.objects.get(name="failed")

def callback(channel, method, properties, body):
    print(f"Message received {body}. {message.read.count()} messages remain in queue.")
    payload = json.loads(body)
    errors = False
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
            elif handler == 'extract-file-system-root':
                extract_file_system_root.handle(job, payload)
            elif handler == 'extract-file-system-directory':
                extract_file_system_directory.handle(job, payload)
            elif handler == 'extract-imgur-link':
                extract_imgur_link.handle(job, payload)
            elif handler == 'extract-reddit-post':
                extract_reddit_post.handle(job, payload)
            elif handler == 'extract-ripme-link':
                extract_ripme_link.handle(job, payload)
            elif handler == 'extract-youtube-dl-link':
                extract_youtube_dl_link.handle(job, payload)
            elif handler == 'transform-media':
                transform_media.handle(job, payload)
            else:
                print(f"Unknown handler [{handler}]")
        except Exception as e:
            errors = True
            job.status_id = failed_status.id
            orm.job_log(job, f"{e}\n {traceback.format_exc()}")
    else:
        print(f"No handler provided")
    print(f"Message processed with{'' if errors else ' no'} errors")
    channel.basic_ack(delivery_tag=method.delivery_tag)

while True:
    try:
        message.read.watch(callback)
    except Exception as e:
        print(f"An exception occurred while processing messages.\n{traceback.format_exc()}")
