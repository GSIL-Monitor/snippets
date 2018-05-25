# -*- coding: utf-8 -*-
import logging
import pprint
import timeit
import time
import threading

from instance_hook import ImplA


logger = logging.getLogger(__name__)

a = ImplA()
def stat(name, options):
    # logger.debug('name: {}'.format(name))
    # logger.debug('options: {}'.format(options))
    pass

def switch():
    global a
    while True:
        a.setup_hook()
        logger.debug('hook up')
        time.sleep(0.1)
        logger.debug('hook down')
        a.teardown_hook()
        time.sleep(0.1)


logging.basicConfig(level=logging.DEBUG)

a.beacon_before('set', stat)
a.setup_hook()

t = threading.Thread(target=switch)
t.start()

_ = timeit.timeit(
    stmt='a.set("k", "v")', number=1000000, globals=globals())
pprint.pprint(_)
