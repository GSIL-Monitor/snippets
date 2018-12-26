# -*- coding: utf-8 -*-
from datetime import datetime
import time
import socket

hostname = socket.gethostname()

TX = '/sys/class/net/{}/statistics/tx_packets'
RX = '/sys/class/net/{}/statistics/rx_packets'


def getRx(name='eth0'):
    fn = RX.format(name)
    with open(fn) as f:
        rv = int(f.read().strip())
    return rv


def getTx(name='eth0'):
    fn = RX.format(name)
    with open(fn) as f:
        rv = int(f.read().strip())
    return rv


rx = getRx()
tx = getTx()
time.sleep(1)
while True:
    newRx = getRx()
    deltaRx = newRx - rx
    newTx = getTx()
    deltaTx = newTx - tx
    dt = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    print('{}\t{}\tr: {}, t: {}'.format(hostname, dt, deltaRx, deltaTx))
    rx = newRx
    tx = newTx
    time.sleep(1)
