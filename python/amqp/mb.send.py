# -*- coding: utf-8 -*-
import base64
import json
import lzma

import msgpack
import requests


url = 'http://127.0.0.1:3000/message/v3/send'

params = {
    'body': '',
    'connection': 'default',
    'exchange': 'amq.topic',
    'routing_key': 'test',
    'content_type': 'text/plain',
    'content_encoding': '',
}

# plain text
params['body'] = 'plain text'

resp = requests.post(url, params)
code = resp.status_code
print(code)

# json
o = {
    'marshal': 'json',
}

payload = base64.b64encode(json.dumps(o).encode('utf-8'))
params['body'] = payload
params['content_type'] = 'application/json'
resp = requests.post(url, params)
code = resp.status_code
print(code)

# msgpack
o = {
    'marshal': 'msgpack',
}

payload = base64.b64encode(msgpack.packb(o))
params['body'] = payload
params['content_type'] = 'application/msgpack'
resp = requests.post(url, params)
code = resp.status_code
print(code)

# lzma
b = b'hello world'
payload = base64.b64encode(lzma.compress(b))
params['body'] = payload
params['content_type'] = ''
params['content_encoding'] = 'lzma'
resp = requests.post(url, params)
code = resp.status_code
print(code)

# json+lzma
o = {
    'marshal': 'json',
}
b = lzma.compress(json.dumps(o).encode('utf-8'))
payload = base64.b64encode(b)
params['body'] = payload
params['content_type'] = 'application/json'
params['content_encoding'] = 'lzma'
resp = requests.post(url, params)
code = resp.status_code
print(code)

# JSON API
o = {
    'marshal': 'json',
}
b = lzma.compress(json.dumps(o).encode('utf-8'))
payload = base64.b64encode(b)
params['body'] = payload.decode('utf-8')
params['content_type'] = 'application/json'
params['content_encoding'] = 'lzma'
params['headers'] = {
    'X-CUSTOM-HEADER': 'custom value',
}

payload = json.dumps(params)

resp = requests.post(
    url, payload, headers={'Content-Type': 'application/json'})
code = resp.status_code
print(code)
