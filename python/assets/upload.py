# -*- coding: utf-8 -*-
import hashlib
import imghdr
import io
import os
import sys


import requests

if len(sys.argv) == 1:
    print('usage: %s </path/to/image>' % sys.argv[0])
    sys.exit(1)

if sys.argv[1].startswith('/'):
    fn = os.path.abspath(sys.argv[1])
else:
    fn = os.path.abspath(os.path.join(os.getcwd(), sys.argv[1]))

with open(fn, 'rb') as f:
    _ = f.read()

m = hashlib.md5()
m.update(_)
hashsum = m.hexdigest()

ext = str(imghdr.what(None, h=_)).lower()
print(hashsum, ext)

url = 'http://qianka.b0.upaiyun.com/images/%s.%s' % (hashsum, ext)
res = requests.head(url)
if res.status_code == 200:
    print(url)
    sys.exit(0)

f = io.BytesIO()
f.write(_)
f.seek(0)
res = requests.post('http://n1386.ops.gaoshou.me:5000/', data=f)

if res.status_code == 200:
    print(url)
    sys.exit(0)
else:
    print(res.status_code)
    print(res.text)
    sys.exit(1)
