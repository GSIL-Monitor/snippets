# -*- coding: utf-8 -*-
import logging
from logging.handlers import DatagramHandler
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

class QiankaUDPHandler(DatagramHandler):

    topic = None

    def __init__(self, topic, host, port):
        self.topic = topic
        DatagramHandler.__init__(self, host, port)


    def emit(self, record):
        s = "%s\t%s" % (self.topic, self.format(record))
        self.send(s.encode('utf-8'))


hostname = HostnameFilter()

h = logging.Formatter('[%(asctime)s %(levelname)-7s %(hostname)s(%(name)s) '
                      '<%(process)d> %(filename)s:%(lineno)d] %(message)s')
f = logging.Formatter('[%(asctime)s %(levelname)-7s (%(name)s) '
                      '<%(process)d> %(filename)s:%(lineno)d] %(message)s')

console = logging.StreamHandler(sys.stderr)
console.setLevel(logging.INFO)
console.setFormatter(f)

qianka = QiankaUDPHandler('hera', 'n1397.ops.gaoshou.me', 5252)
qianka.setLevel(logging.INFO)
qianka.setFormatter(f);
qianka.addFilter(hostname)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.handlers.clear()
logger.addHandler(console)
logger.addHandler(qianka)
