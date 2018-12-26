# -*- coding: utf-8 -*-
import logging
import pprint

import requests

with open('gitlab/token.txt') as f:
    token = f.read().strip()

url = 'https://git.corp.qianka.com/api/v4/projects/{}/merge_requests/{}'

projectId = 'v4%2Fhebe'
mid = 3718

url = url.format(projectId, mid)
logging.error(url)

h = {
    'PRIVATE-TOKEN': token,
}

resp = requests.get(url, headers=h)
logging.error(resp.status_code)
logging.error(pprint.pformat(resp.json()))
