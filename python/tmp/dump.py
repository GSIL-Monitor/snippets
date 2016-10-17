# -*- coding: utf-8 -*-
import argparse

from aves.sqlalchemy import SQLAlchemy
from aves.logging import get_logger
from aves.redis import Redis
from aves import Application

db = SQLAlchemy()
redis = Redis()
logger = get_logger()



def get_idfa_by_user(user_id):
    rs = db.session('zhuanqian').execute("""
SELECT idfa
FROM user_match
WHERE user_id = :user_id
ORDER BY id DESC LIMIT 1
""", dict(user_id=user_id))

    if rs.rowcount > 0:
        return rs.fetchone()['idfa'].upper()
    rs.close()


def get_key(apple_id, idfa):
    return 'zq:idfa:%s_%s' % (apple_id, idfa);


def cache_set(apple_id, idfa):
    _key = get_key(apple_id, idfa)
    redis.session('backend').set(_key, 1)


def get_offset():
    with open('offset') as f:
        content = f.read()
    return content.strip() or 0


def set_offset(v):
    with open('offset', 'w') as f:
        f.write(str(v))


class App(Application):

    def start(self):
        super(App, self).start()
        db.init(self.config['database'])
        redis.init(self.config['redis'])

ap = argparse.ArgumentParser()
ap.add_argument('-a', '--apple-id', help='apple id', required=True)

options = ap.parse_args()

apple_id = options.apple_id

app = App()
app.start()

cnt = 0

offset = get_offset()

while True:

    if cnt % 100 == 0:
        logger.info('processed %s records...' % cnt)

    logger.info('got offset: %s' % offset)

    rs = db.session('zhuanqian').execute("""
SELECT id, user_id, apple_id
FROM user_task_done_log
WHERE apple_id = :apple_id
AND id > :offset
LIMIT 1000
""", dict(apple_id=apple_id, offset=offset))

    if rs.rowcount <= 0:
        logger.info('all done')
        break

    for row in rs.fetchall():
        cnt += 1

        offset = row['id']
        set_offset(offset)

        user_id = row['user_id']
        idfa = get_idfa_by_user(user_id)

        if idfa is None:
            continue

        cache_set(apple_id, idfa)


logger.info('all done')
