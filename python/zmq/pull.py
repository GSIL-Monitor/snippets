#!/bin/bash
from datetime import datetime

import zmq

ctx = zmq.Context()
sock = ctx.socket(zmq.PULL)

sock.connect('tcp://app10-031.i.ajkdns.com:26543')
sock.connect('tcp://app10-102.i.ajkdns.com:26543')

cnt = 0

dtstart = datetime.now()

while True:

    now = datetime.now()

    if (now - dtstart).seconds >= 60:
	print(cnt)
	cnt = 0
	dtstart = now

    sock.recv()
    cnt += 1
