# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2022-3-21
# Description: 行间合并 np.r_[]， 列间合并 np.c_[]
# *****************************************************************

import numpy as np


print("1 行间合并一维数组".center(100, "-"))
d = np.array([7, 8, 9])
e = np.array([1, 2, 3])
print(np.r_[d, e])  # [7 8 9 1 2 3]


print("2 行间合并二维数组".center(100, "-"))
a = np.array([[1, 2, 3], [7, 8, 9]])
b = np.array([[4, 5, 6], [1, 2, 3]])
print(np.r_[a, b])
# [[1 2 3]
#  [7 8 9]
#  [4 5 6]
#  [1 2 3]]

print("3 列间合并一维数组".center(100, "-"))
d = np.array([7, 8, 9])
e = np.array([1, 2, 3])
print(np.c_[d, e])
# [[7 1]
#  [8 2]
#  [9 3]]

print("4 列间合并二维数组".center(100, "-"))
a = np.array([[1, 2, 3], [7, 8, 9]])
b = np.array([[4, 5, 6], [1, 2, 3]])
print(np.c_[a, b])
# [[1 2 3 4 5 6]
#  [7 8 9 1 2 3]]