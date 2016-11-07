# -*- coding: utf-8 -*-

class JsonSerializable(object):

    def to_json(self):
        raise NotImplementedError()
