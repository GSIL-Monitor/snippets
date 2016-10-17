# -*- coding: utf-8 -*-
import hashlib
import logging
import time
import uuid


import requests



logging.basicConfig(format='[%(asctime)s %(levelname)7s <%(process)d> '\
                    '%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)

def get_sign(itunes_id, idfa, timestamp, shared_key):

    m = hashlib.md5()
    m.update(str(itunes_id).encode('UTF-8'))
    m.update(idfa.encode('UTF-8'))
    m.update(str(timestamp).encode('UTF-8'))
    m.update(shared_key.encode('UTF-8'))

    rv = m.hexdigest()

    return rv


itunes_id = 529092160

uuids = []
uuids.append(str(uuid.uuid4()).upper())
uuids.append(str(uuid.uuid4()).upper())
timestamp = int(time.time())
shared_key = 'af6ef1f5-fd26-11e4-be83-002590a68734'

caller_id = '7a68f91c-fd26-11e4-be83-002590a68734'

logging.info(uuid)

idfa = ",".join(uuids)

sign = get_sign(itunes_id, idfa, timestamp, shared_key)

logging.info(sign)

payload = dict(
    idfa=idfa,
    timestamp=timestamp,
    appid=itunes_id,
    sign=sign,
    callerid=caller_id
)

logging.info(payload)


logging.info('send request!')
logging.info('')
logging.info('')

res = requests.post('https://open.snssdk.com/idfa/check/', payload)

if res.status_code == 200:
    logging.info(res.json())
else:
    logging.error('request error!')
