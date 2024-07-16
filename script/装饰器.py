# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-7-16
# Description: 装饰器的魔力,装饰器允许无侵入式地给函数添加新功能。
# http://www.51testing.com/?action-viewnews-itemid-7801717
# ***************************************************************u**


def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")

    return wrapper


@my_decorator
def say_hello():
    print("Hello!")

say_hello()
# Something is happening before the function is called.
# Hello!
# Something is happening after the function is called.
