# -*- coding: utf-8 -*-
import urllib.parse
import uuid

import requests


APP_KEY = ''

def get_idfa():
    return str(uuid.uuid4()).upper()

idfas = set()
for i in range(5):
    idfas.add(get_idfa())

idfa = ",".join(idfas)

data = {
    'method': 'idfa.filter',
    'format': 'json',
    'v': '1.1',
    'appKey': APP_KEY,
    'idfa': idfa
}

print(data)

qs = urllib.parse.urlencode(data)

url = 'http://59.151.93.147:9191/router?%s' % qs
print(url)
res = requests.post(url)

print(res.status_code)
print(res.text)

body = res.json()
