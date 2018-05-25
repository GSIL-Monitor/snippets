# -*- coding: utf-8 -*-
import logging
import pprint

from instance_hook import ImplA

logger = logging.getLogger(__name__)

def stat(name, options):
    logger.debug('name {}'.format(name))
    logger.debug('options {}'.format(options))

    tc = options['timecost']
    tc = int(tc * 1000000000)
    logger.debug(tc)

logging.basicConfig(level=logging.DEBUG)
a = ImplA()
a.beacon_after('set', stat)
a.setup_hook()
a.set("k", "v")
