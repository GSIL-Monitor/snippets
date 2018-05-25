# -*- coding: utf-8 -*-
from threading import Thread
import time

def count():
    c = 0
    while True:
        c = c + 1

for _ in range(4):
    t = Thread(target=count)
    t.start()

while True:
    time.sleep(1)
