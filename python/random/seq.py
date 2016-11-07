# -*- coding: utf-8 -*-
import datetime
import logging
import time
import uuid

logging.basicConfig(level=logging.INFO)


def generate_order_no(user_id, machine_id):
    h = uuid.uuid5(uuid.uuid4(), str(user_id))

    u = str(user_id).zfill(4)[-4:]
    r = str(hash(h)).zfill(19)[-10:]
    logging.debug(r)
    now = datetime.datetime.now()
    y = str(now.year)[-2:]

    r1 = r[:5]
    r2 = r[5:]
    s = '%s%s%s%s%s' % (y, machine_id, r1, r2, u)
    logging.debug(s)
    sum = 0
    for c in s:
        sum += int(c)
    checksum = sum % 10
    logging.debug(checksum)
    rv = '%s%s-%s-%s%s-%s' % (y, machine_id, r1, checksum, r2, u)
    return rv.replace('-', '')

def format_order_no(s):
    return '%s-%s-%s-%s' % (s[:4], s[4:9], s[9:15], s[15:])

if __name__ == '__main__':
    _ = generate_order_no(2347198, '01')
    logging.debug(_)
    logging.debug(format_order_no(_))
