# -*- coding: utf-8 -*-
import logging
import os
import threading
import time

logging.basicConfig(level=logging.INFO)

def long_running_thread():
    while True:
        logging.info('I am running...')
        time.sleep(2)

t = threading.Thread(target=long_running_thread)
t.setDaemon(True)
t.start()

pid = os.fork()
if pid:
    # parent
    while True:
        t.join(timeout=1)
else:
    print(t)
    print(t.isAlive())
