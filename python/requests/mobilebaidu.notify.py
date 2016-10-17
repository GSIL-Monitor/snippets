# -*- coding: utf-8 -*-
import hashlib
import time
import urllib.parse
import uuid

import requests

AK = 'qianka'
SK = '6ccd2782289b2a357b53358eef4eea13'
CH = '1013684e'
IDFA_URL = 'http://ext.baidu.com/api/integral/v1/idfa/save'

def get_sign(idfa, timestamp):
    _ = 'ak=%sch=%sidfa=%stime=%s%s' % (AK, CH, idfa, timestamp, SK)
    print(_)
    m = hashlib.md5()
    m.update(_.encode('ascii'))
    return m.hexdigest()

idfa = str(uuid.uuid4()).upper()
timestamp = str(int(time.time()))

parameters = dict()
parameters['ch'] = CH
parameters['idfa'] = idfa

query = dict()
query['ak'] = AK
query['time'] = timestamp
query['sign'] = get_sign(idfa, timestamp)

qs = urllib.parse.urlencode(query)
url = '%s?%s' % (IDFA_URL, qs)
print(url)
print(parameters)

resp = requests.post(url, parameters)
print(resp.status_code)
print(resp.text)

body = resp.json()
if str(body['errno']) != '0':
    pass
