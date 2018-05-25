# -*- coding: utf-8 -*-
from threading import Thread
import time

cnt1 = 0
cnt2 = 0
stop = False

def increment1():
    global cnt1
    while not stop:
        cnt1 += 1

def increment2():
    global cnt2
    while not stop:
        cnt2 += 1

t1 = Thread(target=increment1)
# t2 = Thread(target=increment2)
t1.start()
# t2.start()

time.sleep(1)
stop = True
t1.join()
# t2.join()

total = cnt1 + cnt2
print(cnt1)
