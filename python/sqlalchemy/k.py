# -*- coding: utf-8 -*-
import logging
import pprint
import re
import time

# from qianka.sqlalchemy import QKSQLAlchemy
from msgpack import unpackb

from oscar import app, db
from oscar.services import blob_content

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
PTRN = re.compile(r'^[\u4e00-\u9fa5]+$')

SQLALCHEMY_BINDS = {}
SQLALCHEMY_BINDS['default'] = {}
SQLALCHEMY_BINDS['default']['host'] = (
    'rm-bp18305s0fcfd23b7.mysql.rds.aliyuncs.com')
SQLALCHEMY_BINDS['default']['port'] = 3306
SQLALCHEMY_BINDS['default']['user'] = 'oscar'
SQLALCHEMY_BINDS['default']['pwd'] = 'thBFwA8SvU'
SQLALCHEMY_BINDS['default']['connector'] = 'mysqldb'
SQLALCHEMY_BINDS['default']['adapter'] = 'mysql'
SQLALCHEMY_BINDS['default']['charset'] = 'utf8'
SQLALCHEMY_BINDS['default']['db'] = 'oscar'

config = {
    'SQLALCHEMY_BINDS': SQLALCHEMY_BINDS,
    'SQLALCHEMY_ECHO': False,
}

# db = QKSQLAlchemy()
# db.configure(config)


class Fetcher(object):

    def fetch_once(self, offset, limit):
        sql = """
        SELECT a.id id, keyword FROM appstore_keyword a LEFT JOIN
        keyword b ON a.id=b.keyword_id WHERE (b.priority=0 OR b.id
        IS NULL) AND a.is_skip=0 AND a.id>:offset ORDER BY a.id
        LIMIT :limit
        """
        p = {
            'offset': offset,
            'limit': limit,
        }
        rv = db.session.execute(sql, p).fetchall()
        return rv

    def do_fetch(self):

        offset = 0
        limit = 100
        total = 0
        filtered = 0
        kws = {}
        while True:
            rows = self.fetch_once(offset, limit)
            if not rows:
                break
            offset = rows[-1]['id']

            total += len(rows)
            for row in rows:
                kw = row['keyword']
                # LOGGER.debug(kw)
                if not PTRN.search(kw):
                    continue
                if len(kw) > 7:
                    continue
                filtered += 1
                kws[kw] = 1

            LOGGER.info('offset: %d', offset)

        LOGGER.info('total rows: %d', total)
        LOGGER.info('filtered rows: %d', filtered)
        LOGGER.info('unique keywords: %d', len(kws))

    def search_result(self, kws):
        kw_ids = [x['id'] for x in kws]
        sql = """SELECT a.id, keyword_id, content_hash FROM search_result a
        INNER JOIN (
          SELECT MAX(id) id FROM search_result WHERE keyword_id in :kw_ids
          GROUP BY keyword_id
        ) b ON a.id = b.id"""
        p = {
            'kw_ids': kw_ids,
        }
        rows = db.session.execute(sql, p).fetchall()
        chash_map = {x['keyword_id']: x['content_hash'] for x in rows}
        rv = []
        for kw in kws:
            kw_id = kw['id']
            if kw_id not in chash_map:
                continue
            chash = chash_map[kw_id]
            _ = {
                'id': kw_id,
                'keyword': kw['keyword'],
                'content_hash': chash,
            }
            rv.append(_)
        return rv

    def fetch_apple_ids(self, hashes):
        rv = {}
        contents = blob_content.get_rows(hashes)
        for chash, b in contents.items():
            apple_ids = unpackb(b)
            if not apple_ids:
                LOGGER.debug('chash %s not apple_ids', chash)
                continue
            if len(apple_ids) < 50:
                LOGGER.debug('chash %s apple_ids < 50', chash)
                continue
            # 取排名45开始，最多10个
            rv[chash] = apple_ids[44:54]
        return rv

    def fetch_app(self, apple_id_map):
        # apple_id => kw_id
        apple_ids = set()
        reverse_map = {}
        for kw_id, _apple_ids in apple_id_map.items():
            for apple_id in _apple_ids:
                reverse_map[apple_id] = kw_id
            apple_ids.update(_apple_ids)

        sql = """SELECT * FROM application WHERE app_id IN :apple_ids"""
        p = {
            'apple_ids': apple_ids,
        }
        rows = db.session.execute(sql, p).fetchall()
        return [dict(x) for x in rows]


# bench initial query
# ts = time.time()
# Fetcher().do_fetch()
# te = time.time()
# tc = te - ts
# LOGGER.info('total time cost: %d ms', int(tc * 1000))


app.ready(db=True, web=False)


def main():

    ts = time.time()
    f = Fetcher()
    keywords = f.fetch_once(100, 10)
    keywords = f.search_result(keywords)
    LOGGER.debug(pprint.pformat(keywords))
    te = time.time()
    tc = te - ts
    LOGGER.info('time cost: %d ms', int(tc * 1000))

    hashes = [x['content_hash'] for x in keywords]
    apple_id_map = f.fetch_apple_ids(hashes)
    LOGGER.debug(pprint.pformat(apple_id_map))

    apps = f.fetch_app(apple_id_map)
    LOGGER.debug(pprint.pformat(apps))


with app.app_context():
    main()
