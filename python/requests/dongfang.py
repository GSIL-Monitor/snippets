# -*- coding: utf-8 -*-
import logging
import time
import uuid

import requests


logging.basicConfig(level=logging.DEBUG)

clickUrl = 'http://jfqapi.76iw.com/scoreboard/qiankaClick'

url = 'http://jfqapi.76iw.com/scoreboard/qkReport'

idfa = str(uuid.uuid4()).upper()
ip = '127.0.0.1'
apple_id = '1366535263'

params = {
    'idfa': idfa,
    'ip': ip,
    'appid': apple_id,
}
logging.debug(params)

ts = time.time()
resp = requests.post(clickUrl, data=params)
te = time.time()
tc = int((te - ts) * 1000)
logging.debug('timecost: {}ms'.format(tc))
logging.debug('http_code: {}'.format(resp.status_code))
logging.debug('body: {}'.format(resp.text))

ts = time.time()
resp = requests.post(url, data=params)
te = time.time()
tc = int((te - ts) * 1000)
logging.debug('timecost: {}ms'.format(tc))
logging.debug('http_code: {}'.format(resp.status_code))
logging.debug('body: {}'.format(resp.text))
