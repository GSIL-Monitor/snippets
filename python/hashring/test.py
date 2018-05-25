# -*- coding: utf-8 -*-
import chashring
from qianka.cache.redis_cache import RedisCache

nodes = [
    'redis://10.47.77.3/2',
    'redis://10.45.23.62/2',
    'redis://10.45.22.22/2',
    'redis://10.45.52.32/2'
]

# user_id = 201
user_id = 53975033
keyb = b'hera:u:current:lppa:%s' % str(user_id).encode('ascii')
key = 'u:current:lppa:%s' % str(user_id)

ring = chashring.HashRing(
    map(lambda x: x.encode('ascii'), nodes),
    128)
_ = ring.find_node(keyb)
print(_)

cache = RedisCache(nodes, 'json', key_prefix='hera')

# with open('testcase.txt', 'w') as f:
#     counter = 0
#     for i in range(50000000, 54000000):
#         key = 'u:current:lppa:%s' % str(i)
#         _ = cache.ring.get_node(key)
#
#         line = "{}\t{}".format(key, _)
#         f.write(line + '\n')
#
#         counter += 1
#         if counter % 10000 == 0:
#             print('counter: {}'.format(counter))

# _ = cache.ring.get_node('hera:did:lppa:a1b3888e5d1f2a0c7da298afe22d8806fb61584b')
# print(_)

from redis import StrictRedis
import lzma
key = 'hera:did:lppa:a1b3888e5d1f2a0c7da298afe22d8806fb61584b'
client = StrictRedis.from_url('redis://10.45.52.32/2')
_ = client.get(key)
_ = lzma.decompress(_)
print(_)
