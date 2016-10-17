# -*- coding: utf-8 -*-

import hashlib


def get_sign(appid, data, ts, shared_key):

    payload = '%s%s%s%s' % (appid, data, ts, shared_key)

    m = hashlib.md5(payload.encode('UTF8'))

    return m.hexdigest()


appid = 98765432
idfa = '81F6B082-08F3-4593-A64F-F4835B845866,DDDA4B66-5830-426E-B6CC-9DBD7549C084'.upper()
ts = 1434426170
key = 'a11ed357-238a-4560-840d-eb0507abb11a'.lower()

sign = get_sign(appid, idfa, ts, key)

print(sign)
