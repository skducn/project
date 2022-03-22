# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2022-3-21
# Description: 未初始化数组 np.empty()
# np.empty 构造一个长度为 shape 的未初始化数组，这个数组的元素可能是内存位置上存在的任何数值。
# empty(shape, dtype=float, order='C')
# *****************************************************************

import numpy as np


print("1 创建5个浮点数1的一维数组".center(100, "-"))
a = np.empty(shape=3)  # 等同于 a = np.empty(3)
print(a)  # [1.74928933e+243 1.69375778e+190 1.38496762e+219]
print(a.dtype)  # float64


print(np.empty(shape=(2, 3)))
# [[6.23042070e-307 1.16824187e-307 2.22522597e-306]
#  [1.33511969e-306 1.37962320e-306 1.78019354e-306]]

print(np.empty(shape=(2, 3), dtype=int))
# [[1769172581  975206772 1633971744]
#  [2036429426  538976266  538976288]]



