# -*- coding: utf-8 -*-
from collections import defaultdict
import time


class Base(object):
    """
    基类，包含了函数钩子的基础设施
    """

    def __init__(self):
        self.before_hooks = defaultdict(list)
        self.after_hooks = defaultdict(list)
        self.hooked = []
        self.origin_funcs = {}
        self.has_hooked = False

    def set(self, key, value, timeout=None):
        """
        举例方法
        """
        self.get_client()
        pass

    def get(self):
        """
        举例方法
        """
        pass

    def get_client(self):
        pass

    def beacon_before(self, name, func):
        """
        注册一个新的钩子
        """
        if not hasattr(self, name):
            raise RuntimeError('not func named: %s' % name)
        inter = getattr(self, name)
        if not callable(inter):
            raise RuntimeError('%s is not a function' % name)
        if not callable(func):
            raise RuntimeError('func is not a function')
        self.before_hooks[name].append(func)

    def beacon_after(self, name, func):
        """
        注册一个新的钩子
        """
        if not hasattr(self, name):
            raise RuntimeError('not func named: %s' % name)
        inter = getattr(self, name)
        if not callable(inter):
            raise RuntimeError('%s is not a function' % name)
        if not callable(func):
            raise RuntimeError('func is not a function')
        self.after_hooks[name].append(func)

    def setup_hook(self):
        """
        配置钩子
        """
        if self.has_hooked:
            return

        hooked = set(
            [x for x in self.before_hooks.keys()] +
            [x for x in self.after_hooks.keys()]
        )
        # 遍历所有已经注册的钩子
        for name in hooked:
            # 获取原来的函数
            origin = getattr(self, name)
            # 并保存起来，用于恢复
            self.origin_funcs[name] = origin
            # 新创建一个函数
            def new_func(*args, **kwargs):
                # logger.debug('new_func: %s' % name)
                # logger.debug('args: %s' % str(args))
                # logger.debug('kwargs: %s' % str(kwargs))

                options = {
                    'args': args,
                    'kwargs': kwargs,
                }

                if name in self.before_hooks:
                    # 执行前置钩子
                    self.before_hook(name, options)

                _ts = time.time()
                rv = origin(*args, **kwargs)
                _te = time.time()
                timecost = _te - _ts
                options['rv'] = rv
                options['timecost'] = timecost

                # 执行后置钩子
                if name in self.after_hooks:
                    self.after_hook(name, options)
                return rv
            # 用新函数替换原有函数
            setattr(self, name, new_func)

        self.hooked = hooked
        self.has_hooked = True

    def teardown_hook(self):
        """
        移除钩子，恢复原状
        """
        for name in self.hooked:
            origin = self.origin_funcs[name]
            setattr(self, name, origin)
        self.hooked = []
        self.has_hooked = False

    def before_hook(self, name, options):
        funcs = self.before_hooks.get(name) or []
        for func in funcs:
            func(name, options)

    def after_hook(self, name, options):
        funcs = self.after_hooks.get(name) or []
        for func in funcs:
            func(name, options)


class ImplA(Base):
    pass

    def set(self, key, value, timeout=None, raw=False):
        pass

    def get(self):
        pass
