# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2021-1-18
# Description: 垃圾回收机制
# python内都是对象，变量都是对象的引用，这有点像C语言的指针。sys模块实际上是指python这个系统，sys.getrefcount接口可以查询对象的引用计数。
# sys.getrefcount返回的计数，总是比实际多1，因为包含了调用此函数的临时计数。
# 默认在对应引用计数为0的时候，python内部的垃圾回收机制会将此对象所占用的内存收回。
# ********************************************************************************************************************

import sys
a = 100
print(sys.getrefcount(a))  # 5
b = a
print(sys.getrefcount(a))  # 6

class Test():
  def __init__(self):
    pass

t = Test()
k = Test()
t._self = t
print(sys.getrefcount(t))  # 3
print(sys.getrefcount(k))  # 2

del(k)
print(sys.getrefcount(k))  # NameError: name 'k' is not defined

del(t)
print(sys.getrefcount(t._self))  # 2
