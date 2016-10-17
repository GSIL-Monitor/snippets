# -*- coding: utf-8 -*-
from functools import update_wrapper
from store import Store


store = Store()

print('init')


class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.keys())))


def wrap(*args, **kwargs):
    print(args)
    print(kwargs)


def cache(timeout, key=None):

    def _(func):

        def wrap(*args, **kwargs):
            print('wrap args: ' + str(args))
            print('wrap kwargs: ' + str(kwargs))

            key = ('internal_cache', func, args, hashabledict(kwargs))

            print('wrap key: ' + str(key))

            if key in store:
                print('cache hit!')
                _ = store.get(key)
                if hasattr(_, 'copy'):
                    return _.copy()
                return _

            print('cache miss!')
            _ = func(*args, **kwargs)
            store.set(key, _, timeout)
            if hasattr(_, 'copy'):
                return _.copy()
            return _


        update_wrapper(wrap, func)

        return wrap

    return _


@cache(600)
def get_apps(name):
    print('heavy loading...')
    return {'a': 1, 'b': 2}


print('run!')

apps = get_apps('hello')
print(apps)
apps.pop('a')
apps = get_apps('hello')
print(apps)
apps = get_apps('hello')
print(apps)
