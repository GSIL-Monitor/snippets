# -*- coding: utf-8 -*-
import timeit

_ = timeit.timeit(
    stmt='a & b',
    setup='a = 4; b = 1|2|4|8'
)
print(_)

_ = timeit.timeit(
    stmt='a in funcs',
    setup='a = "get"; funcs = ["inc", "dec", "get", "set"]'
)
print(_)

_ = timeit.timeit(
    stmt='a in funcs',
    setup='a = "get"; funcs = set(["inc", "dec", "get", "set"])'
)
print(_)
