# -*- coding: utf-8 -*-
import pprint
import sys

import requests


url = sys.argv[1]


def send_request(idfas):
    data = {
        'idfa': ','.join(idfas),
        'appid': 388089858,
    }
    res = requests.post(url, data=data)
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
