# -*- coding: utf-8 -*-
import logging

from ioc import ApplicationContext
from demo.boot.config import MyConfig

logging.basicConfig(level=logging.DEBUG)

ctx = ApplicationContext.create()
ctx.add_config(MyConfig())
ctx.refresh()

domain = ctx.get_bean('post_domain')
print(domain)
print(domain.post_repo)
print(domain.get_all_posts())
