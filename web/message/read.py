import message.connect

from web import settings

def watch(callback):
    connection, channel = message.connect.create()

    channel.basic_qos(
        prefetch_count=1
    )
    channel.basic_consume(
        queue=settings.MESSAGE_QUEUE,
        on_message_callback=callback
    )

    print('Waiting for messages.')
    channel.start_consuming()
