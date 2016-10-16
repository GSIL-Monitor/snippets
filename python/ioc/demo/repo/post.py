# -*- coding: utf-8 -*-
import ioc

class PostRepo(object):

    # attrs:
    #   - post_dao

    def __init__(self):
        pass

    def post_construct(self):
        self.post_dao = ioc.inject('post_dao')

    def all(self):
        return self.post_dao.all()
