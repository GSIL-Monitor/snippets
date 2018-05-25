# -*- coding: utf-8 -*-
import base64
import json
import logging
import lzma
import quopri
import pprint
import time

import pika

conn = None
chan = None
logging.basicConfig(level=logging.DEBUG)

QUEUE_NAME = 'test'

def connect():
    global conn, chan
    try:
        if conn:
            conn.close()
    except pika.exceptions.AMQPConnectionError as e:
        pass

    p = pika.connection.URLParameters(
        'amqp://guest:guest@127.0.0.1:5672/?heartbeat_interval=30')
        # 'amqp://guest:guest@n1432.ops.gaoshou.me:5672/?heartbeat_interval=30')

    while True:
        try:
            conn = pika.BlockingConnection(p)
            chan = conn.channel()
            break
        except pika.exceptions.AMQPConnectionError as e:
            print(e)
            time.sleep(1)
            pass

    # chan.queue_declare(
    #     QUEUE_NAME,
    #     durable=False,
    #     exclusive=False,
    #     auto_delete=True,
    # )
    #
    # chan.queue_bind(
    #     QUEUE_NAME,
    #     exchange='hera.topic',
    #     routing_key='.#',
    # )

connect()

cnt = 0

while True:
    try:
        for d, prop, body in chan.consume(QUEUE_NAME, no_ack=True):
            cnt += 1
            print(prop)
            print(prop.__dict__)
            print(body)
            # print(len(body))
            # b = quopri.encodestring(body)
            # print(len(b))
            # b = base64.b64encode(body)
            # print(len(b))
            # z = lzma.decompress(body)
            # print(len(z))
            print('==========')

    except pika.exceptions.AMQPError as e:
        logging.exception('')
        time.sleep(1)
        connect()

requeued_messages = chan.cancel()
logging.warning(requeued_messages)
conn.close()
