# -*- coding: utf-8 -*-
import os
import json
from urllib.request import Request

import common



env = os.environ.get('COMM_ENV', 'local')

logger = common.get_logger()

url = common.configs[env]['url']

req = Request(url + "communities/1", method='GET')

req.add_header('Accept', 'application/json')

try:
    res = common.opener.open(req)
    logger.info(res.code)
    body = res.fp.read().decode('UTF-8')
    logger.info(body)
    logger.info(json.loads(body))
except Exception as e:
    raise e
