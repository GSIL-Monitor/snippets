# -*- coding: utf-8 -*-
import json
import logging
import pprint
import sys

import requests

url = 'https://api.enhancedsteam.com/pricev3/'
params = {
    'appid': sys.argv[1],
    'stores': 'steam',
    'cc': 'cn',
}

resp = requests.get(url, params=params, timeout=10)
logging.error(resp.status_code)
result = json.loads(resp.text)
logging.error('\n' + pprint.pformat(result))
