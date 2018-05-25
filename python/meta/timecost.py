# -*- coding: utf-8 -*-
import timeit

def stat():
    pass


_ = timeit.timeit(stmt='stat()', globals=globals())
print(_)
_ = timeit.timeit(stmt='stat()', globals=globals())
print(_)
_ = timeit.timeit(stmt='stat()', globals=globals())
print(_)

a = [1, 2, 3]
s = set(a)
d = {x: 1 for x in a}

_ = timeit.timeit(stmt='3 in a', globals=globals())
print(_)
_ = timeit.timeit(stmt='3 in s', globals=globals())
print(_)
_ = timeit.timeit(stmt='3 in d', globals=globals())
print(_)
