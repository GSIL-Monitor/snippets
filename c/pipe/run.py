# -*- coding: utf-8 -*-
import time


cnt = 0
while True:
    cnt += 1
    with open('/tmp/a.txt', 'w') as f:
        f.write(str(cnt) + "\n")
    if cnt % 2 == 0:
        time.sleep(0.2)
    print(str(cnt))
