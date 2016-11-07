# -*- coding: utf-8 -*-
import logging
logging.basicConfig(level=logging.DEBUG)
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

payload = dict(idfa='ABC', ipv4='1.2.3.4')


url = 'http://ad.wap.qunar.com/api/adcomp!insertAduid.action?source=qianka'

appid = 123456

u = urlparse(url)
q = parse_qs(u.query)

q_dist = {}
for _k in q:
    if len(q.get(_k)) == 1:
        q_dist[_k] = q.get(_k)[0]
    else:
        q_dist[_k] = q.get(_k)[0]

q_dist['appId'] = appid
q_dist['idfa'] = payload['idfa']
q_dist['ipv4'] = payload['ipv4']

qs_dist = urlencode(q_dist)

u_dist = (u.scheme, u.netloc, u.path, '', qs_dist, '')

url = urlunparse(u_dist)

print('request to: %s' % url)

from httpclient import get, post

resp = get('http://127.0.0.1:4567/')
logging.debug(resp.code)
logging.debug(resp.message)
logging.debug(resp.body)

resp = post('http://127.0.0.1:4567/post', data={'a': 1, 'b': 2})
logging.debug(resp.code)
logging.debug(resp.message)
logging.debug(resp.body)

resp = post('http://127.0.0.1:4567/post',
            data=open('/tmp/a', 'rb'))
logging.debug(resp.code)
logging.debug(resp.message)
logging.debug(resp.body)
