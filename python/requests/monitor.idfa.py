# -*- coding: utf-8 -*-
import logging
import time

import requests


LOGGER = logging.getLogger(__name__)
URL = 'http://n1509.ops.gaoshou.me:3000/.json'


class Monitor(object):

    def monitor(self):
        while True:
            LOGGER.warning('do monitor')
            self.do()
            time.sleep(10)

    def do(self):
        data = self.fetch()
        if data is None:
            LOGGER.error('request ERROR!')
            return

        worker, mobileApps = data

        l1 = len(worker)
        l2 = len(mobileApps)

        if l1 == l2:
            return

        LOGGER.error('%d <=> %d, error!', l1, l2)

    def fetch(self):
        try:
            resp = requests.get(URL)
            assert resp.status_code == 200
            result = resp.json()
            return result['interludeWorkerStatus'], result['mobileApps']
        except Exception as e:
            LOGGER.exception('')
            return None


if __name__ == '__main__':
    logFormat = '[%(asctime)s %(levelname)-7s %(name)s:%(lineno)d] %(message)s'
    logging.basicConfig(level=logging.INFO, format=logFormat)
    Monitor().monitor()
