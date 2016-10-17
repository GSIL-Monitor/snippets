# -*- coding: utf-8 -*-
import time


MAX_EXPIRE = 9999999999

class Cache(object):

    store = {}

    def inspect(self):
        return self.store

    def set(self, key, value, expire=None):
        self.store[key] = {}
        self.store[key]['value'] = value
        if expire is None:
            self.store[key]['ts'] = MAX_EXPIRE
        else:
            self.store[key]['ts'] = time.time() + expire

    def get(self, key):
        _ = self.store.get(key)
        if _:
            if _['ts'] < time.time():
                del self.store[key]
                rv = None
            else:
                rv = self.store[key]['value']
        else:
            rv = None

        return rv

cache = Cache()

payload = 'abc'

for i in range(10000000):
    cache.set(i, payload)

print('set')
time.sleep(30)
