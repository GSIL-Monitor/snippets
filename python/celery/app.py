# -*- coding: utf-8 -*-
from functools import reduce
import logging
import random
import sys

from celery import Celery
from celery import signals

celery = Celery()
logger = logging.getLogger(__name__)




def _add(a, b):
    return a + b

@celery.task(ignore_result=True)
def add(*args):
    # _ = int(random.random() * 10)
    # if _ < 5:
    #     raise RuntimeError('error')
    print(reduce(_add, args))
    logger.error(reduce(_add, args))


fmt = (
    '[%(asctime)s %(levelname)7s %(name)s] %(message)s'
)
f = logging.Formatter(fmt)
h = logging.StreamHandler(sys.stderr)
h.setFormatter(f)

# crootLogger = logging.getLogger()
# crootLogger.setLevel(logging.DEBUG)
# crootLogger.handlers.clear()
# crootLogger.addHandler(h)


# logging.getLogger('celery')


@signals.after_setup_logger.connect
# def setup_logging_hook(logger, lvl, logfile, format, colorize):
def setup_logging_hook(*args, **kwargs):
    print(args)
    print(kwargs)

    logger = kwargs['logger']
    logger.setLevel(logging.WARNING)
    logger.handlers.clear()
    logger.addHandler(h)


@signals.after_setup_task_logger.connect
# def setup_logging_hook(logger, lvl, logfile, format, colorize):
def setup_task_logging_hook(*args, **kwargs):
    print(args)
    print(kwargs)

    logger = kwargs['logger']
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    logger.addHandler(h)
