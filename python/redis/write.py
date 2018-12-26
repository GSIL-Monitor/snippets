# -*- coding: utf-8 -*-
import uuid

import tqdm

from redis import StrictRedis

kp = 'eeyore:1234567890-11111-{}'


def randomIdfa():
    return str(uuid.uuid4()).upper()


client = StrictRedis.from_url('redis://127.0.0.1/345')

with tqdm.tqdm() as bar:
    buf = {}
    for i in range(20000000):
        k = kp.format(randomIdfa())
        buf[k] = 1
        if len(buf) == 10000:
            client.mset(buf)
            buf = {}
        bar.update(1)
