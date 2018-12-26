# -*- coding: utf-8 -*-
import gzip
import lzma
import sys
import pprint
import time
import simplejson
import zlib

import magic

with open('lppa.plain.txt', 'rb') as f:
    for line in f:
        b = simplejson.loads(line)
        pprint.pprint(b)
        break

b = simplejson.dumps(b).encode('utf-8')
b = zlib.compress(b, 1)
# b = lzma.compress(b, 1)
_ = magic.from_buffer(b[:1024], mime=True)
pprint.pprint(_)

sys.exit()


ts = time.time()
total = 0
with open('lppa.plain.txt', 'rb') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        b = lzma.compress(line, preset=1)
        total += len(b)

tc = time.time() - ts
print('lzma: {}'.format(tc))
print('length: {}'.format(total))

ts = time.time()
total = 0
with open('lppa.plain.txt', 'rb') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        b = zlib.compress(line, 1)
        total += len(b)

tc = time.time() - ts
print('zlib: {}'.format(tc))
print('length: {}'.format(total))

ts = time.time()
total = 0
with open('lppa.plain.txt', 'rb') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        b = gzip.compress(line, 1)
        total += len(b)

tc = time.time() - ts
print('gzip: {}'.format(tc))
print('length: {}'.format(total))
