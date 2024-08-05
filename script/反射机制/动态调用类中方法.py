#-*-coding:utf-8 -*-
#****************************************************************
# Author     : John
# Created on : 2024-8-5
# Description: 动态调用类中方法
# 方法已存在，方法名是字符串，可以通过字符串来动态调用方法
#****************************************************************


class MyClass:
    def greet(self, message):
        print(message)

my_instance = MyClass()

getattr(my_instance, "greet")("Hello, World!")  # Hello, World!

