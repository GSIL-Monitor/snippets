# -*- coding: utf-8 -*-
import msgpack
import redis


r = redis.StrictRedis()

while True:
    __, _ = r.blpop('qianka:eeyore:pending_cache')
    payload = msgpack.unpackb(_, encoding='utf-8')
    print(payload)
