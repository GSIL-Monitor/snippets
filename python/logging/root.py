# -*- coding: utf-8 -*-
import logging
import logging.config
import sys

from aves import Application
from aves.logging import get_logger

app = Application()
app.start()

logger = get_logger('test.app')
logger.info('hello world')

logging.basicConfig()
rlogger = logging.getLogger()

rlogger.debug('debug')
rlogger.info('info')
rlogger.warn('warn')
rlogger.error('error')


slogger = logging.getLogger('status')
slogger.debug('debug')
slogger.info('info')
slogger.warn('warn')

l = slogger.getChild('impl')
l.debug('debug')


vlogger = logging.getLogger('verbose').getChild('impl').getChild('base')
vlogger.debug('debug')
vlogger.info('info')
vlogger.warn('warn')
vlogger.error('error')


logger.error('hello world2')
