# -*- coding: utf-8 -*-
import redis

r = redis.StrictRedis()

while True:
    _ = r.blpop('test', timeout=1)
    if _ is None:
        continue
    print(_)
    break
