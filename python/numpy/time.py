# -*- coding: utf-8 -*-
from collections import defaultdict
import logging
import pprint
import sys

import numpy


logging.basicConfig(level=logging.DEBUG)


fn = sys.argv[1]

data = defaultdict(lambda: defaultdict(list))

with open(fn) as f:
    for line in f:
        t, tc, hostname = line.split('\t')
        hostname = hostname.strip()
        data[hostname][t].append(int(tc))

# logging.debug(pprint.pformat(data))

finalData = defaultdict(lambda: defaultdict(int))
for hostname in data:
    host = data[hostname]
    for t in host:
        tc = sorted(host[t])
        finalTc = numpy.mean(tc)
        finalData[hostname][t] = finalTc

logging.debug(pprint.pformat(finalData))


for hostname in finalData:
    host = finalData[hostname]
    for t in host:
        tc = host[t]
        fn = hostname + '.csv'
        with open(fn, 'a') as f:
            tc = '%.3f' % tc
            line = '{}\t{}\n'.format(t, tc)
            f.write(line)
