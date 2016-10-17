# -*- coding: utf-8 -*-
import os
from time import sleep

import parallelism

pool = parallelism.ProcessPool()


def work():
    import random
    sleep(int(random.random() * 10))

pool.init(os.cpu_count(), work)

while True:
    pool.reap()
