# -*- coding: utf-8 -*-
import gzip
import lzma
import zlib

import magic

b = b'hello world'

mime = magic.Magic(mime=True)
# mime = magic.Magic()
print(mime.from_buffer(gzip.compress(b, 1)))
print(mime.from_buffer(lzma.compress(b, preset=1)))
print(mime.from_buffer(zlib.compress(b, 1)))
