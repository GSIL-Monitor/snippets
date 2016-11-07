# -*- coding: utf-8 -*-
from demo2 import inject
from demo2.dao.post import PostDao

class PostRepo(object):

    def __init__(self):
        pass

    def post_construct(self):
        self.dao = inject('PostDao', PostDao)

    def all(self):
        return self.dao.all()
