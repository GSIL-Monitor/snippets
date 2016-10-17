# -*- coding: utf-8 -*-

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
