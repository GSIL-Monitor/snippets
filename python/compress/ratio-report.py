# -*- coding: utf-8 -*-
import logging
import lzma
import pprint
import zlib


with open('b.bin', 'rb') as f:
    c = f.read().strip()

# 分布情况(LZMA压缩后)
# 数量，字节大小
distribution = []
with open('distribution.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        count, size = line.split('\t')
        count = int(count)
        size = int(size) / 8
        distribution.append([count, size])

distribution.reverse()

ORIGIN_SIZES = []
# 计算出LZMA压缩后大小对应的原始大小
l = 0
for row in distribution:
    logging.error('calc for {}'.format(row[1]))
    size = row[1]
    while True:
        b = c[:l]
        compressed = lzma.compress(b, 1)
        if len(compressed) == size:
            ORIGIN_SIZES.append(l)
            row.append(l)
            break
        l += 1
        if l > len(c):
            ORIGIN_SIZES.append(0)
            row.append(0)
            break


originTotal = 0
lzmaTotal = 0
zlibTotal = 0

for row in distribution:
    count, _, size = row
    b = c[:size]
    originTotal += len(b) * count
    lzmaTotal += len(lzma.compress(b, 1)) * count
    zlibTotal += len(zlib.compress(b, 1)) * count

pprint.pprint({
    'total': originTotal,
    'lzma': lzmaTotal,
    'zlib': zlibTotal,
})
