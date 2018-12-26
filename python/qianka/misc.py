# -*- coding: utf-8 -*-
import logging

from qianka_cache import QKCache


logging.basicConfig(level=logging.DEBUG)

config = {
    'CACHE_ENABLED': True,
    'CACHE_TIMEOUT': 0,
    'CACHE_KEY_PREFIX': 'hera:',
    'CACHE_NODES': {
        'session': ('redisv2', [
            'redis://10.45.32.32',
            'redis://10.45.32.89',
            'redis://10.111.5.98/9',
        ])
    }
}

cache = QKCache()
cache.configure(config)

_ = cache('session').get('v4:uv:index:android:20180719', raw=True)
print(_)
