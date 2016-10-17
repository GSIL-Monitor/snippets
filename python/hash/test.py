# -*- coding: utf-8 -*-
import base64
import sys

def split_to_chunk(line, n):
    return [line[i:i+n] for i in range(0, len(line), n)]

with open(sys.argv[1], 'rb') as f:
    content = f.read()

payload = base64.b64encode(content)
_ = "\n".join(split_to_chunk(payload.decode('ascii'), 36))

print(_)
