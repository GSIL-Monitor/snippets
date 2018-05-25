# -*- coding: utf-8 -*-
import time
from redis import StrictRedis

client = StrictRedis.from_url('redis://')


_ = time.time()
cnt = 0
pipe = None
for i in range(100000):
    if cnt == 0:
        pipe = client.pipeline()
    pipe.set('1', '1', None)
    cnt += 1
    if cnt == 100:
        results = pipe.execute()
        for i in results:
            if i is not True:
                raise RuntimeError('1')
        cnt = 0
        pipe = client.pipeline()

print(int((time.time() - _) * 1000))
