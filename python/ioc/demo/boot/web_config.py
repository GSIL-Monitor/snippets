# -*- coding: utf-8 -*-
import ioc
from ioc.decorators import Bean

from demo.web import WebApp

class MyWebConfig(ioc.Config):

    @Bean(name='webapp')
    def web_server(self):
        rv = WebApp('demo')
        return rv
