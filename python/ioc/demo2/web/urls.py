# -*- coding: utf-8 -*-
from flask import jsonify

from demo2 import inject
from demo2.domain.post import PostDomain

domain = inject('PostDomain', PostDomain)

def index():
    posts = domain.get_all_posts()
    return jsonify(posts)
