# -*- coding: utf-8 -*-
import logging
import time

# import cipip as pyipip

logging.basicConfig(level=logging.DEBUG)

import datx
c = datx.City("/home/momoka/Downloads/17monipdb.datx")

logger = logging.getLogger(__name__)

s = time.time()
# ipip = pyipip.IPIPDatabase('17monipdb.dat')
e = time.time()
delta = e - s
logger.debug('init time cost: %.6f s' % delta)
# _ = ipip.lookup('8.8.8.8')
# logger.debug(_)

counter = 0
s = time.time()

loop = 100
for i in range(loop):
    with open('/home/momoka/src/python/cipip-python/ips.txt') as f:
        for line in f:
            ip = line.strip()
            if not ip:
                continue
            # result = ipip.lookup(ip)
            result = c.find(ip)
            # logger.debug('%s -> %s' % (ip, result))
            counter += 1

e = time.time()
delta = e - s
logger.debug('loops: %d' % loop)
logger.debug('query time cost: %.6f s' % delta)
logger.debug('queries: %d' % counter)
