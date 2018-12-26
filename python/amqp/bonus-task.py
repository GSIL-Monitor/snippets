# -*- coding: utf-8 -*-
import json
import time
import uuid

import pika

conn = pika.BlockingConnection()
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
routing_key = 'bonus_task.action.start'
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
