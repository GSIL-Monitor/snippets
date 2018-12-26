# -*- coding: utf-8 -*-
from qianka_cache import QKCache

cache = QKCache()
cache.configure({
    'CACHE_ENABLED': True,
    'CACHE_DEFAULT_TIMEOUT': 0,
    'CACHE_NODES': {
        'default': ('2layer', {
            'L1': ('redisv2', ['redis://127.0.0.1/127']),
            'L2': ('redisv2', ['redis://127.0.0.1/128']),
        }),
        'L1': ('redisv2', ['redis://127.0.0.1/127']),
        'L2': ('redisv2', ['redis://127.0.0.1/128']),
    },
})
