# -*- coding: utf-8 -*-
import gzip
import time

from messagebroker.v3 import MessageBrokerClientV3

client = MessageBrokerClientV3()

o = {
    'type': 'mb object',
    'time': int(time.time()),
}

_ = client.send(
    connection='default',
    exchange='amq.topic',
    routing_key='mb_hello',
    o=o,
    marshal=MessageBrokerClientV3.MARSHAL_MSGPACK,
    compress=MessageBrokerClientV3.COMPRESS_LZMA,
)
print(_)

_ = client.send(
    connection='default',
    exchange='amq.topic',
    routing_key='mb_hello',
    o=gzip.compress(b'bytes content'),
)
print(_)

_ = client.send(
    connection='default',
    exchange='amq.topic',
    routing_key='mb_hello',
    o='a simple text message',
)
print(_)
