# -*- coding: utf-8 -*-
from qianka.common.job.redis import QkRedisConsumer


class MyConsumer(QkRedisConsumer):

    def handle_message(self, m):
        print(m)


con = MyConsumer()
con.configure(['default'], 'redis://')
con.main()
