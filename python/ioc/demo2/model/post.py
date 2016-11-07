# -*- coding: utf-8 -*-

from demo2.model import JsonSerializable

class Post(JsonSerializable):

    def __init__(self):
        self.id = 0
        self.title = None
        self.content = None


    def __repr__(self):
        return '<#Post #%s:%s>' % (self.id, self.title)


    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
        }
