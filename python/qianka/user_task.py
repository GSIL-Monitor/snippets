# -*- coding: utf-8 -*-
import logging
import sys

import aves

app = aves.Aves()
app.start()

db = aves.SQLAlchemy()
db.init(app.config['database'])

logger = logging.getLogger()

class IDFA(object):

    idfa = None

    def __init__(self, idfa):
        self.idfa = idfa

    @property
    def user_id(self):
        sql = 'SELECT user_id FROM user_match WHERE idfa = :idfa LIMIT 1'
        rs = db.session('zhuanqian').execute(sql, dict(idfa=self.idfa))
        if rs.rowcount:
            r = rs.fetchone()
            return r['user_id']

    @property
    def sharding_index(self):
        sql = 'SELECT `index` FROM user_sharding_index WHERE uid = :user_id'
        rs = db.session('zhuanqian').execute(sql, dict(user_id=self.user_id))
        if rs.rowcount:
            r = rs.fetchone()
            return r['index']

    @property
    def sharding_bind(self):
        index = self.sharding_index
        if index:
            return 'zhuanqian_%03d' % index
        return 'zhuanqian'

    def has_done_task(self, task_id):
        sql = """SELECT * FROM user_subtasks WHERE
user_id = :user_id AND subtasks_id = :task_id"""

        rs = db.session(self.sharding_bind).execute(
            sql,
            dict(user_id=self.user_id,
                 task_id=task_id))

        if rs.rowcount:
            rs.close()
            return True
        return False


idfas = []
for line in sys.stdin:
    idfa = line.strip()
    if idfa:
        idfas.append(IDFA(idfa))

for i in idfas:
    logger.info('user #%s, idfa: %s, has done task 145258: %s' %
                (i.user_id, i.idfa, i.has_done_task(145258)))
