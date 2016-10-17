# -*- coding: utf-8 -*-


class Baz(object):
    name = 'hello'


class Foo(object):

    def __init__(self):
        self.baz = Baz()


    @property
    def hello(self):
        return 'hello property'

    def __getattr__(self, name):

        print('get "%s" proerty from Foo' % name)

        if name.startswith('_'):
            return getattr(self, name)
        else:
            return getattr(self.baz, name)



foo = Foo()
print(foo.baz)
print(foo.name)
print(foo.hello)
print(foo.__dict__)
