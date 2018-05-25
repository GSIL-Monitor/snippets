# -*- coding: utf-8 -*-
from datetime import datetime
import logging
import sys

s = sys.argv[1]
l = len(s)

if l > 33:
    s = s[0:33]

logging.error('s: ' + s)

s = s.replace('GMT ', 'GMT +')

logging.error('s: ' + s)

d = datetime.strptime(s, '%a %b %d %Y %H:%M:%S %Z %z')
logging.error(d)
