# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-3-19
# Description: numpy 数组操作的基石
# Python3已将numpy库作为内置库
# *****************************************************************

import numpy as np

# 实例1，创建一维数组
print(np.arange(10))  # [0 1 2 3 4 5 6 7 8 9]
print(np.arange(1, 10))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(np.arange(1, 10, 3))  # [1 4 7]

# 实例2，创建二维数组
print(np.array([[1, 2], [3, 4]])) #参数为列表
# array([[1, 2],
#        [3, 4]])
print(np.array(([1, 2], [3, 4])))  # 参数为元组
# array([[1, 2],
#        [3, 4]])
print(np.array(((1, 2), (3, 4))))  #参数为元组
# array([[1, 2],
#        [3, 4]])

M = np.array(((np.arange(3)), (np.arange(3))))
print(M)
# array([[0, 1, 2],
#        [0, 1, 2]])
print(M.shape)  # (2, 3)

M = np.array(([np.arange(2)], [np.arange(3)]))
print(M)
# array([[array([0, 1])],
#        [array([0, 1, 2])]], dtype=object)
print(M.shape)
# (2, 1)

M = np.array(([np.arange(2)],[np.arange(2)]))
print(M)
# array([[[0, 1]],
#
#        [[0, 1]]])
print(M.shape)
# (2, 1, 2)


# 实例，数组中两个列表矩阵值相加
a = [0, 1, 2]
b = [2, 1, 3]
x = np.array([a, b])
arr_a = np.sum(x, axis=0)  # [2 2 5]   //矩阵列相加
arr_b = np.sum(x, axis=1)  # [3 6]  //单个列表所有元素相加
print(arr_a)
print(arr_b)
print(type(arr_a))  # <class 'numpy.ndarray'>
for i in range(len(arr_b)):
    print(arr_b[i])
# 3
# 6


x = np.array([1, 2, 3])
print(np.tile(x, 1))  # array([1,2,3])
print(np.tile(x, 2))   # array([1,2,3,1,2,3])   //一维，重复1次
print(np.tile(x, 4))   # [1 2 3 1 2 3 1 2 3 1 2 3]  //一维，重复4次
print(np.tile(x, (1, 2)))   # array([1,2,3,1,2,3])
print(np.tile(x, (2, 2)))   # array([1,2,3,1,2,3],[1,2,3,1,2,3])  //二维，重复1次
print(np.tile(x, (2, 1)))   # array([1,2,3],[1,2,3])  //二维