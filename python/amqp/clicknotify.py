# -*- coding: utf-8 -*-
import json
import time
import uuid

import pika

conn = pika.BlockingConnection()
chan = conn.channel()



def send_notify(eid, tid, idfa, ip):
    global chan

    data = {
        'event_id': eid,
        'task_id': tid,
        'ipv4': ip,
        'idfa': idfa,
    }

    body = json.dumps(data)

    # help(chan.basic_publish)

    properties = {}

    prop = pika.BasicProperties(**properties)

    chan.basic_publish(
        'hera.topic',
        'subtasks.startnotify.#',
        body,
        prop,
    )


idfa = str(uuid.uuid4()).upper()
send_notify(78125, 654777, idfa, '127.0.0.7')
idfa = str(uuid.uuid4()).upper()
send_notify(78126, 654789, idfa, '127.0.0.8')
