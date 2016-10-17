# -*- coding: utf-8 -*-
import lzma

xz_comp = lzma.LZMACompressor()

with open('data.txt', 'rb') as f:
    b = f.read().strip()
    _1 = xz_comp.compress(b)
    _2 = xz_comp.flush()
    with open('b', 'wb') as w:
        w.write(b''.join([_1, _2]))
