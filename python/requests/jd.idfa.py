# -*- coding: utf-8 -*-
import hashlib
import json
import pprint
import uuid
import sys

import requests


SECRET = 'NBQK-7J89-JKDS-RMNW-DEBC-2H8D-KH'


def sign_payload(payload):
    m = hashlib.md5()
    m.update(payload['body'].encode('ascii'))
    m.update(SECRET.encode('ascii'))
    payload['sign'] = m.hexdigest().upper()


idfas = set()
body = []
# idfa = (str(uuid.uuid4()).upper())

for _ in sys.stdin:
    idfa = _.strip()
    if not idfa:
        continue
    idfa = idfa.split('\t')[0]
    idfas.add(idfa)
    body.append(dict(idfa=idfa, clientType=4))

body = json.dumps(body)
# print(body)

payload = dict(
    body=body
)

sign_payload(payload)

payload['unionId'] = 350268123
# print(payload)

res = requests.post(
    'http://adcollect.m.jd.com/queryAtivationByIdfa.do',
    data=payload)

if res.status_code == 200:
    rv = dict()
    payload = res.json()['result']
    for _ in payload:
        idfa = _['idfa']
        if idfa in idfas:
            rv[idfa] = (_['ativation'] and 1) or 0

pprint.pprint(rv)
