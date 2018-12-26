# -*- coding: utf-8 -*-
import sys
import timeit


class AbstractDTO(object):
    """
    明确定义属性的传值对象，此对象的继承子孙中不应该写任何业务逻辑

    * 允许对象属性或者字典访问，包括读取与写入
    * AbstractDTO.serialize 方法获取内部值的可序列化值

    **没有在 __slots__ 内定义的，在赋值时会报错**


    class BonusTaskMapper(AbstractDTO):

        __slots__ = ('task_id', 'user_id', 'genre',)


    class Genre(AbstractDTO):

        __slots__ = ('genre_id', 'name')


    t = BonusTaskMapper()
    t.task_id = 200
    t.user_id = 300
    t.genre = Genre()
    t.genre.genre_id = 6002
    t['task_id'] = 200
    t['user_id'] = 300
    t['genre']['genre_id'] = 6002
    t.genre.name = '分类名称'

    print(t.serialize(recur=False))
    print(t.serialize(recur=True))
    print(t['task_id'])
    """

    __slots__ = tuple()

    def __getitem__(self, name):
        return getattr(self, name)

    def __setitem__(self, name, val):
        return setattr(self, name, val)

    def initialize(self):
        slots = self.__class__._find_slots()
        for k in slots:
            setattr(self, k, None)

    def serialize(self, recur=True, deep=True):

        if deep:
            slots = self.__class__._find_slots()
        else:
            slots = self.__slots__

        rv = {}
        for k in slots:
            v = getattr(self, k)
            if recur and isinstance(v, AbstractDTO):
                v = v.serialize()
            rv[k] = v

        return rv

    @classmethod
    def _find_slots(cls):
        """
        递归找出所有父类的 __slots__ 属性
        """
        s = set()
        for parent in cls.__bases__:
            if issubclass(parent, AbstractDTO):
                for attr in parent._find_slots():
                    s.add(attr)

        for k in cls.__slots__:
            s.add(k)

        rv = tuple(s)
        return rv


class AbstractEvent(AbstractDTO):

    __slots__ = ('_event_name', '_uuid')


class UserFreezeEvent(AbstractEvent):

    __slots__ = ('user_id',)


ufe = UserFreezeEvent()
ufe.initialize()
print(ufe.serialize())
print(ufe.serialize(deep=False))


_ = timeit.timeit(stmt='u = UserFreezeEvent()', setup='from __main__ import UserFreezeEvent')
print(_)
_ = timeit.timeit(stmt="""
u = UserFreezeEvent(); u.initialize();""", setup='from __main__ import UserFreezeEvent')
print(_)

_ = timeit.timeit(stmt="""
u = UserFreezeEvent(); u.user_id=1; u.serialize(deep=False);""", setup='from __main__ import UserFreezeEvent')
print(_)

_ = timeit.timeit(stmt="""
u = UserFreezeEvent(); u.user_id=1; u.initialize();u.serialize(deep=True);""", setup='from __main__ import UserFreezeEvent')
print(_)


# v = UserFreezeEvent._find_slots()
# print(v)
