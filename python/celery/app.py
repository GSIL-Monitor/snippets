# -*- coding: utf-8 -*-
from fnmatch import fnmatch
from functools import reduce
import logging
import random
import sys

from celery import Celery
from celery import signals
from kombu import Exchange, Queue

celery = Celery()
logger = logging.getLogger(__name__)

celery.conf.broker_url = 'amqp://guest:guest@127.0.0.1:5672//'
celery.conf.task_ignore_result = True
celery.conf.task_create_missing_queues = False
celery.conf.task_default_queue = 'celery.default'
celery.conf.task_default_exchange = 'default'
celery.conf.task_default_exchange_type = 'topic'
celery.conf.task_default_delivery_mode = 'transient'
celery.conf.task_result_exchange = 'celery.result'
celery.conf.task_result_persistent = False

defaultEx = Exchange('default', type='topic', durable=True)

celery.conf.task_queues = (
    Queue(
        'celery.default', defaultEx, routing_key='default',
        durable=False, auto_delete=True
    ),
    Queue(
        'celery.slow', defaultEx, routing_key='slow.#',
        durable=False, auto_delete=True
    ),
)





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


def route_task(name, args, kwargs, options, task=None, **kw):
    print(name)
    print(args)
    print(kwargs)
    print(options)
    print(task)
    print(kw)
    _ = fnmatch(name, 'slow.*')
    print(_)
    if fnmatch(name, 'slow.*'):
        return {
            'exchange': 'default',  # TODO:
            'exchange_type': 'topic',
            'routing_key': 'slow.' + name,
        }


celery.conf.task_routes = [route_task,]

import slow
