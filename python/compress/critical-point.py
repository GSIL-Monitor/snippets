# -*- coding: utf-8 -*-
import lzma
import zlib


with open('b.bin', 'rb') as f:
    c = f.read().strip()


l = 1
while True:
    b = c[:l]
    # compressed = zlib.compress(b, 1)
    compressed = lzma.compress(b, 1)
    if len(compressed) < len(b):
        print(l)
        break
    l += 1
