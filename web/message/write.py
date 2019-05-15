import message.connect
import json

def send(payload):
    connection, channel = message.connect.create('mediacrity')
    channel.basic_publish(exchange='', routing_key='mediacrity', body=json.dumps(payload))
    connection.close()
