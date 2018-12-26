# -*- coding: utf-8 -*-
import json
import logging
import uuid

import requests


def getIdfa():
    return str(uuid.uuid4()).upper()


idfas = []
for i in range(5):
    _ = {
        'ost': 1,
        'uuid': getIdfa(),
    }
    idfas.append(_)

url = 'http://dingding.test.58.com/ad/clickactivereport'

params = {
    'params': json.dumps(idfas),
}

resp = requests.post(url, params=params, timeout=10)
logging.error(resp.status_code)
logging.error(resp.text)
