# -*- coding: utf-8; mode: python -*-
from ploceus.api import task
from ploceus.helper import run, local
from ploceus.task import TaskRunner

@task
def test():
    return run('sha256sum /etc/hosts')

def f():
    hostname = 'lb1'
    hosts = [hostname]
    rv = TaskRunner.run_task_with_hosts(test, hosts)
    print(rv[hostname].__dict__)

f()
