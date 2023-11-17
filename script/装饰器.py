# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2023-2-13
# Description   : 装饰器
# 定义一个通用的扩展函数，可以作用域所有函数。这类不改变原函数代码的通用函数就是：装饰器。
# 装饰器本质上是一个python函数或类，装饰器的返回值也是一个函数/类对象

# https://testerhome.com/topics/23691
# *********************************************************************

# todo 函数赋值变量（函数也是对象）
def func(message):
    print("打印一条message: {}".format(message))
send_message = func
send_message("123")

# todo 函数作为参数
def func(message):
    print("打印一条message: {}".format(message))
def call_func(varfunc, message):
    varfunc(message)
call_func(func,123456)  #打印一条message: 123456


# todo 函数的嵌套
def call_func():
    def func(message):
        print("打印一条message: {}".format(message))
    return func

c = call_func()  # 函数 call_func() 的返回值是函数对象 func 本身
c(456)  # 打印一条message: 456


# todo 无参装饰函数
def my_decorator(func):
    def wrapper():
        print('wrapper of decorator')
        func()
    return wrapper

def greet():
    print('hello world')

r = my_decorator(greet)  # 这里的函数 my_decorator() 就是一个装饰器，它把真正需要执行的函数 greet() 包裹在其中，并且改变了它的行为，但是原函数 greet() 不变.
r()
# 输出
# wrapper of decorator
# hello world


# # 2）todo 语法糖 @
def my_decorator(func):
    def wrapper():
        print('wrapper of decorator')
        func()
    return wrapper

@my_decorator
def greet():
    print('hello world')

greet()
# wrapper of decorator
# hello world


# todo 带参装饰函数
def my_decorator(func):
    def wrapper(message):
        print('wrapper of decorator')
        func(message)
    return wrapper

@my_decorator
def greet(message):
    print(message)
greet('hello world')
# 输出
# wrapper of decorator
# hello world

# todo 带参装饰函数，使用是不定长参数：(*args, **kwargs)
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print('wrapper of decorator2')
        func(*args, **kwargs)
    return wrapper

@my_decorator
def greet():
    print('hello world2')
greet()
# wrapper of decorator2
# hello world2


# todo 带参装饰器
def repeat(num):
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(num):
                print(i, 'wrapper of decorator')
                func(*args, **kwargs)
        return wrapper
    return my_decorator

@repeat(3)
def greet():
    print('hello world')
greet()
# 0 wrapper of decorator
# hello world
# 1 wrapper of decorator
# hello world
# 2 wrapper of decorator
# hello world


# todo 类装饰器
class Request:
    def __init__(self, func):
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        # 每当调用一个类的示例时，函数call() 就会被执行一次。
        self.num_calls += 1
        print('num of calls is: {}'.format(self.num_calls))
        return self.func(*args, **kwargs)

@Request
def example():
    print("hello world")

example()
# num of calls is: 1
# hello world

example()
# num of calls is: 2
# hello world




# # 3）装饰器带参数
# def use_log(level):
#     def decorator(func):
#         def inner(*args, **kwargs):
#             if level == "warn":
#                 print("warning2")
#                 # logging.warning("%s is running by warning" % func.__name__)
#             elif level == 'info1':
#                 print("info")
#                 # logging.warning("%s is running by info" % func.__name__)
#             else:
#                 print('other3')
#                 # logging.warning("%s is running by other" % func.__name__)
#             return func(*args, **kwargs)
#         return inner
#     return decorator
#
# def introduce4(name, age, city):
#     print(f"我叫{name}, 我今年{age}岁了, 我来自{city}")
# info1 = use_log(introduce4('周星驰', 28, '香港'))
# info1('info1')
# info2 = use_log(introduce4('周润发', 26, '香港'))
# info2('warn')
# info3 = use_log(introduce4('成龙', 29, '香港'))
# info3('xxx')
#
#
# @use_log('info1')
# def introduce4(name, age, city):
#     print(f"我叫{name}, 我今年{age}岁了, 我来自{city}")
# info1 = use_log(introduce4('周星驰', 28, '香港'))
# info1('info1')
# info2 = use_log(introduce4('周润发', 26, '香港'))
# info2('warn')
# info3 = use_log(introduce4('成龙', 29, '香港'))
# info3('xxx')
#



