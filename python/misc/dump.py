# -*- coding: utf-8 -*-
import hashlib
import time

_from = '1013684a'
token = 'FpOd3tLRjVaa1FBpZURPcklBQXZFNnpwM9ZrYXBoWk21'
timestamp = int(time.time())


def get_sign(_from, timestamp, token):

    with open('idfa.txt') as f:
        _ = f.read()

    payload = '%s%s%s%s' % (_from,
                            timestamp,
                            token,
                            _)

    payload = payload.encode('UTF-8')
    m = hashlib.md5()
    m.update(payload)
    return m.hexdigest()



secret = get_sign(_from, timestamp, token)

o = 'curl -L -v -H "Content-Type: text/plan" -X POST -T ./idfa.txt "http://r6.mo.baidu.com/v5/idfa/status?from=%(_from)s&secret=%(secret)s&time=%(timestamp)s"' % dict(_from=_from, timestamp=timestamp, secret=secret)

print(o)
