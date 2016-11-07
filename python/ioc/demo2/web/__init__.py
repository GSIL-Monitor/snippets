# -*- coding: utf-8 -*-
import flask
from flask.json import JSONEncoder

from demo2.model import JsonSerializable

class MyJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, JsonSerializable):
            return obj.to_json()
        return super(MyJsonEncoder, self).default(obj)


class WebApp(flask.Flask):

    def __init__(self, import_name):
        super(WebApp, self).__init__(import_name)

    def post_construct(self):
        from demo2.web import urls
        self.route('/')(urls.index)

        self.json_encoder = MyJsonEncoder
