# -*- coding: utf-8 -*-

from ploceus.api import task, run, run_task

@task
def test(hello):
    print(hello)
    return run('date').stdout

def my_task():
    return run_task(test, ['n1386.ops.gaoshou.me'])
