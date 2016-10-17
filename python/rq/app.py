# -*- coding: utf-8 -*-
from time import sleep
from redis import StrictRedis

from rq import Queue

from module2 import add, error


q = Queue(connection=StrictRedis())
job = q.enqueue(add, 1, 3, result_ttl=10)

sleep(2)

print(job.result)
