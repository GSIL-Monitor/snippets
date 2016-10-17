# -*- coding: utf-8 -*-
import collections
import hashlib
import io
import logging
import time
import urllib.parse
import uuid
import sys

import requests

logging.basicConfig(level=logging.DEBUG)

def get_idfa():
    return str(uuid.uuid4()).upper()


_from = '1013684a'
idfa = sys.stdin.read().strip()
sign = 'f3d6b2544b4bec1c70bc6357f5d678c95d944faf'

data = collections.OrderedDict()
data['from'] = _from
data['idfa'] = idfa
data['sign'] = sign
data['c'] = 'jp'
data['e'] = 'url'
data['pl'] = 'i5'
data['url'] = 'https://itunes.apple.com/WebObjects/MZStore.woa/wa/search?media=software&country=CN'

p = urllib.parse.urlencode(collections.OrderedDict(data))
logging.debug(p)

resp = requests.get('http://r6.mo.baidu.com/v4/', params=p, allow_redirects=False)
logging.debug(resp.status_code)
logging.debug(resp.text)
