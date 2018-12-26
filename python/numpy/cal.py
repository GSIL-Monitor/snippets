# -*- coding: utf-8 -*-
import logging
import sys

import numpy

logging.basicConfig(level=logging.DEBUG)
fn = sys.argv[1]

arr = []
with open(fn) as f:
    for line in f:
        cnt, visit = line.split('\t')
        arr.append((int(cnt), int(visit)))

samples = []
for el in arr:
    cnt, visit = el
    _ = [visit] * cnt
    samples.extend(_)

print(len(samples))


logging.debug('mean: {}'.format(numpy.mean(samples)))
logging.debug('median: {}'.format(numpy.median(samples)))
logging.debug('stdev: {}'.format(numpy.std(samples)))
