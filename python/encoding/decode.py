# -*- coding: utf-8 -*-
import pickle

import msgpack

# import common




with open('file', 'rb') as f:
    _ = f.read()

_ = pickle.loads(msgpack.unpackb(_))

print(_)
print(_.prop1)
print(_.prop2)
