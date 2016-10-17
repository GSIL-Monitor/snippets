# -*- coding: utf-8 -*-
import threading
import time
import sys

from aves import Application
from aves.sqlalchemy import SQLAlchemy

app = Application()
app.start()


sys.exit(0)


def sharding_by_user(bind, user_id):
    if bind == 'zhuanqian':
        if user_id <= 1000:
            return 'zhuanqian_shard1'
        if user_id > 1000:
            return 'zhuanqian_shard2'

    raise RuntimeError('cannot shard')


db = SQLAlchemy()
db.init(app.config['database'])

def connect():
    user_id = 1000
    bind = sharding_by_user('zhuanqian', user_id)
    sess = db.session(bind)
    print(sess)
    print(sess.get_bind())
    sess.execute('select 1')
    sess.remove()
    time.sleep(3)
    db.reset()
    time.sleep(1)
    db.reset_all()
    user_id = 2000
    bind = sharding_by_user('zhuanqian', user_id)
    sess = db.session(bind)
    print(sess)
    print(sess.get_bind())
    sess.execute('select 1')
    sess.remove()
    time.sleep(3)
    db.reset()
    time.sleep(1)
    db.reset_all()
    print('========end=======')

while True:
    connect()
