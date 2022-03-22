# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2022-3-21
# Description: 排序sort,排序索引argsort,最大值索引argmax,最小值索引argmin,向上取整ceil,向下取整floor


# *****************************************************************

import numpy as np


print("1 行排序sort".center(100, "-"))
a = np.array([[4, 3, 5], [1, 6, 1]])
print(np.sort(a))  # 等同于 np.sort(a,1)   或 np.sort(a,axis=1)
# [[3 4 5]
#  [1 1 6]]


print("2 列排序sort".center(100, "-"))
a = np.array([[4, 3, 5], [1, 6, 1]])
print(np.sort(a, 0))
# [[1 3 1]
#  [4 6 5]]


print("3 排序索引argsort()，返回索引号及值".center(100, "-"))
x = np.array([44, 23, 10, 24])
arg = np.argsort(x)
print(arg)  # [2 1 3 0]
# 算法：10索引号2，23索引号1，24索引号3，44索引号0
print(x[arg])  # [10 23 24 44]


print("4 排序索引argsort()，进行再索引排序".center(100, "-"))
print(np.argsort(arg))  # [3 1 0 2]
# 算法：对 array([2, 1, 3, 0] 进行再索引排序，0索引号3，1索引号1，2索引号0，3索引号2，结果：[3，1，0，2]


print("5 排序索引argsort()，返回数组中最大值的索引号".center(100, "-"))
print(arg[-1])  # 0   //最大值44索引号0

print("6 排序索引argsort()，返回数组中最小值的索引号".center(100, "-"))
print(arg[0])  # 2  //最小值10索引号2


print("7 最大值索引 argmax()".center(100, "-"))
a = np.array([44, 23, 3310, 124])
print(a.argmax())  # 2

print("8 最小值索引 argmin()".center(100, "-"))
a = np.array([44, 23, 3310, 124])
print(a.argmin())  # 1


print("9 向上取整 np.ceil()".center(100, "-"))
n = np.array([-1.7, -2.5, -0.2, 0.6, 1.2, 2.7, 11])
print(np.ceil(n))  # [-1. -2. -0.  1.  2.  3. 11.]

print("10 向下取整 floor()".center(100, "-"))
a = np.array([-1.7, -1.5, -0.2, 0.2, 1.5, 1.7, 2.0])
print(np.floor(a))  # [-2. -2. -1.  0.  1.  1.  2.]




