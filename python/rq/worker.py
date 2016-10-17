# -*- coding: utf-8 -*-
import itertools
import sys
from rq import Queue, Connection, Worker

with Connection():

    q = Queue('low', prefix='test')

    w = Worker(q, prefix='test')

    w.work()
