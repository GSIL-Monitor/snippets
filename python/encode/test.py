# -*- coding: utf-8 -*-
import base64
import sys

_in = sys.argv[1]

_in = _in.encode('ascii')
try:
    base64.b64decode(_in)
except:
    print('1')
    print(_in[:10])
