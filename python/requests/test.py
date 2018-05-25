# -*- coding: utf-8 -*-
import logging
import uuid

import requests



logging.basicConfig(level=logging.DEBUG)
idfa = str(uuid.uuid4()).upper()

params = {
    'idfa': '9B945147-1809-444C-B902-C0CEC75C6972,6BF4A74A-202A-4C7B-ADE8-D6652B9A39BF',
    'appid': '1359569295',
}
url = 'http://cqbygdt.geekgame.cn/qkqueryidfa'

res = requests.post(url, params)

print(res.status_code)
print(res.text)
