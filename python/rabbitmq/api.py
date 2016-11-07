# -*- coding: utf-8 -*-
import datetime
import json
import pprint
from urllib.parse import quote

import requests

HOST = 'n1413.ops.gaoshou.me'

url = 'http://guest:guest@%s:15672/api/connections' % HOST

def close_connection(name, host):
    _url = 'http://guest:guest@%s:15672/api/connections/%s' % (
        host, quote(name))
    resp = requests.delete(_url)
    print(resp.status_code)

r = requests.get(url)
p = json.loads(r.text)

dt = datetime.datetime(2016, 10, 17)
ts = int(dt.strftime("%s")) * 1000

a = [x for x in filter(
    lambda x: x['connected_at'] < ts and x['timeout'] == 0, p)]

total = len(a)
cnt = 0
for _ in a:
    cnt += 1
    dt = datetime.datetime.fromtimestamp(_['connected_at'] / 1000)
    print(_['name'], ': ', dt.strftime('%Y-%m-%d %H:%M:%S'))
    close_connection(_['name'], HOST)
    print("%s/%s" % (cnt, total))
