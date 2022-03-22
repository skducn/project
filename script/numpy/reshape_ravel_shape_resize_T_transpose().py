# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2022-3-21
# Description: reshape、ravel、shape、resize、.T、transpose
# reshape() 修改维度，不影响原数组维度，需赋新变量  # numpy.reshape(a, newshape, order='C')
# ravel() 多维转一维，不影响原数组维度，需赋新变量
# shape()=值  赋值修改原数组维度
# resize() 修改原值维度
# *****************************************************************

import numpy as np


print("1 reshape修改维度，不修改原数组，有返回值".center(100, "-"))
n1 = np.array([1, 2, 3, 4, 5, 6, 7, 8])
n2 = n1.reshape(2, 4)
print(n2.ndim)  # 2


print("2 reshape修改维度，第三个参数-1系统自己计算，因确定前两个维度，第三个维度的值本身就已经确定了".center(100, "-"))
n3 = n1.reshape(2, 2, -1)
print(n3)
# [[[1 2]
#   [3 4]]
#
#  [[5 6]
#   [7 8]]]
print(n3.ndim)  # 3

print("3 reshape修改维度，第三个参数-1系统自己计算，因确定前两个维度，第三个维度的值本身就已经确定了".center(100, "-"))
n4 = n1.reshape(4, 2, -1)
print(n4)
# [[[1]
#   [2]]
#
#  [[3]
#   [4]]
#
#  [[5]
#   [6]]
#
#  [[7]
#   [8]]]
print(n4.ndim)  # 3


print("4 ravel多维转一维,不修改原数组，有返回值".center(100, "-"))
n5 = n3.ravel()
print(n5)  # [1 2 3 4 5 6 7 8]


print("5 shape() 赋值修改原数组维度".center(100, "-"))
print(n3.shape)  # (2, 2, 2)
print(n3)
n3.shape = 8
print(n3)
print(n3.shape)  # (8,)  // (8, ) ≠ (8, 1)：前者表示一维数组（无行和列的概念），后者则表示一个二维数组，也即是一个列向量；

print("6 resize() 修改原值维度".center(100, "-"))
n3.resize(2, 4)
print(n3)
# [[1 2 3 4]
#  [5 6 7 8]]


print("7 转置T 与 np.transpose()".center(100, "-"))
print(n3.T)  # 等同于 np.transpose(n3)
# [[1 5]
#  [2 6]
#  [3 7]
#  [4 8]]
