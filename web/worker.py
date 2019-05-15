from common import orm

orm.connect()

import json

import message.read
from message.handler import extract_reddit_saves

def callback(channel, method, properties, body):
    print(f"Message received {body}")
    payload = json.loads(body)
    if 'handler' in payload:
        handler = payload['handler']
        if handler == 'extract_reddit_saves':
            extract_reddit_saves.handle(payload)
        else:
            print(f"Unknown handler [{handler}]")
    else:
        print(f"No handler provided")

message.read.watch(callback)
