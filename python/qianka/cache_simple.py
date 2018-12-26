# -*- coding: utf-8 -*-
from qianka_cache import QKCache

cache = QKCache()
cache.configure({
    'CACHE_ENABLED': True,
    'CACHE_DEFAULT_TIMEOUT': 0,
    'CACHE_NODES': {
        'default': ('redis', ['redis://127.0.0.1:6380/0']),
    }
})

# _ = cache('default').dec('1')
# print(_)

k = 'k1'
v = 1
cache.set(k, v)
rt = cache.get(k)
print(rt)
print(type(rt))
