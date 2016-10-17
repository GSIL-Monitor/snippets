# -*- coding: utf-8 -*-

import lzma

xz_decomp = lzma.LZMADecompressor()

with open('b', 'rb') as f:
    _ = f.read()
    o = xz_decomp.decompress(_)
    print(o)
