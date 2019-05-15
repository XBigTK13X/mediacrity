import message.connect
import json

def extract(job_id, source_id):
    payload = {
        'job_id': job_id,
        'source_id': source_id
    }
    connection, channel = message.connect.create('extract')
    channel.basic_publish(exchange='', routing_key='extract', body=json.dumps(payload))
    connection.close()
