# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2022-3-21
# Description: 步长数组 np.arange()  左开右闭即包含左边，不包含右边
# *****************************************************************

import numpy as np


print("1, arange() 生成序列数组(默认int32)".center(100, "-"))
print(np.arange(10))  # [0 1 2 3 4 5 6 7 8 9]
print(np.arange(1, 10))  # [1 2 3 4 5 6 7 8 9]
print(np.arange(1, 10, 3))  # [1 4 7]
print(np.arange(1, 10, 3)[2])  # 7
a = np.arange(1, 13)
print(a)  # [ 1  2  3  4  5  6  7  8  9 10 11 12]
print(a.dtype)  # int32


print("3.2, arange().reshape() 生成序列多维数组".center(100, "-"))
a = np.arange(1, 25).reshape(4, 2, 3)  # reshape表示重新定义维度，如：4个2行3列的多维数组
print(a)
# [[[ 1  2  3]
#   [ 4  5  6]]
#
#  [[ 7  8  9]
#   [10 11 12]]
#
#  [[13 14 15]
#   [16 17 18]]
#
#  [[19 20 21]
#   [22 23 24]]]



print("3 创建[1,8]区间3*3二维浮点数数组".center(100, "-"))
print(np.arange(9.).reshape(3, 3))
# [[0. 1. 2.]
#  [3. 4. 5.]
#  [6. 7. 8.]]