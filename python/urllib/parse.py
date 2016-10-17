# -*- coding: utf-8 -*-
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
import sys


url = sys.argv[1]

u = urlparse(url)
q = parse_qsl(u.query)


print(q)

payload = dict(appId='123', idfa='fwjijfwijfwi', ipv4='127.0.0.1', q=3)

for k in payload:
    q.append((k, payload[k]))

u_dist = (u.scheme, u.netloc, u.path, '', urlencode(q), '')
url = urlunparse(u_dist)

print(url)
