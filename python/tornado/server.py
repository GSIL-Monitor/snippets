# -*- coding: utf-8 -*-
import hashlib

from aves import Application
from aves.logging import get_logger

import tornado.web
import tornado.httpclient
import tornado.httputil
import tornado.ioloop


logger = get_logger()
app = Application()
app.start()


def get_sign(itunes_id, data, timestamp):
    shared_key = 'aa8a8a68-17f8-4120-8e7d-ea82cf97cd36'
    payload = '%s%s%s%s' % (itunes_id, data, timestamp, shared_key)

    m = hashlib.md5()
    m.update(payload.encode('UTF-8'))
    rv = m.hexdigest()
    return rv


class PostHandler(tornado.web.RequestHandler):

    def post(self):
        sign = self.get_argument('sign', None)
        logger.debug(sign)
        if sign:
            idfa = self.get_argument('idfa')
            timestamp = self.get_argument('timestamp')
            ipv4 = self.get_argument('ipv4')
            itunes_id = self.get_argument('appid')
            sign_check = get_sign(itunes_id, '%s%s' % (idfa, ipv4), timestamp)
            assert sign == sign_check


class PostErrorHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def post(self):


        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch('http://')



app = tornado.web.Application()

app.add_handlers(r'.*', [(r'/post', PostHandler, None, 'post')])
app.add_handlers(r'.*', [(r'/post_error',
                          PostErrorHandler, None, 'post_error')])


app.listen(4567)
logger.info('app listening at localhost:4567')
tornado.ioloop.IOLoop.instance().start()
