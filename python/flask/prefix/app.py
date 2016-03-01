# -*- coding: utf-8 -*-
import os

import flask

PREFIX = os.environ.get('PREFIX', '')
static_url_path = (PREFIX and os.path.join(PREFIX, 'static')) or None

server = flask.Flask(__name__,
                     static_url_path=static_url_path)
server.debug = True

#
# monkey patch
#
route_orig = server.route
def route(rule, **options):
    rule = PREFIX + rule
    return route_orig(rule, **options)
server.route = route

url_for_orig = server.jinja_env.globals['url_for']
def url_for(endpoint, **values):
    if endpoint.startswith('/'):
        endpoint = PREFIX + endpoint

    rv = url_for_orig(endpoint, **values)

    return rv

server.jinja_env.globals['url_for'] = url_for

@server.route('/')
def index():
    return flask.render_template('spam.html')
