# -*- coding: utf-8 -*-
import logging
import random
import time
import uuid


import redis
import msgpack



r = redis.StrictRedis()

idfa = [
    '275DAB3F-F200-4127-AC1A-F9762FB8435A',
    'BA2F6EFE-C7C8-466E-BB43-594F4D9D7ADE'
]
result = {}
for i in idfa:
    result[i] = int(random.random() * 2)

r = redis.StrictRedis()


app = {
    'apple_id': 123,
    'idfa': idfa,
    'ad_id': 1,
    'url': 'http://example.com',
    'idfa_type': 0,
    'result': result,
}


while True:
    payload = msgpack.packb(app)
    r.rpush('qianka:eeyore:pending_cache', payload)
    logging.warning('pushed %s' % payload)
    time.sleep(5)
