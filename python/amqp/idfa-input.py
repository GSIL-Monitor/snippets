# -*- coding: utf-8 -*-
import json
import random
import time
import uuid

import pika

conn = pika.BlockingConnection()
chan = conn.channel()

idfa = str(uuid.uuid4()).upper()


# help(chan.basic_publish)

def send(userId, idfa):
    properties = {
        'content_type': 'application/json',
        'content_encoding': '',
    }
    prop = pika.BasicProperties(**properties)
    o = {
        'uid': userId,
        'idfa': idfa,
    }
    routing_key = 'keys.compact_state'
    body = json.dumps(o)

    chan.basic_publish(
        'hera.topic',
        routing_key,
        body,
        prop,
    )


while True:
    userId = random.randint(0, 999999999)
    idfa = str(uuid.uuid4()).upper()
    send(userId, idfa)
    time.sleep(0.01)
