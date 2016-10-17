# -*- coding: utf-8 -*-
import logging
import re

CURRENCY_PATTERN = re.compile(r'获得(\d+\.?\d*?)金')

orig = '你好，获得1.00金'

_m = CURRENCY_PATTERN.search(orig)
if _m:
    currency = _m.group(1).rstrip('.0')
    logging.warning(currency)
    orig = CURRENCY_PATTERN.sub('获得 %s 金' % currency, orig)

logging.warning(orig)
