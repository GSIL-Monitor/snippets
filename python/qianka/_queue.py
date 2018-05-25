# -*- coding: utf-8 -*-
import time

from qianka_queue.amqp import QkAmqp

amqp = QkAmqp()
amqp.configure({
    'AMQP_CONNECTIONS': {
        'default': 'amqp://127.0.0.1',
    }
})

o = {
    'time': time.time(),
}

_ = amqp.send(
    o,
    exchange_name='amq.topic',
    routing_key='hello',
    marshal='msgpack',
    compress='zlib',
)
print(_)
amqp.reset()
_ = amqp.send(
    o,
    exchange_name='amq.topic',
    routing_key='hello',
    marshal='msgpack',
    compress='zlib',
)
print(_)

time.sleep(300)
