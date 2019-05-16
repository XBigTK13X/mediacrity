import message.connect
import json
from media.models import Job, JobStatus

default_status = JobStatus.objects.get(name="pending")

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
    job = Job.objects.create(status_id=default_status.id)
    payload['job_id'] = job.id
    connection, channel = message.connect.create('mediacrity')
    channel.basic_publish(exchange='', routing_key='mediacrity', body=json.dumps(payload))
    connection.close()
    return job.id
