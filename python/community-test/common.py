# -*- coding: utf-8 -*-
import logging
import sys

from urllib.request import HTTPRedirectHandler, build_opener
from urllib.response import addinfourl

from colorlog import ColoredFormatter



configs = {
    'local': {
        'url': 'http://localhost:8080/',
    },
    'pg': {
        'url': 'http://xapp20-053.i.ajkdns.com:8080/'
    },
    'prod': {
        'url': 'http://community.internal.a.ajkdns.com/'
    }
}

def get_logger():
    hdl = logging.StreamHandler(sys.stdout)
    logger = logging.getLogger('bespoke-remote')
    del logger.handlers[:]
    logger.setLevel(logging.DEBUG)
    hdl.setLevel(logging.DEBUG)
    formatter = ColoredFormatter(
        "[%(asctime)s %(log_color)s%(levelname)-8s%(reset)s] %(message)s",
        datefmt=None,
        reset=True,
        log_colors = {
            'DEBUG': 'bold_cyan',
            'INFO': 'bold_green',
            'WARNING': 'bold_yellow',
            'ERROR': 'bold_red',
            'CRITICAL': 'bold_red',
        }
    )
    hdl.setFormatter(formatter)
    logger.addHandler(hdl)
    return logger


class SimpleSmartHandler(HTTPRedirectHandler):

    def http_error_303(self, url, fp, errcode, errmsg, headers, data=None):
        return addinfourl(fp, headers, url, errcode)

opener = build_opener(SimpleSmartHandler)
