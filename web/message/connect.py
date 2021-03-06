import pika

from web import settings

def create():
    credentials = pika.PlainCredentials(settings.MESSAGE_USER, settings.MESSAGE_PASS)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        settings.MESSAGE_HOST,
        settings.MESSAGE_PORT,
        '/',
        credentials,
        blocked_connection_timeout=None,
        socket_timeout=None,
        stack_timeout=None
    ))
    channel = connection.channel()
    channel.queue_declare(queue=settings.MESSAGE_QUEUE, durable=True)
    return connection, channel
