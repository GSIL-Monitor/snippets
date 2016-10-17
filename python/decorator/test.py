# -*- coding: utf-8 -*-
import functools

import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger()


class Hello(object):

    def __init__(self, func):
        self.func = func

    def __call__(self):
        self.func()


def task(*args, **kwargs):
    invoked = bool(not args or kwargs)
    logger.info('wrapper: %s', args)
    logger.info('wrapper: %s', kwargs)

    logger.info(invoked)

    if not invoked:
        func, args = args[0], ()

    def wrapper(func):
        logger.info('wrapper: %s', func)

        def pre_hook(*args, **kwargs):
            logger.info('pre_hook')
            func(*args, **kwargs)

        return Hello(pre_hook)


    return wrapper if invoked else wrapper(func)


@task
def test1():
    logger.info('test1')


@task(default=True)
def test2():
    logger.info('test2')


logger.info('start!')

test1()
test2()
