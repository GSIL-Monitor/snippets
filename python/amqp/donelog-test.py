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
    # 'content_type': 'application/json',
    # 'content_encoding': '',
    'headers': {
        'X-QK-CONTENT-TYPE': 'json',
    }
}


## subtask 256
body = json.dumps({
    'id': 1,
    'user_id': 200,
    'task_id': 256,
    'task_type': 1,
    'discount': 2.34,
    'univalent': 4,
    'integral': 1,
    'shifu_bonus': 0.2,
    'shiye_bonus': 0.1,
    'create_time': '2018-07-20 14:24:00',
})

prop = pika.BasicProperties(**properties)

chan.basic_publish(
    'tigger.topic',
    'user_task_done_log',
    body,
    prop,
)


## zstask
body = json.dumps({
    'id': 1,
    'user_id': 200,
    'task_id': 512,
    'task_type': 2,
    'discount': 2.34,
    'univalent': 4,
    'integral': 1,
    'shifu_bonus': 0.2,
    'shiye_bonus': 0.1,
    'create_time': '2018-07-20 14:24:00',
})

prop = pika.BasicProperties(**properties)

chan.basic_publish(
    'tigger.topic',
    'user_task_done_log',
    body,
    prop,
)
