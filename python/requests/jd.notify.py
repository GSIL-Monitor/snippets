# -*- coding: utf-8 -*-
import logging
from urllib.parse import urlencode
import uuid


import requests


logging.basicConfig(level=logging.INFO)


url = 'http://adcollect.m.jd.com/adcollect.action'




def sign_payload(idfa, client_ip):

    _ = '%s%s%s%s%s' % ('350268123',
                        idfa,
                        client_ip,
                        '1',
                        'FELFOK4IHR5GDROLRJGKFU84FKGLFOUF')

    print(_)
    import hashlib
    m = hashlib.md5()
    m.update(_.encode('ascii'))
    return m.hexdigest().upper()

p = dict()
p['unionId'] = 350268123
p['idfa'] = str(uuid.uuid4()).upper()
p['clientIp'] = '192.168.1.1'
p['clientType'] = '1'
p['sign'] = sign_payload(p['idfa'], p['clientIp'])

print(p)

res = requests.get(url + '?' + urlencode(p))

print(res)
print(res.text)
