# -*- coding: utf-8 -*-
import logging
import logging.config
import random
import time

import logging_config

logger = logging.getLogger()
status = logging.getLogger('status')

while True:
    s = random.random()
    s = 2
    time.sleep(s)

    logger.debug('调试！！！')
    logger.warning('警告！！！')
    status.warning('警告！！！')

    try:
        raise RuntimeError
    except Exception:
        logger.exception('hello')
