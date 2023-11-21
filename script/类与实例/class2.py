# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2020-3-23
# Description: 类方法，静态方法
# 1，类方法，使用@classmethod,可以访问类变量
# 2，静态方法，使用@staticmethod，不能访问类变量
# *******************************************************************************************************************************


# todo: 类方法 @classmethod
# 类方法是将类本身作为对象进行操作的方法，可以被继承
print("类方法 @classmethod".center(100, "-"))
class ClassWay:
    num = 1
    @classmethod
    def func(cls):  # 类方法第一个参数为cls，自动绑定到类。
        print('num=', cls.num)  # 类方法可以访问类变量，如num

ClassWay.func()  # num= 1
a = ClassWay()
a.func()  # num= 1
print(ClassWay.func)  # <bound method ClassWay.func of <类与实例 '__main__.ClassWay'>>
print(a.func)  # <bound method ClassWay.func of <类与实例 '__main__.ClassWay'>>
print(type(a.func))  # <类与实例 'method'>
print(type(a))  # <类与实例 '__main__.ClassWay'>
print(type(ClassWay))  # <类与实例 '__main__.ClassWay'>


# todo: 静态方法 @staticmethod
print("静态方法 @staticmethod".center(100, "-"))
class StaticWay:
    num = 2  # 静态方法不能访问类变量
    @staticmethod
    def func():
        a = 33
        print(a)

StaticWay.func() # 33
b = StaticWay()
c = StaticWay()
b.func()  # 33
c.func()   # 33


# 由于使用了staticmathod，所以静态方法的地址共享同一块数据
print(StaticWay.func) # <function B.func at 0x0000020478715040>
print(b.func) # <function B.func at 0x0000020478715040>
print(c.func) # <function B.func at 0x0000020478715040>





class ClassTest(object):
    __num = 0

    @classmethod
    def addNum(cls):
        cls.__num += 1

    @classmethod
    def getNum(cls):
        return cls.__num

    # 这里我用到魔术方法__new__，主要是为了在创建实例的时候调用累加方法。
    def __new__(self):
        ClassTest.addNum()
        print("执行1")
        # return super(ClassTest, self).__new__(self)  # <__main__.Student object at 0x0000012456D16880>
b

class Student(ClassTest):
    def __init__(self):
        self.name = ''
        print("执行2")

a = Student()
b = Student()
c = Student()
print(ClassTest.getNum())