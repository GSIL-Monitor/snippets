# -*- coding: utf-8 -*-
import json
import random
import time
import uuid

import pika

conn = pika.BlockingConnection()
chan = conn.channel()

idfa = str(uuid.uuid4()).upper()

body = json.dumps({
    'idfa': idfa,
    'uid': random.randint(10000, 200000),
})

# help(chan.basic_publish)

properties = {
    'content_type': 'application/json',
    'content_encoding': '',
}

prop = pika.BasicProperties(**properties)

chan.basic_publish(
    'hebe.topic',
    'explore_task.idfa_check',
    body,
    prop,
)
