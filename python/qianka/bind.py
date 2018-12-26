# -*- coding: utf-8 -*-

from qianka_cache import QKCache

cache = QKCache()
cache.configure({
    'CACHE_ENABLED': True,
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'hera:',
    'CACHE_NODES': {
        'short': ('redisv2', [
            'redis://10.111.5.98/7',   # 1496:6379
            'redis://10.111.5.99/7',   # 1497:6379
            'redis://10.111.5.100/7',  # 1498:6379
            'redis://10.111.5.97/7',   # 1499:6379
        ]),
        'misc': ('redisv2', [
            'redis://10.111.5.98/0',   # 1496:6379
            'redis://10.111.5.99/0',   # 1497:6379
            'redis://10.111.5.100/0',  # 1498:6379
            'redis://10.111.5.97/0',   # 1499:6379
        ]),
    }
})

# k = 'user:last:bundle.v6:{}'.format(57145249)
k = 'lite:bind:uid:{}'.format(57145249)
_ = cache('misc').get(k)
print(_)
