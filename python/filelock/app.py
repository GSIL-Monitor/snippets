# -*- coding: utf-8 -*-
from time import sleep

import filelock

lock = filelock.FileLock('my.lock')

try:
    with lock.acquire(timeout=3):
        print('lock acquired, sleep for 10s...')
        sleep(10)

except filelock.Timeout as err:
    print('Cound not acquire the file lock, quit...')
