#-*-coding:utf-8 -*-
#****************************************************************
# Author     : John
# Created on : 2019-10-28
# Description: 反射机制
# 反射机制就是在运行时，动态的确定对象的类型，并可以通过字符串调用对象属性、方法、导入模块，是一种基于字符串的事件驱动。
# python是一门解释型语言，因此对于反射机制支持很好。在python中支持反射机制的函数有 eval()、exec()、getattr()、setattr()、delattr()、__import__，这些函数都可以执行字符串。
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

print('userTest')

def sayHello():
    print('hello userTest')
