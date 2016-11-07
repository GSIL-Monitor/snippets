# -*- coding: utf-8 -*-
import ioc

from demo.domain.post import PostDomain

post_domain = ioc.inject('post_domain', PostDomain)

def index():
    posts = post_domain.get_all_posts()
    return str(posts)
