# -*- coding: utf-8 -*-
import logging
import sys
import time

from aves import Application
from aves.sqlalchemy import SQLAlchemy

app = Application()
app.start()

db = SQLAlchemy()
db.init(app.config['database'])


logger = logging.getLogger()
total = 1079697

def write_db(ids):

    values = ",".join(map(lambda x: str(x), ids))


    sql = """
DELETE FROM user_task_done_log
WHERE id in (%s)
""" % values

    # logger.error(sql)
    # db.session('zhuanqian').execute(sql)

    sql = """
UPDATE user_task_done
SET log_is_executed = 0
WHETE
id in (%s)
""" % values

    # logger.error(sql)
    # db.session('zhuanqian').execute(sql)
    # db.session('zhuanqian').commit()


cnt = 0
ids = set()
for line in sys.stdin:
    _ = line.strip()
    if not _:
        continue

    row_id = int(_)

    cnt += 1
    ids.add(row_id)

    if cnt % 1000 == 0:
        write_db(ids)
        ids = set()
        logger.error('done %s/%s' % (cnt, total))

if len(ids) > 0:
    write_db(ids)
logger.error('all done')
