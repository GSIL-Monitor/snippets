# -*- coding: utf-8 -*-
import flask
import redis

from seq import generate_order_no, format_order_no

webapp = flask.Flask(__name__)
webapp.debug = True
machine_id = '01'

r = redis.StrictRedis()

def save_order(order_no):
    r.set('::test:%s' % order_no, 1)

def exists_order(order_no):
    return r.get('::test:%s' % order_no) is not None

def order():
    user_id = 28931672
    o = generate_order_no(user_id, machine_id)
    conflicted = False
    while True:
        if exists_order(o):
            webapp.logger.error('conflicted order_no: %s' % format_order_no(o))
            conflicted = True
            continue
        save_order(o)
        break
    if conflicted:
        flask.abort(400)
    return format_order_no(o)


webapp.route('/')(order)
