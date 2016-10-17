# -*- coding: utf-8 -*-
import logging
import uuid

import requests



logging.basicConfig(level=logging.DEBUG)
idfa = str(uuid.uuid4()).upper()

res = requests.post('http://data.seeyouyima.com/marketing/activation-status.php?application=1', params={'idfa': idfa, 'appid': '123'})

print(res.status_code)
print(res.text)
