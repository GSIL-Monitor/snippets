# -*- coding: utf-8 -*-
from functools import wraps


def inner():
    pass


@wraps(inner)
def outer():
    return inner()
