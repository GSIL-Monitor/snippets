# -*- coding: utf-8 -*-
import json
import pprint
import time

import requests


def send(i):
    url = 'http://localhost:8080/message/kafka/v1/send'
    b = json.dumps({
        'hello': 'world',
        'int': i,
    })

    data = json.dumps({
        'content_type': 'application/json',
        'connection': 'default',
        'topic': 'test',
        'body': b,
    })

    headers = {
        'Content-Type': 'application/json',
    }

    resp = requests.post(url, data, headers=headers, timeout=5)


i = 0
while True:
    i += 1
    send(i)
    time.sleep(1)
