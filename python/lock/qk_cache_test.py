# -*- coding: utf-8 -*-
import logging
import time

from qianka_cache import QKCache
from redis_lock import QkRedisExLock


logging.basicConfig(level=logging.DEBUG)

config = {
    'CACHE_ENABLED': True,
    # 'CACHE_PREFIX': 'hebe:',
    'CACHE_PREFIX': '',
    'CACHE_DEFAULT_TIMEOUT': 900,
    'CACHE_NODES': {
        'default': ('redisv2', ['redis://'])
    },
}

cache = QKCache()
cache.configure(config)

_cache = cache.get_cache()
k = 'some-key'
timeout = 5
with QkRedisExLock(_cache, k, timeout) as lock:
    time.sleep(3)
