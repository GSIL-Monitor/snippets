# -*- coding: utf-8 -*-
import logging
import socket
import sys

from kafka_logging import KafkaLoggingHandler

class HostnameFilter(logging.Filter):
    hostname = ''

    def __init__(self):
        self.hostname = socket.gethostname()


    def filter(self, record):
        record.hostname = self.hostname
        return True

hostname = HostnameFilter()

h = logging.Formatter('[%(asctime)s %(levelname)-7s %(hostname)s(%(name)s) '
                      '<%(process)d> %(filename)s:%(lineno)d] %(message)s')
f = logging.Formatter('[%(asctime)s %(levelname)-7s (%(name)s) '
                      '<%(process)d> %(filename)s:%(lineno)d] %(message)s')

console = logging.StreamHandler(sys.stderr)
console.setLevel(logging.INFO)
console.setFormatter(f)

kafka = KafkaLoggingHandler('127.0.0.1', 'test')
kafka.setLevel(logging.INFO)
kafka.setFormatter(h)
kafka.addFilter(hostname)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.handlers.clear()
logger.addHandler(console)

logger = logging.getLogger('status')
logger.setLevel(logging.INFO)
logger.handlers.clear()
logger.addHandler(kafka)
logger.propagate = False
