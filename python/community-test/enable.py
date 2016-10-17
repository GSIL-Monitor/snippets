# -*- coding: utf-8 -*-
import os
import json
from urllib.request import Request


env = os.environ.get('COMM_ENV', 'local')

import common

logger = common.get_logger()

url = common.configs[env]['url']

req = Request(url + "communities/1/action/display/show", method='PUT')

# req.add_header('Content-type', 'application/json;charset=UTF-8')
req.add_header('Content-length', '0')
req.add_header('Accept', 'application/json')

try:
    res = common.opener.open(req)
    logger.info(res.code)
    logger.info(json.loads(res.fp.read().decode('UTF-8')))
except Exception as e:
    raise e
