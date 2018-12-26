# -*- coding: utf-8 -*-
from httpclient import HttpClient

client = HttpClient()

resp = client.get('http://127.0.0.1/?c=4', query={'a': 1, 'b': 2})
print(resp.status_code)
print(resp.text)

resp = client.get('http://127.0.0.1/?c=4', query={'a': 1, 'b': 2})
print(resp.status_code)
print(resp.text)
