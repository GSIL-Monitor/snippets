# -*- coding: utf-8 -*-
import logging

from abstract import AbstractExLock
import error


LOGGER = logging.getLogger(__name__)


class RedisExLock(AbstractExLock):
    """
    使用 redis 服务端做排他锁

    锁失败时，会抛出 error.FailToLockError 要注意捕捉

    client = redis.StrictRedis.from_url('...')
    lock_key = 'some-key'
    timeout = 60
    with RedisExLock(client, lock_key, 60) as lock:
        do_something_awsome()

    """

    def __init__(self, client, key, timeout):
        """
        Args:
            :client: redis.StrictRedis
            :key: str
            :timeout: int 秒
        """
        super().__init__()

        self.client = client
        self.key = key
        self.timeout = timeout

    def _lock(self):
        k = self.key
        _ = self.client.setnx(k, 1)
        if not _:
            # False
            raise error.FailToLockError('already locked for "{}"'.format(k))

        self.client.expire(k, self.timeout)
        LOGGER.debug('>>> lock "%s" acquired', self.key)

    def _unlock(self):
        if self.locked:
            self.client.delete(self.key)
        LOGGER.debug('>>> unlocked "%s"', self.key)


class QkCacheAdapter(object):
    """
    从 QiankaCache.get_cache(bind) 得到缓存实例对象
    到 Redis 客户端实例的适配器

    便于让两边的代码平滑衔接

    相当于

    inst = cache.get_cache('bind')
    adapter = QkCacheAdapter(inst)
    client = adapter.get_client(key)  # <== 得到 redis.StrictRedis 实例
    """

    def __init__(self, cache_inst):
        self.inst = cache_inst

    def get_client(self, k):
        rv = self.inst._get_connection(k)
        return rv


class QkRedisExLock(RedisExLock):
    """
    使用 qianka-cache 的 RedisCache 实例，以 redis 服务端做排他锁

    锁失败时，会抛出 error.FailToLockError 要注意捕捉

    _cache = cache.get_cache(bind)
    lock_key = 'some-key'
    timeout = 60
    with QkRedisExLock(_cache, lock_key, 60) as lock:
        do_something_awsome()
    """

    def __init__(self, cache_inst, key, timeout):
        adapter = QkCacheAdapter(cache_inst)
        client = adapter.get_client(key)
        super().__init__(client, key, timeout)
