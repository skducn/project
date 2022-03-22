# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2022-3-21
# Description: 0数组 np.zeros()
# numpy.ones(shape, dtype=None, order='C')
# shape : 数组的形状，例如 (2, 3) 或 2.
# dtype : 数组的数据类型，默认为float64. (i = int32, f = float32)
# order : 数组元素在内存中的排列方式，默认 'C’表示C语言排列方式，或者‘F’表示 Fortran 语言排列方式.
# *****************************************************************

import numpy as np


print("1 创建5个浮点数0的一维数组".center(100, "-"))
print(np.zeros(5))  # [0. 0. 0. 0. 0.] //默认dtype('float64')


print("2 创建5个整数0的一维数组".center(100, "-"))
print(np.zeros((5,), dtype=np.int))  # [0 0 0 0 0]


print("3 创建2*2浮点数0的二维数组".center(100, "-"))
print(np.zeros((2, 2)))
# [[0. 0.]
#  [0. 0.]]


print("4 创建5个11的数组".center(100, "-"))
print(np.zeros(5, "i")+11)   # [11 11 11 11 11]