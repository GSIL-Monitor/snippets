# -*- coding: utf-8 -*-
import pickle
import lzma

with open('/home/momoka/tmp/device-subtask.data', 'rb') as f:
    c = f.read()

data = pickle.loads(c)

lines = []
for row in data:
    b = row['packages']
    line = lzma.decompress(b)
    lines.append(line)

c = b'\n'.join(lines)
with open('device.plain.txt', 'wb') as f:
    f.write(c)
