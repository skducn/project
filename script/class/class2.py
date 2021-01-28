# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2020-3-23
# Description: 类方法，静态方法
# 1，类方法，使用@classmethod,可以访问类变量
# 2，静态方法，使用@staticmethod，不能访问类变量
# *******************************************************************************************************************************

'''类方法，使用@classmethod'''
class A:
    num = 1
    @classmethod
    def func(cls):  # 类方法需要传递cls参数，类似于self
        print('num', cls.num)  # 类方法可以访问类变量，如num

A.func()  # num 1
a = A()
a.func()  # num 1
print(A.func)  # <bound method A.func of <class '__main__.A'>>
print(a.func)  # <bound method A.func of <class '__main__.A'>>
print("~~~~~~~~~~~~")

'''静态方法，使用@staticmethod'''
class B:
    num = 2  # 静态方法不能访问类变量
    @staticmethod
    def func():
        a = 33
        print(a)

B.func() # 33
b = B()
c = B()
b.func()  # 33
c.func()   # 33
print("~~~~~~~~~~~~")

'''由于使用了staticmathod，以下三个地址共享同一块数据, '''
print (B.func) # <function B.func at 0x0000020478715040>
print (b.func) # <function B.func at 0x0000020478715040>
print (c.func) # <function B.func at 0x0000020478715040>


