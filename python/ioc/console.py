# -*- coding: utf-8 -*-
from ioc import component

@component
class Console(object):
    def writeLine(self, *args):
        print(*args)
