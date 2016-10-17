# -*- coding: utf-8 -*-
import pickle

import msgpack

import common





m = common.MyClass()
m.prop1 = '1'
m.prop2 = {'a': 1}

_ = msgpack.packb(pickle.dumps(m))

with open('file', 'wb') as f:
    f.write(_)
