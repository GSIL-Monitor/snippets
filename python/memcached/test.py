# -*- coding: utf-8 -*-
import time

import msgpack
import pylibmc


mc = pylibmc.Client(['127.0.0.1'])

payload = 'hello world'
start = time.time()
mc.set('hello', msgpack.dumps(payload), 1)

print(time.time() - start)

time.sleep(1)

_ = mc.get('hello')
print(_)
