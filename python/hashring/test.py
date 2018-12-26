# -*- coding: utf-8 -*-
from qianka_cache import QKCache

cache = QKCache()
cache.configure({
    'CACHE_ENABLED': True,
    'CACHE_NODES': {
        'default': ('redisv2', [
            'redis://192.168.1.1',
            'redis://192.168.1.2',
            'redis://192.168.1.3',
            'redis://192.168.1.4',
            'redis://192.168.1.5',
        ])
    }
})

for i in range(100):
    key = str(i)
    url = cache()._key_to_url(key)
    print(url)
