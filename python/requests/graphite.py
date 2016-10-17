# -*- coding: utf-8 -*-
import json
import logging
import urllib


import requests


logging.basicConfig(level=logging.DEBUG)

def fetch_data(target, _from='-1d', until='now', _format='json'):
    params = {
        'target': target,
        'from': _from,
        'until': until,
        'format': _format
    }
    _ = urllib.parse.urlencode(params)

    url = '%s/render?%s' % ('http://n1391.ops.gaoshou.me:8000', _)

    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError('response not 200')

    # if _format == 'json':
    #    return res.json()
    return res.text


d = fetch_data(
    'transformNull(stats.counters.biz.zq.hera.subtasks.finish.count,0)')

a = sum(map(lambda x: x[0], json.loads(d)[0]['datapoints']))
print(int(a))

d = fetch_data(
    'transformNull(stats.counters.biz.zq.hera.subtasks.start.count,0)')

b = sum(map(lambda x: x[0], json.loads(d)[0]['datapoints']))
print(int(b))

print(a / b)

d = fetch_data(
    'transformNull(stats.counters.biz.zq.hera.subtasks.finish_rongyuka.count,0)')

a = sum(map(lambda x: x[0], json.loads(d)[0]['datapoints']))
print(int(a))

d = fetch_data(
    'transformNull(stats.counters.biz.zq.hera.subtasks.start_rongyuka.count,0)')

b = sum(map(lambda x: x[0], json.loads(d)[0]['datapoints']))
print(int(b))

print(a / b)
