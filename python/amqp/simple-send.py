# -*- coding: utf-8 -*-
import json
import time
import uuid

import pika

conn = pika.BlockingConnection()
chan = conn.channel()

idfa = str(uuid.uuid4()).upper()

userId = 2003
taskId = 1
requestTime = int(time.time())
body = json.dumps([idfa, userId, taskId, requestTime])

# help(chan.basic_publish)

properties = {
    'content_type': 'application/json',
    'content_encoding': '',
}

prop = pika.BasicProperties(**properties)

chan.basic_publish(
    'hebe.topic',
    'highearn.sf_idfa',
    body,
    prop,
)
