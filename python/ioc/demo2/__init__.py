# -*- coding: utf-8 -*-

def inject(name, clazz):
    from demo2.boot import beans
    bean = beans.get(name)
    if bean is None:
        raise RuntimeError('cannot get bean with name: "%s"' % name)

    if not isinstance(bean, clazz):
        raise RuntimeError('bean named "%s" is not type: %s' % name, clazz)

    return bean
