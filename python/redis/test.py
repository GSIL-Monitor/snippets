# -*- coding: utf-8 -*-
import time
from unittest import TestCase

import msgpack
import redis
import redis.exceptions

from cache import RedisCache


config = [
    ('redis://localhost', 1),
    ('redis://localhost', 2)
]


class RedisCacheTestCase(TestCase):

    def setUp(self):
        self.cache = RedisCache(config, marshal_module=msgpack,
                                key_prefix='test')


    def tearDown(self):
        r = redis.StrictRedis.from_url('redis://localhost')
        r.flushdb()
        r.connection_pool.disconnect()


    def test_init(self):
        assert isinstance(self.cache, RedisCache)


    def test_key_to_conn(self):
        assert isinstance(self.cache._key_to_conn('1'), redis.StrictRedis)


    def test_set_get(self):
        assert self.cache.set('hello', [1, 2])
        assert self.cache.get('hello') == [1, 2]


    def test_set_get_with_timeout(self):
        assert self.cache.set('hello', '1', timeout=10)
        assert self.cache.get('hello') == 1


    def test_set_get_with_timeout_expired(self):
        assert self.cache.set('hello', {'a': 'hello'}, timeout=1)
        time.sleep(1.1)
        assert self.cache.get('hello') == None


    def test_delete(self):
        assert self.cache.set('hello', [2, 3])
        assert self.cache.delete('hello')
        assert self.cache.delete('world') == 0
        assert self.cache.get('hello') == None


    def test_add(self):
        assert self.cache.add('hello', [3, 4])
        assert self.cache.get('hello') == [3, 4]
        assert self.cache.add('hello', [4, 5]) == 0
        assert self.cache.get('hello') == [3, 4]


    def test_clear(self):
        assert self.cache.add('hello', 1)
        assert self.cache.add('world', 2)
        assert self.cache.add('mike', 3)
        assert self.cache.clear()
        assert self.cache.get('hello') == None
        assert self.cache.get('world') == None
        assert self.cache.get('mike') == None


    def test_get_many(self):
        assert self.cache.set('hello', 1)
        assert self.cache.set('world', ['a', 'c'])
        assert self.cache.set('mike', {'key': 'value'})
        assert (self.cache.get_many('world', 'mike', 'hello') ==\
                [[b'a', b'c'], {b'key': b'value'}, 1])


    def test_set_many(self):
        input = {
            'mike': 'hello world',
            'a': 200,
            'c': [400, 300],
        }
        assert self.cache.set_many(input)

        assert self.cache.get('mike') == b'hello world'
        assert self.cache.get('a') == 200
        assert self.cache.get('c') == [400, 300]


    def test_delete_many(self):
        assert self.cache.set('hello', 1)
        assert self.cache.set('world', 1)
        assert self.cache.set('alpha', 1)
        assert self.cache.set('beta', 1)

        assert self.cache.delete_many('hello', 'world',
                                      'alpha', 'beta', 'charlie') ==\
                                      [True, True, True, True, False]


    def test_inc(self):
        assert self.cache.inc('hello', 1) == 1
        assert self.cache.inc('hello', delta=10) == 11

        self.cache.set('hello', 20)
        with self.assertRaises(redis.exceptions.ResponseError):
            self.cache.inc('hello')


    def test_dec(self):
        assert self.cache.dec('hello') == -1
        assert self.cache.dec('hello', delta=10) == -11

        self.cache.set('hello', 20)
        with self.assertRaises(redis.exceptions.ResponseError):
            self.cache.dec('hello')
