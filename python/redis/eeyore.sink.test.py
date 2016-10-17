# -*- coding: utf-8 -*-
import random
import time
import uuid

import redis
import msgpack



r = redis.StrictRedis()


while True:
    _, payload = r.blpop('qianka:eeyore:pending_write_back')
    _ = msgpack.unpackb(payload)
    print(_)
