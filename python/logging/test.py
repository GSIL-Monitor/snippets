# -*- coding: utf-8 -*-
import logging
import logging.config
import time

logging.config.fileConfig('logging.ini')

logger = logging.getLogger().getChild('test.app')



while True:
    logger.info('an info')
    logger.debug('a debug')
    time.sleep(1)
