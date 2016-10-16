# -*- coding: utf-8 -*-
import ioc

class PostDomain(object):

    # attr:
    #   - post_repo

    def __init__(self):
        pass

    def post_construct(self):
        self.post_repo = ioc.inject('post_repo')

    def get_all_posts(self):
        return self.post_repo.all()
