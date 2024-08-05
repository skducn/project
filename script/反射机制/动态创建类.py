#-*-coding:utf-8 -*-
#****************************************************************
# Author     : John
# Created on : 2019-10-28
# Description: 动态创建类
# 创建一个是字符串的类名
#****************************************************************


class_dict = {'say_hello': (lambda self: print("Hello from DynamicClass"))}
DynamicClass = type('DynamicClass', (), class_dict)
instance = DynamicClass()

instance.say_hello()  # Hello from DynamicClass