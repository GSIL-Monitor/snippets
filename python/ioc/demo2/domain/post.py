# -*- coding: utf-8 -*-
from demo2 import inject
from demo2.repo.post import PostRepo

class PostDomain(object):

    def __init__(self):
        pass

    def post_construct(self):
        self.repo = inject('PostRepo', PostRepo)

    def get_all_posts(self):
        return self.repo.all()
