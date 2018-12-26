# -*- coding: utf-8 -*-
import json
import time
import uuid

import pika

p = pika.ConnectionParameters(
    host='fn1037.ops.gaoshou.me',
    port=5672,
    virtual_host='/')

conn = pika.BlockingConnection(p)
chan = conn.channel()

idfa = str(uuid.uuid4()).upper()

# help(chan.basic_publish)

properties = {
    'content_type': 'application/json',
    'content_encoding': '',
    'headers': {
        'x-delay': 1000,
    }
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
exchange = 'huan.delay.topic'
routing_key = 'pin:create:order.2222222'
body = json.dumps(o)
_ = chan.basic_publish(
    exchange,
    routing_key,
    body,
    prop,
)

print(_)


import sys
sys.exit()


o = {
    'task_id': 12897318,
    'user_id': 1289361,
    'complete_at': '2018-11-23 15:20:10',
    'timestamp': int(time.time()),
}
routing_key = 'bonus_task.action.complete'
body = json.dumps(o)
chan.basic_publish(
    'hebe.topic',
    routing_key,
    body,
    prop,
)

o = {
    'task_id': 12897318,
    'user_id': 1289361,
    'coin': 110,
    'timestamp': int(time.time()),
}
routing_key = 'bonus_task.action.reward'
body = json.dumps(o)
chan.basic_publish(
    'hebe.topic',
    routing_key,
    body,
    prop,
)

o = {
    'task_id': 12897318,
    'user_id': 1289361,
    'timestamp': int(time.time()),
}
routing_key = 'bonus_task.action.giveup'
body = json.dumps(o)
chan.basic_publish(
    'hebe.topic',
    routing_key,
    body,
    prop,
)
o = {
    'task_id': 12897318,
    'user_id': 1289361,
    'timestamp': int(time.time()),
}
routing_key = 'bonus_task.action.expire'
body = json.dumps(o)
chan.basic_publish(
    'hebe.topic',
    routing_key,
    body,
    prop,
)
