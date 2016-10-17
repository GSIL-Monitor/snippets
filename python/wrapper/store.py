# -*- coding: utf-8 -*-
import time

class Store(object):

    _store = {}

    def __init__(self):
        pass


    def __contains__(self, key):
        self._reap(key)
        return (key in self._store)


    def _reap(self, key):
        if key in self._store:
            if time.time() > self._store.get(key).get('expire'):
                self._store.pop(key)


    def _reap_all(self):
        key_to_remove = set()
        for key in self._store:
            if time.time() > self._store.get(key).get('expire'):
                key_to_remove.add(key)

        for k in key_to_remove:
            self._store.pop(k)


    def inspect(self):
        return self._store


    def get(self, key):
        self._reap(key)

        if key in self._store:
            return self._store[key].get('value')


    def set(self, key, value, expire=999999999):
        if key not in self._store:
            self._store[key] = {}
        self._store[key]['value'] = value
        self._store[key]['expire'] = time.time() + expire

