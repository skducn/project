# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2022-3-21
# Description: 等差数列 np.linspace()
# numpy.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None)
# start 采样的起点
# stop 采样的终点
# num 采样的点个数，默认为50个，必须是非负数。
# endpoint 判断是否包括stop值，默认为true即包括stop值.
# retstep 当为true时，返回值是（samples，step）格式，step为样本之间的间距，默认为 false
# dtype 为输出数组的类型，如果dtype没有给出，则从其他输入参数推断数据类型。
# *****************************************************************

import numpy as np


print("1 等差数列".center(100, "-"))
print(np.linspace(-5, 5, 5))  # [-5.  -2.5  0.   2.5  5. ]

print(np.linspace(-5, 5, 5, endpoint=False))  # [-5. -3. -1.  1.  3.]

print(np.linspace(-5, 5, 5, endpoint=False, retstep=True))  # (array([-5., -3., -1.,  1.,  3.]), 2.0)

print(np.linspace(-5, 5, 5, False, True, dtype=int))  # (array([-5, -3, -1,  1,  3]), 2.0)