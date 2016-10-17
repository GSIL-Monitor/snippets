# -*- coding: utf-8 -*-
import sys

import requests


task_id = sys.argv[1]

payload = dict(
    title='测试标题',
    download_url='http://example.com',
    click_notify_url='http://notify.com',
    search_keyword='search_keyword',
    begin_time='1970-01-01 00:00:02',
    end_time='1970-01-01 00:00:03',
    plan_count=5000,
    platform=1,
    unit_price=1234567,
    unit_award=7654321,
    idfa_query_url='idfa'
)

_ = requests.post('http://127.0.0.1:5000/api/ios_tasks/gsadmin/%s' % task_id, data=payload)

print(_)
