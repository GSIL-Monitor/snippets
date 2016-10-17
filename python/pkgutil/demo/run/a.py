# -*- coding: utf-8 -*-
import pkgutil

def load_module(module):
    for loader, name, ispkg in pkgutil.iter_modules(module.__path__):
        module_name = '%s.%s' % (module.__name__, name)
        print('loading view: %s' % module_name)
        _module = __import__(module_name, fromlist=[''])
        print(_module.__name__)
        print(_module.notify)
        print('loaded')


from demo import test

load_module(test)
