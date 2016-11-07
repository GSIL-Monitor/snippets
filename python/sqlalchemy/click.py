# -*- coding: utf-8 -*-
import base64
import json
import logging

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

source_sql = """
select * from task_notify_queue where task_id = 151059 and status = 0
"""

task_sql = """
select appid, ad_id, subtitle from subtasks where id = :id
"""

MESSAGE_BROKER_URL = 'http://10.45.32.112/message/v1/send'

class MQService(object):

    def __init__(self, url):
        self.url = url

    def send(self, payload, routing_key, exchange_name='hera.topic',
             bind='default', flag='json'):

        if flag == 'text':
            body = payload
        if flag == 'json':
            body = json.dumps(payload).encode('ascii')
            body = base64.b64encode(body)
        else:
            raise RuntimeError('unknown flag: %s' % flag)

        data = {
            'connection': bind,
            'exchange': exchange_name,
            'routingKey': routing_key,
            'body': body,
            'flag': flag,
        }

        logger.debug(data)
        return True
        resp = requests.post(
            self.url,
            data=data
        )
        logger.debug(resp.body)
        return resp.status_code == 200


class T(object):
    def __init__(self):
        self.engine = create_engine(
            'mysql+pymysql://staff:1112da0c6e@'
            'itunesregister1.mysql.rds.aliyuncs.com/zhuanqian'
            '?charset=utf8')
        self.session = sessionmaker(
            self.engine, autocommit=True, autoflush=True)()

        self.mq = MQService('')
        self.tasks = {}

    def get_task(self, id):
        if id in self.tasks:
            rv = self.tasks[id]
        else:
            rv = self.session.execute(task_sql, dict(id=id)).fetchone()
            if rv:
                self.tasks[id] = rv
        return rv

    def requeue(self):
        rs = self.session.execute(source_sql)

        total = rs.rowcount
        cnt = 0

        for row in rs.fetchall():
            cnt += 1
            logger.info('sent %s/%s' % (cnt, total))
            task = self.get_task(row['task_id'])
            if task is None:
                continue

            notify_event = {}
            notify_event['user_id'] = row['user_id']
            notify_event['task_id'] = row['task_id']
            notify_event['idfa'] = row['idfa']
            notify_event['ipv4'] = row['ipv4']
            notify_event['event_id'] = row['id']

            apple_id = int(task['appid'])
            routing_key = 'subtasks.startnotify.%s' % apple_id
            notify_event['advertiser_id'] = int(task['ad_id'])
            notify_event['title'] = task['subtitle']
            notify_event['apple_id'] = apple_id
            logger.debug(notify_event)

            self.mq.send(notify_event, routing_key=routing_key)

t = T()
t.requeue()
