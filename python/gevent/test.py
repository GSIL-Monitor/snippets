# -*- coding: utf-8 -*-
import gevent
import gevent.pool
import random

from functools import wraps


def work(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            rv = func(*args, **kwargs)
            return True, rv, args, kwargs
        except:
            return False, None, args, kwargs
    return wrapper


@work
def sleep(sec):
    if sec > 2:
        raise RuntimeError('too heavy!')
    print('sleeping for %s' % sec)
    gevent.sleep(sec)
    return sec



def submit_work(func, *args, **kwargs):
    g = pool.spawn(func, *args, **kwargs)
    g.link_value(callback)
    g.link_exception(fail_callback)
    return g

pool = gevent.pool.Pool(200)

def callback(x):
    print(x.value)

def fail_callback(x):
    print(x.exception)


_ = []
for i in range(300):
    _.append(submit_work(sleep, random.random() * 3))


pool.join(timeout=1)
