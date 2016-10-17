# -*- coding: utf-8 -*-
import flask
from io import BytesIO


import qrcode



server = flask.Flask(__name__)


@server.route('/')
def index():
    pil_img = qrcode.make('hello world')
    _ = BytesIO()
    pil_img.save(_)
    _.seek(0)
    blob = _.read()
    rv = flask.Response(blob)
    rv.headers['Content-Type'] = 'image/png'
    return rv


server.run(port=3000, debug=True)
