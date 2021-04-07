# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-3-19
# Description: numpy (Numerical Python) 多维数组对象
# NumPy 是一个运行速度非常快的数学库，主要用于数组计算
# ndarray = N-dimensional array 多维度数组
# 一个强大的N维数组对象 ndarray
# 广播功能函数
# 整合 C/C++/Fortran 代码的工具
# 线性代数、傅里叶变换、随机数生成等功能
# NumPy 通常与 SciPy（Scientific Python）和 Matplotlib（绘图库）一起使用， 这种组合广泛用于替代 MatLab，是一个强大的科学计算环境，有助于我们通过 Python 学习数据科学或者机器学习。
# SciPy 是一个开源的 Python 算法库和数学工具包。
# SciPy 包含的模块有最优化、线性代数、积分、插值、特殊函数、快速傅里叶变换、信号处理和图像处理、常微分方程求解和其他科学与工程中常用的计算。
# Matplotlib 是 Python 编程语言及其数值数学扩展包 NumPy 的可视化操作界面。它为利用通用的图形用户界面工具包，如 Tkinter, wxPython, Qt 或 GTK+ 向应用程序嵌入式绘图提供了应用程序接口（API）。
# NumPy 官网 http://www.numpy.org/
# NumPy 源代码：https://github.com/numpy/numpy
# SciPy 官网：https://www.scipy.org/
# SciPy 源代码：https://github.com/scipy/scipy
# Matplotlib 官网：https://matplotlib.org/
# Matplotlib 源代码：https://github.com/matplotlib/matplotlib
# *****************************************************************

import numpy as np
import pandas as pd

obj = pd.Series([1,2,3,4])
print(obj)

print("1 生成一维数组并获取元素".center(100, "-"))
print(np.arange(10))  # [0 1 2 3 4 5 6 7 8 9]
# for i in range(len(np.arange(10))):
#     print(np.arange(10)[i])
print(np.arange(1, 10))  # [1 2 3 4 5 6 7 8 9]
print(np.arange(1, 10, 3))  # [1 4 7]
print(np.arange(1, 10, 3)[2])  # 7



print("2 获取多维数组中的元素".center(100, "-"))
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


print("5 列表的统计与重复".center(100, "-"))
x = np.array([1, 2, 3])
print(x.mean())   # 2.0  //计算列表中所有值的平均数
print(x.sum())   # 6  //计算列表中所有值的合计

print(np.tile(x, 1))  # [1,2,3]
print(np.tile(x, 2))   # [1,2,3,1,2,3]   //横向重复*2次
print(np.tile(x, 4))   # [1 2 3 1 2 3 1 2 3 1 2 3]  //横向重复*4次
print(np.tile(x, (1, 2)))   # [1,2,3,1,2,3]  //横向重复*2次
print(np.tile(x, (2, 2)))   # [1,2,3,1,2,3],[1,2,3,1,2,3]  //横向与纵向各重复*2次
print(np.tile(x, (2, 1)))   # [1,2,3],[1,2,3]  //纵向重复*2次


print("6 随机生成N行M列的二维数组".center(100, "-"))
arr = np.random.rand(4, 4)
# [[0.50398151 0.49137049 0.57337883 0.8637965 ]
#  [0.45352152 0.02176194 0.09520183 0.86945503]
#  [0.56745522 0.65480827 0.02221036 0.90495728]
#  [0.70681986 0.19456123 0.5346386  0.95599382]]
print(arr)


