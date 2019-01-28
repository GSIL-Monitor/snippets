# -*- coding: utf-8 -*-


class LockError(Exception):
    pass


class FailToLockError(LockError):
    pass
