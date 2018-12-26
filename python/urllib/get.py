# -*- coding: utf-8 -*-
from urllib.parse import urlencode
from urllib.request import Request, urlopen

url = 'http://localhost'

params = urlencode({
    'token': '18923172',
    'message': '你好',
})

url += '?' + params

req = Request(url)
urlopen(req)
