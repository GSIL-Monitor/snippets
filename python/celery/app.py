# -*- coding: utf-8 -*-
from functools import reduce
import logging
import random

from celery import Celery


celery = Celery()




def _add(a, b):
    return a + b

@celery.task(ignore_result=True)
def add(*args):
    # _ = int(random.random() * 10)
    # if _ < 5:
    #     raise RuntimeError('error')

    print(reduce(_add, args))
