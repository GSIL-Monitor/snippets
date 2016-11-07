# -*- coding: utf-8 -*-
import logging
logging.basicConfig(level=logging.DEBUG)

from demo2 import inject
from demo2.boot import boot
from demo2.domain.post import PostDomain

boot()
domain = inject('PostDomain', PostDomain)
logging.debug(domain)
logging.debug(domain.get_all_posts())
