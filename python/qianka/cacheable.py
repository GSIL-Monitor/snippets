# -*- coding: utf-8 -*-
from functools import wraps
import time

from qianka_cache import QKCache

cache = QKCache()
cache.configure({
    'CACHE_ENABLED': True,
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_NODES': {
        'default': ('memory', 128),
    }
})


def cacheable(key, timeout, bind, condition=None):
    """
    对函数进行包装的缓存装饰器，默认行为如下
    """

    if not isinstance(key, str) and not callable(key):
        raise ValueError('key参数只允许str或者函数')

    if condition and not callable(condition):
        raise ValueError('condition必须是函数')

    def w(fn):

        # 嵌套情况复杂，如果包装的是静态方法
        # 将无法判断调用时的第一个参数是否为
        # 对象实例本身，造成参数错误
        if isinstance(fn, staticmethod):
            raise ValueError('@cacheable需在@staticmethod下面')

        @wraps(fn)
        def cacheWrapper(*args, **kwargs):

            k = key
            if callable(key):
                k = key(*args, **kwargs)

            rv = cache.get(k)
            if rv is not None:
                return rv

            rv = fn(*args, **kwargs)

            # 默认需要设置缓存
            do_set = True
            if condition and callable(condition):
                do_set = False
                if condition(rv):
                    do_set = True

            if do_set:
                cache.set(k, rv, timeout=timeout)

            return rv
        return cacheWrapper

    return w


class SomeService(object):

    @staticmethod
    @cacheable(
        key=lambda x, y: 'staticSum_{}_{}'.format(x, y),
        timeout=1,
        bind='default',
    )
    def staticSum(a, b):
        time.sleep(1)
        return a + b

    @cacheable(
        key=lambda self, x, y: 'sum_{}_{}'.format(x, y),
        timeout=15,
        bind='default',
    )
    def sum(self, a, b):
        time.sleep(2)
        return a + b


ss = SomeService()

_ = SomeService.staticSum(1, 2)
print(_)
print('---------')
_ = SomeService.staticSum(1, 2)
print(_)
print('---------')
time.sleep(1)
_ = SomeService.staticSum(1, 2)
print(_)
# ss.staticSum(1, 2)

_ = ss.sum(2, 3)
print(_)
_ = ss.sum(3, 4)
print(_)
_ = ss.sum(2, 3)
print(_)
