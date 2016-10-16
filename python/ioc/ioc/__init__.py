# -*- coding: utf-8 -*-
import logging

logging.basicConfig(level=logging.DEBUG)

context = None

class ApplicationContext(object):

    def __init__(self):
        self.beans = {}
        self.configs = []
        self.need_post_construct = []

    def add_config(self, config):
        logging.debug('add_config: %s' % config)
        self.configs.append(config)

    def refresh(self):
        for c in self.configs:
            # print(c)
            if c.evaludated:
                continue
            logging.debug('eval config: %s' % c)
            self._eval_config(c)
        self._eval_post_construct()

    def _eval_post_construct(self):
        for b in self.need_post_construct:
            logging.debug('eval post_construct() for bean: %s' % b)
            b.post_construct()

    def _eval_config(self, config):
        for i in dir(config):
            if i.startswith('__'):
                continue
            bo = getattr(config, i)
            if not isinstance(bo, BeanObject):
                continue
            logging.debug('eval bean: %s' % bo.name)
            if bo.name in self.beans:
                raise RuntimeError(
                    'already created Bean named "%s"' % bo.name)
            bo.ctx = config
            bean = bo()
            if hasattr(bean, 'post_construct'):
                self.need_post_construct.append(bean)
            self.beans[bo.name] = bean
        config.evaludated = True

    def get_bean(self, name, clazz=None):
        rv = self.beans.get(name)
        if rv is None:
            raise RuntimeError('cannot get bean with name: "%s"' % name)
        if clazz:
            if not isinstance(rv, clazz):
                raise RuntimeError('bean "%s" is not type: "%s"' % name, clazz)
        return rv

    @staticmethod
    def create():
        global context
        rv = ApplicationContext()
        context = rv
        return rv

class Config(object):

    def __init__(self):
        self.beans = {}
        self.evaludated = False


class BeanObject(object):

    name = None
    func = None
    ctx = None

    def __init__(self, name, func):
        # print('===> BeanObject')
        # print(name)
        # print(func)
        self.name = name
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(self.ctx, *args, **kwargs)

    def __repr__(self):
        return '<#BeanObject %s>' % self.name


def inject(name, clazz=None):
    global context
    return context.get_bean(name, clazz)
