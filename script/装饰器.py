# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2023-2-13
# Description   : 装饰器
# 定义一个通用的扩展函数，可以作用域所有函数。这类不改变原函数代码的通用函数就是：装饰器。
# 装饰器本质上是一个python函数或类，装饰器的返回值也是一个函数/类对象
# *********************************************************************

# # 1）被装饰函数不带参数
#
# def wrapper_info(func):
#     def inner():
#         print("开始介绍...")
#         res = func()
#         print("介绍结束...")
#         return res
#     return inner
#
# def introduce1():
#     print("我是周润发，我来自HONG KONG")
#
# info = wrapper_info(introduce1)
# info()



# # 2）被装饰函数带参数，需要用到不定长参数：(*args, **kwargs)
#
# def wrapper_info(func):
#     """
#     用来对其他函数进行扩展，使其他函数可以在执行前做一些额外的动作
#     :param func: 要扩展的函数对象
#     :return:
#     """
#     def inner(*args, **kwargs):
#         print("开始介绍...")
#         res = func(*args, **kwargs)
#         print("介绍结束...")
#         return res
#     return inner
#
# def introduce3(name, age, city):
#     print(f"我叫{name}, 我今年{age}岁了, 我来自{city}")
#
#
# info = wrapper_info(introduce3)
# info('刘德华', 22, '香港')

# @wrapper_info
# def introduce3(name, age, city):
#     print(f"我叫{name}, 我今年{age}岁了, 我来自{city}")
# introduce3('刘德华', 28, '香港')


# 3）装饰器带参数
def use_log(level):
    def decorator(func):
        def inner(*args, **kwargs):
            if level == "warn":
                print("warning2")
                # logging.warning("%s is running by warning" % func.__name__)
            elif level == "info1":
                print("info")
                # logging.warning("%s is running by info" % func.__name__)
            else:
                print('other3')
                # logging.warning("%s is running by other" % func.__name__)
            return func(*args, **kwargs)
        return inner
    return decorator

def introduce4(name, age, city):
    print(f"我叫{name}, 我今年{age}岁了, 我来自{city}")


# @use_log('info')
# def introduce4(name, age, city):
#     print(f"我叫{name}, 我今年{age}岁了, 我来自{city}")


info1 = use_log(introduce4('周星驰', 28, '香港'))
info1('info')


info2 = use_log(introduce4('周润发', 26, '香港'))
info2('warn')

info3 = use_log(introduce4('成龙', 29, '香港'))
info3('xxx')



