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
    time.sleep(s)

    logger.debug('debug')
    logger.warning('warning')
    status.warning('warning')
