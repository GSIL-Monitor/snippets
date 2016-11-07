# -*- coding: utf-8 -*-
import ioc

from demo.repo.post import PostRepo

class PostDomain(object):

    # attr:
    #   - post_repo

    def __init__(self):
        pass

    def post_construct(self):
        self.post_repo = ioc.inject('post_repo', PostRepo)

    def get_all_posts(self):
        return self.post_repo.all()
