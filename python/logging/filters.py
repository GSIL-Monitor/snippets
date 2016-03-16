# -*- coding: utf-8 -*-
import logging
import socket

class HostnameFilter(logging.Filter):
    hostname = ''

    def __init__(self):
        self.hostname = socket.gethostname()


    def filter(self, record):
        record.hostname = self.hostname
        return True
