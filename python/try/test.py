# -*- coding: utf-8 -*-

import asyncio


try:
    raise RuntimeError('test')
except asyncio.TimeoutError as err:
    print('err catched')
else:
    print('else clause')
