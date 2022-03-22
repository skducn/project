# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2022-3-21
# Description: 1数组 np.ones()
# numpy.ones(shape, dtype=None, order='C')
# shape : 数组的形状，例如 (2, 3) 或 2.
# dtype : 数组的数据类型，默认为float64. (i = int32, f = float32)
# order : 数组元素在内存中的排列方式，默认 'C’表示C语言排列方式，或者‘F’表示 Fortran 语言排列方式.
# *****************************************************************

import numpy as np


print("1 创建5个浮点数1的一维数组".center(100, "-"))
a = np.ones(5)
print(a)  # [1. 1. 1. 1. 1.]
print(a.dtype)  # float64

d = np.ones(5, "f")  # array([1., 1., 1., 1., 1.], dtype=float32)
print(d)  # [1. 1. 1. 1. 1.]
print(d.dtype)  # float32

print("2 创建5个整数1的一维数组".center(100, "-"))
b = np.ones(5, "i")  # 等同于 b = np.ones(5,dtype=np.int32)  等同于 np.ones((5,), dtype=np.int)
print(b)  # [1 1 1 1 1]
print(b.dtype)  # int32

c = np.ones(5, dtype=np.int64)
print(c)  # [1 1 1 1 1]
print(c.dtype)  # int64



print("3 创建3*5浮点数1的二维数组".center(100, "-"))
e = np.ones((3, 5))
print(e)
# [[1. 1. 1. 1. 1.]
#  [1. 1. 1. 1. 1.]
#  [1. 1. 1. 1. 1.]]
print(e.dtype)  # float64


print("4 创建3个4*2整数1的二维数组，即三维".center(100, "-"))
f = np.ones([3, 4, 2], "i")
print(f)
# [[[1 1]
#   [1 1]
#   [1 1]
#   [1 1]]
#
#  [[1 1]
#   [1 1]
#   [1 1]
#   [1 1]]
#
#  [[1 1]
#   [1 1]
#   [1 1]
#   [1 1]]]
print(f.dtype)  # int32



print("5 创建5个0.2的数组".center(100, "-"))
print(np.ones(5)/5)   #  [0.2 0.2 0.2 0.2 0.2]