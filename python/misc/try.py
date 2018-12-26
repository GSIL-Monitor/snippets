# -*- coding: utf-8 -*-
try:
    raise RuntimeError()
except KeyError:
    raise ValueError()
finally:
    print('finally')
