# -*- coding: utf-8 -*-
import time

from redis import StrictRedis


class CacheLock(object):

    def __init__(self, client, key, timeout=300):
        self.client = client
        self.key = key
        self.timeout = timeout

    def __enter__(self):
        _ = self.client.setnx(self.key, 1)
        if not _:
            raise RuntimeError('race condition')
        else:
            self.client.expire(self.key, self.timeout)

    def __exit__(self, *args):
        print(args)
        self.client.delete(self.key)


client = StrictRedis.from_url('redis://127.0.0.1')


with CacheLock(client, 'hello'):
    print('hello')
    time.sleep(2)
