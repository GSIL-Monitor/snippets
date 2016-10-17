# -*- coding: utf-8 -*-
from multiprocessing.pool import Pool
from multiprocessing.pool import ThreadPool
import os
import threading
import time


pool = Pool()



def master():
    while True:
        time.sleep(1)

def checker():

    def sleep():
        import time
        with open('/tmp/test.log', 'a') as f:
            f.writelines('sleep 3')
        time.sleep(3)

    while True:
        print('submit new task')
        pool.apply_async(sleep)
        time.sleep(1)


t1 = threading.Thread(target=master)
t2 = threading.Thread(target=checker)

t1.start()
t2.start()

t1.join()
t2.join()

# pool.close()
# pool.join()
