# -*- coding: utf-8 -*-

class PostModel(object):

    title = None
    content = None

    def __init__(self):
        self.title = ''
        self.content = ''

    def __repr__(self):
        return '<#PostModel %d:%s' % (self.id, self.title)
