import pika

from web import settings

def create():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=settings.MESSAGE_QUEUE, durable=True)
    return connection, channel
