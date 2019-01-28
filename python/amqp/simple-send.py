# -*- coding: utf-8 -*-
import json
import time
import uuid

import pika

p = pika.ConnectionParameters(
    host='127.0.0.1',
    port=5672,
    virtual_host='/')

conn = pika.BlockingConnection(p)
chan = conn.channel()

idfa = str(uuid.uuid4()).upper()

# help(chan.basic_publish)

properties = {
    'content_type': 'application/json',
    'content_encoding': '',
}

prop = pika.BasicProperties(**properties)


o = {
    'task_id': 12897318,
    'user_id': 1289361,
    'start_at': '2018-11-23 15:20:00',
    'timestamp': int(time.time()),
}
# routing_key = 'bonus_task.action.start'
# exchange = 'hebe.topic'
exchange = ''
routing_key = 'celery'
body = json.dumps(o)
_ = chan.basic_publish(
    exchange,
    routing_key,
    body,
    prop,
)
print(_)
