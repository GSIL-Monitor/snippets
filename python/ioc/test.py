# -*- coding: utf-8 -*-
from ioc import ApplicationContext, Config
from ioc.decorators import Bean

class StringContainer(object):

    s = None

    def __init__(self, s):
        self.s = s

    def getS(self):
        return s

class T(object): pass

class MyConfig(Config):

    @Bean
    def myString(self):
        return 'myString'

    @Bean(name='t')
    def myT(self):
        return T()

    @Bean
    def a(self):
        return StringContainer(self.myString())

class MyWebConfig(Config):

    @Bean
    def myAnotherString(self):
        return 'myAnotherString'

ctx = ApplicationContext.create()
ctx.add_config(MyConfig())
ctx.add_config(MyWebConfig())
ctx.refresh()
s = ctx.get_bean('myString')
print(s)
print(id(s))

t = ctx.get_bean('t', T)
print(t)

a = ctx.get_bean('a')
print(a)
print(a.getS())
print(id(a.getS()))

ms = ctx.get_bean('myAnotherString')
print(ms)
