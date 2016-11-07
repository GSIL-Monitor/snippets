# -*- coding: utf-8 -*-
from demo2 import inject
from demo2.web import WebApp
from demo2.boot import boot

boot()
webapp = inject('WebApp', WebApp)
