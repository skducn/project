# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2022-3-21
# Description: 创建矩阵 np.mat()
# mat 成员函数：https://blog.csdn.net/weixin_39258979/article/details/109358408
# 矩阵是二维的，可通过字符串或列表创建
# mat = asmatrix 源码中mat作为指向asmatrix函数的一个变量
# np.mat 与 np.array可互相转换，但需要注意维度的变化，因为array可以是任意维度数组,mat 只能创建二维数组
# *****************************************************************

import numpy as np


print("1 用字符串创建矩阵".center(100, "-"))
a = np.mat(data="1,2;3,4")  # matrix([[1, 2],[3, 4]])
print(a)
# [[1 2]
#  [3 4]]


print("2 修改矩阵元素".center(100, "-"))
b = np.asmatrix([[5, 6], [7, 8]])
print(b)
# [[5 6]
#  [7 8]]
b[0, 1] = 10000
print(b)
# [[    5 10000]
#  [    7     8]]


print("3 用字符串或列表创建矩阵".center(100, "-"))
print(np.mat("1,2;3,4"))
# [[1 2]
#  [3 4]]
print(np.mat([1, 2, 3, 4]))
# [[1 2 3 4]]


print("4 np.mat 与 np.array 互相转换，需要注意维度的变化".center(100, "-"))
arr = np.array([1,2,3,4,5])
print(arr.ndim)  # 1
y = np.mat(arr)  # 将array转换成mat
print(y)  # [[1 2 3 4 5]]
print(y.ndim)  # 2
z = np.array(y)  # 将mat再转回array
print(z)  # [[1 2 3 4 5]]
print(z.ndim)  # 2


print("5 矩阵求逆 x.I".center(100, "-"))
x = np.mat([[1,2],[3,4]])
print(x)
# [[1 2]
#  [3 4]]
print(x.I)
# [[-2.   1. ]
#  [ 1.5 -0.5]]


print("6 矩阵转置 x.T".center(100, "-"))
x = np.mat([[1,2],[3,4]])
print(x)
# [[1 2]
#  [3 4]]
print(x.T)
# [[1 3]
#  [2 4]]


print("7 矩阵乘积".center(100, "-"))
A = np.mat([[1, 2], [3, 4]])
B = np.mat([[5, 6], [7, 8]])
print(A.dot(B))  # 等同于 np.matmul(A,B) = A*B
# [[19 22]
#  [43 50]]
# 算法：[1*5+2*7 1*6+2*8][3*5+4*7 3*6+4*8]


print("8 点乘（元素相乘）".center(100, "-"))
print(np.multiply(A, B))
# [[ 5 12]
#  [21 32]]
# 算法：[1*5 2*6][3*7 4*8]