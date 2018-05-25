# -*- coding: utf-8 -*-
import logging
import pprint
import json

import requests

url = 'http://127.0.0.1:3000/a/5.0/app.report'

payload = json.dumps({'hello': 'world'})

headers = {
    # 'Content-Type': 'application/json; charset=utf8',
    # 'Content-Type': 'application/octet-stream',
    # 'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Type': '',
}

resp = requests.post(url, data=payload, headers=headers)

logging.error(pprint.pformat(resp.status_code))
logging.error(pprint.pformat(resp.text))
