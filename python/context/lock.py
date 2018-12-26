# -*- coding: utf-8 -*-
import contextlib


class LockFailedError(Exception):
    pass


class AbstractLock(contextlib.ContextManager):

    def __init__(self):
        self._locked = False

    def __enter__(self):
        locked = self._do_lock()
        if not locked:
            raise LockFailedError('cannot lock')
        return self

    def __exit__(self, exc_type, exc_value, trackback):
        if self._locked:
            self._do_unlock()
        return

    def _do_lock(self):
        """
        @override 覆盖这个方法，修改调用参数
        """
        rv = self._lock()
        return rv

    def _do_unlock(self):
        """
        @override 覆盖这个方法，修改调用参数
        """
        rv = self._unlock()
        return rv

    def _lock(self, *args, **kwargs):
        """
        True 加锁成功
        False 不成功
        """
        raise NotImplementedError()

    def _unlock(self, *args, **kwargs):
        raise NotImplementedError()


class RedisLock(AbstractLock):

    def __init__(self, **data):
        self.data = data

    # ...


SomeService = None
userId = 12837128

with RedisLock(key='some-lock-key', userId=userId, timeout=300):
    SomeService.doBiz()
