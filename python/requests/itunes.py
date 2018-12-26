# -*- coding: utf-8 -*-
import logging
import time
import timeit

import requests

LOGGER = logging.getLogger(__name__)

url = 'https://itunes.apple.com/cn/app/id1434012154?mt=8'


def func1():
    ts = time.time()
    resp = requests.get(url)
    missing = resp.status_code == 404
    te = time.time()

    tc = int((te - ts) * 1000)

    # LOGGER.error('tc: {} ms'.format(tc))


def func2():
    ts = time.time()
    with requests.get(url, stream=True) as resp:
        missing = resp.status_code == 404
    te = time.time()

    tc = int((te - ts) * 1000)

    # LOGGER.error('tc: {} ms'.format(tc))


def func3():
    ts = time.time()
    with requests.head(url, stream=True) as resp:
        missing = resp.status_code == 404
    te = time.time()

    tc = int((te - ts) * 1000)

    # LOGGER.error('tc: {} ms'.format(tc))


_ = timeit.timeit('func1()', globals=locals(), number=100)
LOGGER.error(_)
_ = timeit.timeit('func2()', globals=locals(), number=100)
LOGGER.error(_)
_ = timeit.timeit('func3()', globals=locals(), number=100)
LOGGER.error(_)
