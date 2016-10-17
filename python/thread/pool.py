# -*- coding: utf-8 -*-
from multiprocessing.pool import ThreadPool
from time import sleep

def do_some_work(payload):
    print('got payload: %s' % payload)
    if payload >= 3:
        raise Exception()
    sleep(payload)
    return payload

pool = ThreadPool(4)

doing_queue = set()

ok_result = []
fail_result = []

def ok_callback(result):
    ok_result.append(result)


def fail_callback(result):
    fail_result.append(result)


def submit_job(payload):
    doing_queue.add(
        pool.apply_async(do_some_work,
                         args=(payload,)))

def wait_for_result(timeout, block=False):
    sleep(timeout)
    rv = []
    done = set()
    for result in doing_queue:
        if not block and result.ready():
            rv.append(result.get())
            done.add(result)

    for _ in done:
        doing_queue.remove(_)

    return rv

submit_job(1)
submit_job(2)
submit_job(3)
submit_job(4)

rv = wait_for_result(5)

print(ok_result, fail_result)
