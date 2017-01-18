# -*- coding: utf-8 -*-
from ioc import component

from common import ctx

@component
class Greeter(object):

    def greet(self, name=None):
        ctx['Console'].writeLine('Hello, %s !' % (name or 'World'))
