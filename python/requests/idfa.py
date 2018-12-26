# -*- coding: utf-8 -*-
import pprint
import sys

import requests
import logging
logging.basicConfig(level=logging.DEBUG)


url = sys.argv[1]


def send_request(idfas):
    data = {
        'idfaList': ','.join(idfas),
        'idfa': 1,
        # 'appid': 388089858,
        'out_id': 30,
    }
    res = requests.get(url, params=data)
    pprint.pprint(res.json())


idfas = set()
for line in sys.stdin:
    idfa = line.strip()
    if idfa:
        idfas.add(idfa)

    if len(idfas) >= 200:
        send_request(idfas)
        idfas = set()

if len(idfas) > 0:
    send_request(idfas)
