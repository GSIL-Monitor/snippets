# -*- coding: utf-8 -*-
import logging
import time

import gevent
import gevent.monkey
from gevent.pool import Pool
import requests
import zmq.green as zmq

from aves.multiprocessing.pool.process import ProcessPool



logging.basicConfig(level=logging.DEBUG)
gevent.monkey.patch_socket()
ctx = zmq.Context()

recv = ctx.socket(zmq.PULL)
recv.bind('tcp://127.0.0.1:23456')

poll = zmq.Poller()
poll.register(recv, zmq.POLLIN)

pool = Pool(1000)
# pool = ProcessPool(48)

cnt = 0

def send(msg):
    res = requests.get('http://localhost:4567/?msg=' + msg.decode('UTF-8'))
    print(res)


while True:

    cnt += 1
    logging.debug('polling...')
    socks = dict(poll.poll())
    if recv in socks and socks[recv] == zmq.POLLIN:

        msg = recv.recv()
        print('got %s from upstream' % msg)

        # send(msg)

        if pool.full():
            pool.join(timeout=1)
        else:
            pool.spawn(send, msg)

        if cnt == 1000:
            break

pool.join()
