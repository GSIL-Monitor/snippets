# -*- coding: utf-8 -*-
import sys

import redis


class Scanner(object):

    def __init__(self):
        self.client = redis.StrictRedis.from_url(
            'redis://n1540.ops.gaoshou.me/33')

    def scan(self, pattern):

        cursor = 0

        while True:
            # print('scan from cursor: {}'.format(cursor))
            cursor, keys = self._scan(cursor, pattern)

            if cursor == 0:
                break

            for key in keys:
                print('found: {}'.format(key))

    def _scan(self, cursor, pattern):
        _ = self.client.scan(
            cursor,
            pattern,
            1000)

        return _

pattern = sys.argv[1]
Scanner().scan(pattern)
