# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-9-19
# Description: python的框架案例
# 1、类中私有变量或私有方法不能被实例引用
# 2、实例引用时通过_类__私有变量直接init中私有变量，类似地，实例引用可通过_类_私有方法直接访问
# 3、私有方法可以重写init的self.x值
# *****************************************************************

class A(object):
    def __init__(self, x):
        self.__abc = 5  # 私有变量
        self.x = x
    def __func(self):  # 私有方法
        self.x = 33
        print("123456")

a = A(2)
print(a.x)  # 2， init中构造了self.x
print(a._A__abc)  # 5， 通过_类名__变量，直接访问
# print(a.__abc)  # 报错，私有变量不能被实例引用，"AttributeError: 'A' object has no attribute '__abc'"
# print(a.__func)  # 报错，私有方法不能被实例引用，AttributeError: 'A' object has no attribute '__func'

a._A__func()  # 123456， 通过_类名__方法，重新初始化init中self.x
print(a.x)  # 33