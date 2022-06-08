# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2021-1-18
# Description: 垃圾回收机制
# ********************************************************************************************************************
#sys.getrefcount函数用来查看一个对象有几个引用

import sys

class Test():
  def __init__(self):
    pass

t = Test()
k = Test()
t._self = t
print(sys.getrefcount(t))  # 3
print(sys.getrefcount(k))  # 2

del(k)
# print(sys.getrefcount(k))  # NameError: name 'k' is not defined

del(t)
# print(sys.getrefcount(t._self))  # 2
