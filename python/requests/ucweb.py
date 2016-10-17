# -*- coding: utf-8 -*-
import hashlib
import time
import uuid


import requests


def sign_payload_ucweb(payload, timestamp):

    idfa = payload.get('idfa')

    # timestamp = int(time.time())
    ch = 'zhangjd@qiankaios'

    sign = get_sign_ucweb(ch, timestamp, idfa)

    payload['ch'] = ch
    payload['time'] = timestamp
    payload['sign'] = sign
    payload['appid'] = 586871187

    return payload


def get_sign_ucweb(ch, timestamp, idfa):

    key = 'aa927ce32a'

    _ = ('appid=586871187&ch=%(ch)s&idfa=%(idfa)s'
         '&time=%(time)s%(key)s') % dict(ch=ch,
                                         idfa=idfa,
                                         time=timestamp,
                                         key=key)
    print(_)
    m = hashlib.md5()
    m.update(_.encode('UTF-8'))
    rv = m.hexdigest()
    return rv

payload = {}
payload['idfa'] = str(uuid.uuid4()).upper()
payload['idfa']= '1B17ECEF-559C-4ECB-B498-8EF5CA04178C'

{'appid': 586871187, 'idfa': '1B17ECEF-559C-4ECB-B498-8EF5CA04178C', 'time': 1467103834, 'ch': 'zhangjd@qiankaios', 'sign': '36f5489a17c2ddc9f730c897a8ae28c9'}
print(payload['idfa'])

timestamp = 1467103834
payload = sign_payload_ucweb(payload, timestamp)
print(payload['sign'])

print(payload)
res = requests.post('http://union.uc.cn/public/ios_promotion.php',
                    params=payload)

print(res.status_code)
print(res.json())
