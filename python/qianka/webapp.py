# -*- coding: utf-8 -*-
import time

from flask import Flask

from qianka_queue.amqp import QkAmqp


webapp = Flask(__name__)
webapp.config.from_pyfile('config.py')

amqp = QkAmqp()
amqp.configure(webapp.config)
amqp.setup_flask_app(webapp)


@webapp.route('/mq')
def mq():
    o = {
        'time': time.time(),
    }
    _ = amqp.send(
        o, exchange_name='amq.topic', routing_key='',
        marshal='msgpack', compress='zlib',
    )
    return str(_)


webapp.run(port=3000, threaded=True)
