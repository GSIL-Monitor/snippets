# -*- coding: utf-8 -*-
from redis import StrictRedis
from qianka_cache import QKCache

cache = QKCache()

cache.configure({
    'CACHE_ENABLED': True,
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_NODES': {
        'ip': ('redisv2', [
            'redis://10.111.5.98/8',   # 1496:6379
            'redis://10.111.5.99/8',   # 1497:6379
            'redis://10.111.5.100/8',  # 1498:6379
            'redis://10.111.5.97/8',   # 1499:6379
        ]),
    },
})

_ = cache('ip').get('ip:address:1.182.164.144')
print(_)


client = StrictRedis.from_url('redis://n1435.ops.gaoshou.me/')
kl = client.keys('hera:ip:address:*')
total = len(kl)
i = 0
for k in sorted(kl):
    _ = client.get(k)
    print(_)
    if _:
        k = k.decode('utf8')
        nk = k.replace('hera:', '')
        print(nk)
        cache('ip').set(nk, _, timeout=86400 * 2, raw=True)
    i += 1
    print('{}/{}'.format(i, total))
