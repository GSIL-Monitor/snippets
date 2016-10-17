# -*- coding: utf-8 -*-
from functools import wraps
import logging


logging.basicConfig(
    format='(%(levelname)-7s): %(message)s',
    level=logging.DEBUG
)


logger = logging.getLogger()


def cachable(store, key, timeout=None):
    logger.debug('cachable: %s', store)
    logger.debug('cachable: %s', key)
    logger.debug('cachable: %s', timeout)

    def _(func):

        def _cache_layer(*args, **kwargs):

            logger.debug('_cache_layer: %s', args)
            logger.debug('_cache_layer: %s', kwargs)

            return func(*args, **kwargs)

        return _cache_layer

    return _


@cachable(store='backend', key=lambda x: 'user_%s' % x, timeout=300)
def read_from_db(user_id):
    return user_id


logger.debug(read_from_db(1))
