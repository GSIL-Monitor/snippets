# -*- coding: utf-8 -*-
import logging
import time

import redis
import msgpack

r = redis.StrictRedis()


result = [
    (1, 1, 0),
    (1, 2, 1),
]
while True:
    payload = msgpack.packb(result)
    r.rpush('qianka:eeyore:pending_writeback', payload)
    logging.warning('pushed %s' % payload)
    time.sleep(5)
