# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2022-3-21
# Description: 常用数学运算 min,max,mean,sum,exp,around,sqrt

# *****************************************************************

import numpy as np

n = np.array([[5, 10, 15],
              [20, 125, 30],
              [35, 40, 45]])
print(n)

print("1 min()最小值".center(100, "-"))
print(n.min())  # 5


print("2 max()最大值".center(100, "-"))
print(n.max())  # 125
print(n.max(axis=0))  # [ 35 125  45]  //将每列中最大值组成数组
print(n.max(1))  # [ 15 125  45]  //将每行中最大值组成数组


print("3 mean()平均值".center(100, "-"))
print(n.mean().round(2))  # 36.11  //平均值保留2位
print(n.mean(0))  # [20.         58.33333333 30.        ]  //将每列求平均值组成数组
print(n.mean(1))  # [10.         58.33333333 40.        ]  //将每行求平均值组成数组



print("4 sum()求和".center(100, "-"))
print(n.sum())  # 325
print(n.sum(axis=0))  # [ 60 175  90]  //将每列求和组成数组
print(n.sum(axis=1))  # [ 30 175 120]  //将每行求和组成数组


print("5 exp()e的x幂次方".center(100, "-"))
n1 = np.arange(5)
print(np.exp(n1))  # [ 1.          2.71828183  7.3890561  20.08553692 54.59815003]



print("6 around()四舍五入,可指定精度".center(100, "-"))
# around(a, decimals=0, out=None)
# decimals 要舍入的小数位数。 默认值为0。 如果为负，整数将四舍五入到小数点左侧的位置
n = np.array([-0.746, 4.6, 9.4, 7.447, 10.455, 11.555])
print(np.around(n))  # [-1.  5.  9.  7. 10. 12.]
print(np.around(n, decimals=1))  # [-0.7  4.6  9.4  7.4 10.5 11.6]


print("7 sqrt()开根号".center(100, "-"))
print(np.sqrt(n1))  # [0.         1.         1.41421356 1.73205081 2.        ]



