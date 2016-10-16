# -*- coding: utf-8 -*-
import ioc

def index():
    post_domain = ioc.inject('post_domain')
    posts = post_domain.get_all_posts()
    return str(posts)
