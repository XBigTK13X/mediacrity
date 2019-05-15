import message.connect

def watch(callback):
    connection, channel = message.connect.create('mediacrity')
    channel.basic_consume(queue='mediacrity', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages.')
    channel.start_consuming()
