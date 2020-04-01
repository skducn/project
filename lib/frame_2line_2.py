# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-9-19
# Description: python的框架案例
# __xxx 双下划线表示私有类型（变量或方法），只允许这个类本身进行访问了，子类也只能引用，不能覆盖父类的方法。
# *****************************************************************

class A(object):
    def __method(self):
        print("I'm a method in A")
    def method(self):
        self.__method()

class B(A):
    def __method(self):
        print("I'm a method in B")

a = A()
a.method()  # I'm a method in A
a._A__method()  # I'm a method in A
# a.__method # 报错，AttributeError: 'A' object has no attribute '__method' ，因为它只允许在该类的内部中使用，私有方法。

b = B()
b.method()  # I'm a method in A ,
# B继承了父类A，由于A中__method()s是私有方法，它只允许在该类的内部中使用，所以 b.method()不会调用 B.__method 的方法，防止子类覆盖父类。
b._B__method()  # I'm a method in B
