# -*- coding: utf-8 -*-

class Component(object):
    def __init__(self, klass):
        self.klass = klass
        self.module_name = klass.__module__
        self.class_name = klass.__name__
        self.built = False
        self.result = None

    def build(self):
        if not self.built:
            self.result =  self.klass()
            self.built = True
        return self.result

    def __repr__(self):
        return '<#Component %s.%s>' % (
            self.module_name,
            self.class_name)


class Context(object):

    def __init__(self):
        self.beans = {}


    def register(self, name, klass, *args, **kwargs):
        if self.beans.get(name):
            raise Exception('bean with name "%s" already registered' % name)

        obj = klass(*args, **kwargs)
        self.beans[name] = obj


    def refresh(self):
        for c in recorded_components:
            if c.class_name in self.beans:
                continue
            bean = c.build()
            self.beans[c.class_name] = bean

        for name in self.beans:
            bean = self.beans.get(name)
            if hasattr(bean, '__post_constructed__') and \
               bean.__post_constructed__:
                continue
            if hasattr(bean, 'post_construct'):
                bean.post_construct()
            bean.__post_constructed__ = True


    def __getitem__(self, name):
        if name in self.beans:
            return self.beans.get(name)
        raise Exception('not bean with name "%s" registered.' % name)

recorded_components = []

def component(klass):
    _ = Component(klass)
    recorded_components.append(_)
    return _
