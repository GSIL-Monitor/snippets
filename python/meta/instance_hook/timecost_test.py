# -*- coding: utf-8 -*-
import logging
import timeit

from instance_hook import ImplA


logger = logging.getLogger(__name__)

a = ImplA()

def stat(name, optons):
    pass

_ = timeit.timeit(
    stmt='a.set("k", "v")', globals=globals())
print(_)
a.beacon_before('set', stat)
a.setup_hook()
_ = timeit.timeit(
    stmt='a.set("k", "v")', globals=globals())
print(_)
a.teardown_hook()
_ = timeit.timeit(
    stmt='a.set("k", "v")', globals=globals())
print(_)
