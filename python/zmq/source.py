# -*- coding: utf-8 -*-
import time
import random
import zmq




ctx = zmq.Context()

pusher = ctx.socket(zmq.PUSH)
pusher.connect('tcp://localhost:23456')

for i in range(1000):
    pusher.send(str(int(random.random() * 100)).encode('UTF-8'))
