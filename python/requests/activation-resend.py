# -*- coding: utf-8 -*-
import base64
import simplejson as json

import requests


MESSAGE_BROKER_URL = 'http://10.45.32.112/message/v1/send'


def send(
        payload, routing_key, exchange_name='hera.topic', bind='default',
        flag='json'):

    if flag == 'text':
        body = payload
    elif flag == 'json':
        body = json.dumps(payload).encode('ascii')
        body = base64.b64encode(body)
    else:
        raise RuntimeError('unknown flag: {}'.format(flag))

    data = {
        'connection': bind,
        'exchange': exchange_name,
        'body': body,
        'flag': 'json',
    }

    resp = requests.post(MESSAGE_BROKER_URL, data=data)

    return resp.status_code == 200
