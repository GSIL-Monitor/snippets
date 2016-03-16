# -*- coding: utf-8 -*-
import logging
import logging.config
import random
import time

import logging_config

logging.config.dictConfig(logging_config.logging_config)

logger = logging.getLogger()

while True:
    s = random.random()
    time.sleep(s)

    logger.debug('debug')
    logger.warning('warning')
