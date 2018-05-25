# -*- coding: utf-8 -*-
import argparse
import time

import pika

ap = argparse.ArgumentParser()
ap.add_argument('--exchange', default='amq.topic')
ap.add_argument('--routing-key', default='hello')
ap.add_argument('--host', default='127.0.0.1')
ap.add_argument('--port', default=5672, type=int)
ap.add_argument('--queue', default='test')
ap.add_argument('--sleep', default=0.0, type=float)

options = ap.parse_args()

url = 'amqp://guest:guest@%s:%d' % (options.host, options.port)

cp = pika.URLParameters(url)
conn = pika.BlockingConnection(cp)
chan = conn.channel()

chan.queue_declare(options.queue, durable=False, auto_delete=True)
chan.queue_bind(
    options.queue,
    exchange=options.exchange,
    routing_key=options.routing_key)


cnt = 0


def on_message(channel, frame, prop, body):
    global cnt
    cnt += 1
    time.sleep(options.sleep)
    print(cnt)


chan.basic_consume(
    on_message, options.queue, no_ack=True, consumer_tag='hello')

chan.start_consuming()

while True:
    time.sleep(1)
