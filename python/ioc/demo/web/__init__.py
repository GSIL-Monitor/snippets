# -*- coding: utf-8 -*-
import logging

import flask
import ioc

class WebApp(flask.Flask):

    def __init__(self, app_name):
        super(WebApp, self).__init__(app_name)

    def post_construct(self):
        from demo.web import urls

        self.route('/')(urls.index)
