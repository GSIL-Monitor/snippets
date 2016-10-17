# -*- coding: utf-8 -*-
import hashlib
import time
import sys
import urllib.parse
import uuid

import requests

AK = 'qianka'
SK = '6ccd2782289b2a357b53358eef4eea13'
CH = '1013684e'
IDFA_URL = 'http://ext.baidu.com/api/integral/v1/idfa/query'

def get_sign(idfa, timestamp):
    _ = 'ak=%sidfa=%stime=%s%s' % (AK, idfa, timestamp, SK)
    print(_)
    m = hashlib.md5()
    m.update(_.encode('ascii'))
    return m.hexdigest()

idfas = []
for line in sys.stdin:
    idfa = line.strip()
    if idfa:
        idfas.append(idfa)

idfa = ','.join(idfas)
timestamp = str(int(time.time()))

parameters = dict()
parameters['ak'] = AK
parameters['idfa'] = idfa
parameters['time'] = timestamp
parameters['sign'] = get_sign(idfa, timestamp)

resp = requests.get(IDFA_URL, parameters)
print(resp.status_code)
print(resp.text)

body = resp.json()
import pprint
pprint.pprint(body)
