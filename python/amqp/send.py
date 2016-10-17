# -*- coding: utf-8 -*-
import datetime
import logging
import time

import pika

conn = None
chan = None

def on_message(*args, **kwargs):
    print(args, kwargs)

def connect():
    global conn ,chan
    try:
        if conn:
            conn.close()
    except pika.exceptions.AMQPConnectionError as e:
        pass

    p = pika.ConnectionParameters(
        host='127.0.0.1',
        port=5670,
        virtual_host='/')

    while True:
        try:
            conn = pika.BlockingConnection(p)
            chan = conn.channel()
            break
        except pika.exceptions.AMQPConnectionError as e:
            print(e)
            time.sleep(0.5)
            pass


cnt = 0
connect()
while True:
    try:
        b = str(datetime.datetime.now())
        chan.basic_publish(
            exchange='test.exchange',
            routing_key='test',
            body=b)
        cnt += 1
        print(cnt)
        time.sleep(0.5)
    except pika.exceptions.AMQPError as e:
        logging.exception('')
        time.sleep(0.5)
        connect()

conn.close()
