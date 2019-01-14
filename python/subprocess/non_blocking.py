# -*- coding: utf-8 -*-
from queue import Empty, Queue
from subprocess import Popen, PIPE
from threading import Thread


def enqueue_data(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


p = Popen(
    '/bin/bash -c "while true; do date; sleep 1; done"', stdout=PIPE,
    shell=True)
q = Queue()
t = Thread(target=enqueue_data, args=(p.stdout, q))
t.daemon = True
t.start()

while True:
    rc = p.poll()
    if rc is not None:
        # TODO:
        break
    try:
        line = q.get(timeout=.05)
    except Empty:
        pass
    else:
        print(line)
