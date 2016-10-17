# -*- coding: utf-8 -*-
import hashlib
import io
import logging
import time
import urllib.parse
import uuid


import requests



logging.basicConfig(level=logging.DEBUG)

def get_idfa():
    return str(uuid.uuid4()).upper()

def get_secret_baidu_ime(_from, timestamp, token, idfa):

    feed = ('%s%s%s%s' % (_from, timestamp, token, idfa)).encode('UTF-8')

    print(feed)

    m = hashlib.md5()
    m.update(feed)
    rv = m.hexdigest()
    return rv

with open('txt') as f:
    idfa = f.read()

data = io.BytesIO()
data.write(idfa.encode('UTF-8'))
data.seek(0)


url = 'http://r6.mo.baidu.com/v5/idfa/status'
timestamp = int(time.time())

_from = '1013684a'
token = 'FpOd3tLRjVaa1FBpZURPcklBQXZFNnpwM9ZrYXBoWk21'
secret = get_secret_baidu_ime(_from, timestamp, token, idfa)

params = {}
params['from'] = _from
params['time'] = timestamp
params['secret'] = secret

qs = urllib.parse.urlencode(params)

url = url + '?' + qs

res = requests.post(url, headers={'Content-Type': 'text/plan'}, data=data)

print('code: %s' % res.status_code)
print('response: %s' % res.text)
print('decoded obj: %s' % res.json())
