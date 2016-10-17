# -*- coding: utf-8 -*-
import datetime
import socket
import time

from kombu import Connection, Exchange, Queue

exchange = Exchange('amq.topic', 'topic', durable=True)
queue = Queue('test', exchange=exchange, routing_key='#')


def on_message(timestamp, message):
    message.ack()

#
# with Connection('amqp://guest:guest@127.0.0.1//?heartbeat=2') as conn:
#     with conn.Consumer(queue, callbacks=[on_message]) as consumer:
#         while True:
#             conn.drain_events()


def do():
    try:
        with Connection(
                'pyamqp://guest:guest@127.0.0.1://?heartbeat=2') as conn:


        # producer = conn.Producer(serializer='json')
            cnt = 0
        # while True:
        #     b = str(datetime.datetime.now())
        #     producer.publish(b, exchange=exchange, routing_key='test')
        #     cnt += 1
        #     print(cnt)
        #     time.sleep(10)
            with conn.Consumer(queue, callbacks=[on_message]) as consumer:
                    while True:
                        try:
                            conn.heartbeat_check(rate=1)
                            conn.drain_events(timeout=1)
                        except socket.timeout as e:
                            pass
                        except Exception as e:
                            raise
    except Exception as e:
        print(e)
        print(type(e))


while True:
    do()
