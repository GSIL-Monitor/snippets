# -*- coding: utf-8 -*-
import logging
import time

import redis

import redis_lock


logging.basicConfig(level=logging.DEBUG)


client = redis.StrictRedis()

k = 'some-key'
timeout = 5

with redis_lock.RedisExLock(client, k, timeout) as lock:
    time.sleep(3)
