# -*- coding: utf-8 -*-


class AbstractLock(object):
    """
    """

    def __init__(self):
        self.locked = False

    def __enter__(self):
        self._lock()
        self.locked = True
        return self

    def __exit__(self, cls, err, trace):
        if self.locked:
            self._unlock()

    def _lock(self):
        raise NotImplementedError()

    def _unlock(self):
        raise NotImplementedError()



class AbstractExLock(AbstractLock):
    """
    抽象排他锁
    """
