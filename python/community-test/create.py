# -*- coding: utf-8 -*-
import json
from urllib.request import Request, urlopen

import common

logger = common.get_logger()

url = common.configs['local']['url']

comm = {
    'name': '新建的测试小区',
    'city_id': 11,
    'area_code': '000100010001',
    'address': '新建测试小区的地址',
    'floor_area_ratio': '新建测试小区的容积率',
}


req = Request(url + "communities", method='POST')

req.data = json.dumps(comm).encode('UTF-8')

req.add_header('Content-type', 'application/json;charset=UTF-8')
req.add_header('Accept', 'application/json')

try:
    res = urlopen(req)
    logger.info(res.code)
    logger.info(json.loads(res.fp.read().decode('UTF-8')))
except Exception as e:
    raise e
