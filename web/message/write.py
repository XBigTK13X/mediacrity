import message.connect
import json
from media.models import Job, JobStatus
from web import settings
import pika

DEFAULT_STATUS = JobStatus.objects.get(name="pending")
PERSISTENT_DELIVERY_MODE=2

def send(source_id=None, media_id=None, log_entry="Starting the job", handler=None):
    if handler == None:
        raise Exception("handler is required when calling message.send()")
    payload = {
        'handler': handler,
        'log_entry': log_entry
    }
    if media_id != None:
        payload['media_id'] = media_id
    if source_id != None:
        payload['source_id'] = source_id
    job = Job.objects.create(status_id=DEFAULT_STATUS.id)
    payload['job_id'] = job.id
    connection, channel = message.connect.create()
    channel.basic_publish(
        exchange='',
        routing_key=settings.MESSAGE_QUEUE,
        body=json.dumps(payload),
        properties=pika.BasicProperties(
            delivery_mode=PERSISTENT_DELIVERY_MODE,
        )
    )
    connection.close()
    return job.id
