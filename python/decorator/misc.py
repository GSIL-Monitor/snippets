# -*- coding: utf-8 -*-
from functools import wraps

#
# 重点！
# Python中的装饰器，不是Java的注解！完全不同的概念
# Python的装饰器，是真的在使用装饰器的地方**执行了装饰器的代码**
# 一句话结论：不懂就不要去用
#


def decorator(fn):

    # 这里的代码实际上在使用装饰器时就已经运行了
    print('use decorator')

    @wraps(fn)  # <== 这一句有什么用？ XDDDDDDD
    def new_wrapper(*args, **kwargs):
        print("wrapper !!")
        rv = fn(*args, **kwargs)
        return rv
    return new_wrapper


print('>> 1 start')


def hello():
    print('hello1')


print('>>> 1.1')


# 没有装饰器
# 'hello1'
hello()


print('>> 1 end')

print('>> 2 start')


# 使用了装饰器
# **这里其实已经会运行装饰器方法里的代码**
@decorator
def hello2():
    print('hello2')


print('>>> 2.1')


# 调用 **被装饰后的hello1 方法**
# 'wrapper !!'
# 'hello2'
hello2()


print('>> 2 end')


print('>> 3 start')

# 这里我们比较一下装饰器使用方法的区别
# @decorator
# def hello3():
#     print('hello3')
#
# 相当于写了以下代码
# def hello3():
#     print('hello3')
# hello3 = decorator(hello3)
#
# **而不是**
# def hello3():
#     print('hello3')
# decorator(hello3)
# 思考：这里没有任何赋值，什么情景适用？


# 先定义一个函数
def hello3():
    print('hello3')


id1 = id(hello3)

# 套用装饰器后
hello3 = decorator(hello3)

id2 = id(hello3)

print('>>> 3.1 id1 => {}'.format(id1))
print('>>> 3.1 id2 => {}'.format(id2))

# 可以看到两者实际上是不一样的对象


print('>>> 3.2')

#
# 实际上，用@写法，也可以拿到原始的函数指针，只是比较奇怪
#
def func_pointer_inspector(fn):
    # 使用 @ 套用装饰器，只有装饰器内部才能获取原始的 "被装饰函数"
    print('>>> 3.2 id1: {}'.format(id(fn)))

    # @wraps(fn)   # 这里没有调用，会与上面有什么区别？
    def new_wrapper(*args, **kwargs):
        rv = fn(*args, **kwargs)
        return rv
    return new_wrapper


@func_pointer_inspector
def hello3_2():
    print('hello3_2')


print('>>> 3.2 id2: {}'.format(id(hello3_2)))


print('>> 3 end')

print('>> 4 start')


#
# 思考
#
# 以下代码会出现什么效果？
@decorator
def func1():
    print('func1')


def func2():
    """
    这里想直接使用 func1 里的逻辑

    会只打印 'func1' 吗？
    """
    return func1()


# 如果运行 func2() 会输出什么？
func2()

print('>> 4 end')
