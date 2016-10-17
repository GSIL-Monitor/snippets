# -*- coding: utf-8 -*-
import time

import msgpack
import pylibmc



mc = pylibmc.Client(['127.0.0.1'])

payload = 'hello world'
start = time.time()
mc.set('hello', msgpack.dumps(payload), 10)

print(time.time() - start)
