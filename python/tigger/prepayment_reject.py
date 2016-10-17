# -*- coding: utf-8 -*-
import sys

import requests


pk = sys.argv[1]

_ = requests.post('/api/prepayments/%s/reject' % pk)

print(_)
