# -*- coding: utf-8 -*-
import sys

import requests

proxies = {
    'https': 'http://tigger:tigger321@hk01.proxy.gaoshou.me:8213',
    'http': 'http://tigger:tigger321@hk01.proxy.gaoshou.me:8213',
}


url = sys.argv[1]

resp = requests.get(url, stream=True, timeout=10, proxies=proxies)
print(resp.status_code)
print(resp.text)
