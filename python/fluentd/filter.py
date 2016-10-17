# -*- coding: utf-8 -*-
import logging
import json
import sys

logger = logging.getLogger(__name__)
logger.handlers = []
handler = logging.FileHandler('/tmp/test.log')
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

for line in sys.stdin:
    try:
        tag, hostname, datetime = line.strip().split("\t")
        logger.info(line)
        logger.info(hostname)
        print("%s\t%s" % ("alog.api", datetime))
    except Exception as e:
        logger.exception(line)
