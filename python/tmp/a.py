# -*- coding: utf-8 -*-
from fnmatch import fnmatch
def _validate_value(_range, v):

    if type(_range) != list:
        _range = [_range]

    for r in _range:

        if type(r) in (list, tuple) and len(r) == 2:
            if _validate_range(r[0], r[1], str(v)):
                return True
        elif _validate_single_value(r, str(v)):
            return True

    return False


def _validate_single_value(c, v):
    return fnmatch(v, c)


def _validate_range(s, e, v):
    return s <= v <= e


_ = _validate_value('201*', '2015')

print(_)
