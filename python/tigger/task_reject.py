# -*- coding: utf-8 -*-
import sys

import requests


task_id = sys.argv[1]

_ = requests.post('http://127.0.0.1:5000/api/ios_tasks/%s/reject' % task_id)

print(_)
