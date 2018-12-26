# -*- coding: utf-8 -*-
import logging
import time

import requests


LOGGER = logging.getLogger(__name__)

while True:
    try:
        resp = requests.get('https://qianka.com')
        time.sleep(1)
    except requests.exceptions.RequestException as err:
        LOGGER.exception('err')
