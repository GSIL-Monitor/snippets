# -*- coding: utf-8 -*-
import logging

from ioc import ApplicationContext
from demo.boot.config import MyConfig
from demo.boot.web_config import MyWebConfig

logging.basicConfig(level=logging.DEBUG)

ctx = ApplicationContext.create()
ctx.add_config(MyConfig())
ctx.add_config(MyWebConfig())
ctx.refresh()

app = ctx.get_bean('webapp')
print(app)
