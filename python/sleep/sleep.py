# -*- coding: utf-8 -*-
import random
import time
import sys

s = int(random.random() * 5)
if s == 0:
    print('will sleep for 1 seconds...', flush=True)
    time.sleep(1)
    sys.exit(0)

s = random.random() * 100
print('will sleep for %s seconds...' % s, flush=True)
time.sleep(s)
