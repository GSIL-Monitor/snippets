# -*- coding: utf-8 -*-
import flask

from test import app

@app.route('/')
def index():
    return flask.render_template('index.html')
