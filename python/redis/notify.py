# -*- coding: utf-8 -*-
import logging
import time
import uuid

import msgpack
import redis


QUEUE_NAME = 'qianka:notify:pending_send'

req = 1
r = redis.StrictRedis()

def get_idfa():
    return str(uuid.uuid4()).upper()


def send(ad_id, url, payload):
    global req
    p = [req, ad_id, url, payload, int(time.time())]
    logging.warning(p)
    _ = msgpack.packb(p)
    r.rpush(QUEUE_NAME, _)
    req += 1

while True:

    # send(1, 'http://127.0.0.1:4567/post', {
    #     'idfa': get_idfa(),
    #     'ipv4': '127.0.0.1',
    #     'appid': 1000,
    # })
    # send(2, 'http://127.0.0.1:4567/', {
    #     'idfa': get_idfa(),
    #     'ipv4': '127.0.0.2',
    #     'appid': 2000,
    # })
    send(50, 'http://127.0.0.1:4567', {
        'idfa': get_idfa(),
        'ipv4': '127.0.0.3',
        'appid': 3000,
    })
    time.sleep(3)
