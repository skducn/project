# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-3-19
# Description: numpy 多维数组对象
# Python3已将numpy库作为内置库
# *****************************************************************

import numpy as np
import pandas as pd

obj = pd.Series([1,2,3,4])
print(obj)

print("1 创建一维数组".center(100, "-"))
print(np.arange(10))  # [0 1 2 3 4 5 6 7 8 9]
# for i in range(len(np.arange(10))):
#     print(np.arange(10)[i])
print(np.arange(1, 10))  # [1 2 3 4 5 6 7 8 9]
print(np.arange(1, 10, 3))  # [1 4 7]
print(np.arange(1, 10, 3)[2])  # 7



print("2 获取多维数组中的值".center(100, "-"))
print(np.array([[1, 2], [3, 4]]))  # 参数为列表
# [[1, 2], [3, 4]]
print(np.array(([5, 6], [7, 8])))  # 参数为元组
# [5, 6], [7, 8]]
print(np.array(((9, 10), (11, 12))))  # 参数为元组
# [[9, 10], [11, 12]]
print(np.array(((9, 10), (11, 12)))[1][0])  # 11



print("3 创建多维数组及获取列表维度".center(100, "-"))
M = np.array(((np.arange(3)), (np.arange(3))))
print(M)  # [[0, 1, 2],[0, 1, 2]]
print(M.shape)  # (2, 3)   # 获取列表行列维度。
print(M.ndim)  # 2    //表示二维列表

X = np.array(((np.arange(3))))
print(X.ndim)  # 1  //ndim维度，表示一维列表。
print(X.dtype)  # int32   //dtype数据类型


print("4 两个列表矩阵值相加与单加".center(100, "-"))
a = [0, 1, 2]
b = [2, 1, 3]
x = np.array([a, b])
arr_a = np.sum(x, axis=0)  # [2 2 5]   //矩阵列相加
arr_b = np.sum(x, axis=1)  # [3 6]  //单列表所有元素相加
print(arr_a)
print(arr_b)
print(type(arr_a))  # <class 'numpy.ndarray'>
for i in range(len(arr_b)):
    print(arr_b[i])
# 3
# 6


print("5 列表维度与值的叠加".center(100, "-"))
x = np.array([1, 2, 3])
print(x.mean())   # 2.0  //计算列表中所有值的平均数
print(x.sum())   # 6  //计算列表中所有值的合计

print(np.tile(x, 1))  # [1,2,3]
print(np.tile(x, 2))   # [1,2,3,1,2,3]   //一维，重复*2次
print(np.tile(x, 4))   # [1 2 3 1 2 3 1 2 3 1 2 3]  //一维，重复*4次
print(np.tile(x, (1, 2)))   # [1,2,3,1,2,3]  //一维嵌套重复1次
print(np.tile(x, (2, 2)))   # [1,2,3,1,2,3],[1,2,3,1,2,3]  //二维嵌套重复*2次
print(np.tile(x, (2, 1)))   # [1,2,3],[1,2,3]  //二维，重复*1次


print("6 生产一个4行4列的二维数组".center(100, "-"))
arr = np.random.rand(4, 4)
# [[0.50398151 0.49137049 0.57337883 0.8637965 ]
#  [0.45352152 0.02176194 0.09520183 0.86945503]
#  [0.56745522 0.65480827 0.02221036 0.90495728]
#  [0.70681986 0.19456123 0.5346386  0.95599382]]
print(arr)
print(arr.mean())   # 0.5258695184297864  //计算平均数

