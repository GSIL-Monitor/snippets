# -*- coding: utf-8 -*-
import sys

from qianka_cache import QKCache

cache = QKCache()
cache.configure({
    'CACHE_ENABLED': True,
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_NODES': {
        'user': ('redisv2', [
            'redis://10.111.5.98/10',   # 1496:6379
            'redis://10.111.5.99/10',   # 1497:6379
            'redis://10.111.5.100/10',  # 1498:6379
            'redis://10.111.5.97/10',   # 1499:6379
        ])
    }
})

def doset(userId):
    cache_key = '{}_is_need_do_priority_task'.format(userId)
    cache('user').set(cache_key, 1, timeout=86400 * 2)


fn = sys.argv[1]
i = 0
with open(fn) as f:
    for line in f:
        i += 1
        userId = int(line.strip())
        doset(userId)
        print(i)
