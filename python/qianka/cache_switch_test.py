# -*- coding: utf-8 -*-
import logging
import threading
import time
import timeit

from qianka_cache import QKCache
from statsd import StatsClient

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

config = {
    'CACHE_ENABLED': True,
    'CACHE_NODES': {
        'default': ('redis', ['redis://127.0.0.1']),
        'mem': ('memcached', ['127.0.0.1:11211']),
    },
    'CACHE_METRIC_SAMPLE_RATE': 1,
}


cache = QKCache()
cache.configure(config)
cache.get('1')
cache('mem').get('1')

stats = StatsClient()

cache._stats = stats

cnt = 10000

def switch():
    global cache
    while True:
        cache.setup_metric_reporting()
        logger.debug('hook up')
        time.sleep(0.8)
        cache.teardown_metric_reporting()
        logger.debug('hook down')
        time.sleep(0.8)

t = threading.Thread(target=switch)
t.start()

_ = timeit.timeit(stmt="cache.get('1')", globals=globals(), number=cnt)
print(_)
_ = timeit.timeit(stmt="cache('mem').get('1')", globals=globals(), number=cnt)
print(_)

cache.setup_metric_reporting()

print(cache._instances['default'].get)
print(cache._instances['mem'].get)


_ = timeit.timeit(stmt="cache.get('1')", globals=globals(), number=cnt)
print(_)
_ = timeit.timeit(stmt="cache('mem').get('1')", globals=globals(), number=cnt)
print(_)

cache.teardown_metric_reporting()

print(cache._instances['default'].get)
print(cache._instances['mem'].get)

_ = timeit.timeit(stmt="cache.get('1')", globals=globals(), number=cnt)
print(_)
_ = timeit.timeit(stmt="cache('mem').get('1')", globals=globals(), number=cnt)
print(_)
