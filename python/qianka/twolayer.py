# -*- coding: utf-8 -*-
import logging

from qianka_cache import QKCache


logging.basicConfig(level=logging.DEBUG)

config = {
    'CACHE_ENABLED': True,
    'CACHE_TIMEOUT': 0,
    'CACHE_NODES': {
        'default': ('2layer', {
            'L1': ('memcached', ['127.0.0.1']),
            'L2': ('redis', ['redis://127.0.0.1/2']),
        }),
        'mem': ('memcached', ['127.0.0.1']),
    }
}

cache = QKCache()
cache.configure(config)

_ = cache.get_many('1', '2', '3', '4', '5', raw=True)
# _ = cache('mem').get_many('1', '2', '3', '4', '5', raw=True)
print(_)
