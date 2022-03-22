# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2022-3-21
# Description: 随机数数组
# np.random.randint()   返回随机整数
# numpy.random.randint(low, high=None, size=None, dtype=’i’)
# 范围区间为[low,high），包含low，不包含high
# 参数：low为最小值，high为最大值，size为数组维度大小，dtype为数据类型，默认的数据类型是np.int
# high没有填写时，默认生成随机数的范围是[0，low)

# np.random.randn()  返回一个或一组样本，具有标准正态分布。
# numpy.random.randn(d0,d1,…,dn)
# dn表格每个维度
# 返回值为指定维度的array
# 标准正态分布—-standard normal distribution
# 标准正态分布又称为u分布，是以0为均值、以1为标准差的正态分布，记为N（0，1）。

# np.random.choice()  从给定的一维数组中生成随机数
# numpy.random.choice(a, size=None, replace=True, p=None)
# a为一维数组类似数据或整数；size为数组维度；当replace为False时，生成的随机数不重复; p为数组中的数据出现的概率
# a为整数时，对应的一维数组为np.arange(a)
# p的长度与a的长度应一致 且 p数据之和应为1

# np.random.seed() 使得随机数据可预测，可确定
# 与 np.random.rand() 配合使用，当设置相同的seed，每次生成的随机数相同。

# 生成[0,1)之间的浮点数
# np.random.random_sample()
# np.random.random()
# np.random.ranf()
# np.random.sample()
# *****************************************************************

import numpy as np


print("1 随机生成5个[0,1)之间的整数，也就是0".center(100, "-"))
print(np.random.randint(1, size=5))  # [0 0 0 0 0]


print("2 随机生成[1,5)之间的1个整数".center(100, "-"))
print(np.random.randint(1, 5))  # 3


print("3 随机生成[-5，5)之间的二维（3*2）整数".center(100, "-"))
print(np.random.randint(-5, 5, size=(3, 2)))
# [[-4 -1]
#  [-3 -3]
#  [ 3 -5]]


print("4 随机生成6行4列的值".center(100, "-"))
print(np.random.randn(6, 4))
# [[ 0.32314679  1.23325152 -2.1016414  -0.06127316]
#  [ 1.51479541 -1.28828059 -1.06433812  0.17173979]
#  [-0.8170658   1.25234848 -0.22049326  0.92720949]
#  [-0.14603881  1.06924451  0.57540857 -0.24223491]
#  [ 2.08319112 -0.09651141  0.95922309 -0.87515154]
#  [ 0.59251939 -0.60462325  1.1159383  -0.56848018]]



print("5 随机生成3个2行4列值".center(100, "-"))
print(np.random.randn(3, 2, 4))
# [[[ 0.15401664 -1.51134509  0.15166834 -1.54365455]
#   [ 1.66948221  1.63047723 -2.1197293  -0.28258025]]
#
#  [[-1.73558635 -0.37080485 -0.68901723 -0.04386469]
#   [-0.04296036  0.32244412 -0.8690349  -0.3154619 ]]
#
#  [[-2.21120948 -0.29722982  1.20499195  0.72950365]
#   [-0.90711593  2.13048125  0.18490091 -1.48507351]]]



print("6 在[0,4]区间内随机生成3个整数，且3个数不重复".center(100, "-"))
print(np.random.choice(5, 3, replace=False))  # [1 2 4]

print("7 在[0,4]区间内随机生成3个整数，且3个数中可以重复".center(100, "-"))
print(np.random.choice(5, 3, replace=True))  # [1 2 2]

print("8 在[0,4]区间内随机生成3*2个整数".center(100, "-"))
print(np.random.choice(5, size=(3, 2)))
# [[0 4]
#  [1 3]
#  [1 2]]

print("9 在demo列表内随机生成3*3个元素".center(100, "-"))
demo = ['lenovo', 'sansumg', 'moto', 'xiaomi', 'iphone']
print(np.random.choice(demo, size=(3, 3)))
# [['moto' 'moto' 'iphone']
#  ['moto' 'moto' 'iphone']
#  ['sansumg' 'lenovo' 'xiaomi']]

print("10 在demo列表内随机生成3*3个元素，每个元素的出现的概率分别为 0.1, 0.6, 0.1, 0.1, 0.1".center(100, "-"))
demo = ['lenovo', 'sansumg', 'moto', 'xiaomi', 'iphone']
print(np.random.choice(demo, size=(3, 3), p=[0.1, 0.6, 0.1, 0.1, 0.1]))
# [['sansumg' 'sansumg' 'sansumg']
#  ['lenovo' 'sansumg' 'sansumg']
#  ['sansumg' 'moto' 'iphone']]


print("10 设置seed为0，rand()每次生成的随机数相同".center(100, "-"))
np.random.seed(0)
print(np.random.rand(5))  # [0.5488135  0.71518937 0.60276338 0.54488318 0.4236548 ]
np.random.seed(0)
print(np.random.rand(5))  # [0.5488135  0.71518937 0.60276338 0.54488318 0.4236548 ]

np.random.seed(1676)
print(np.random.rand(5))  # [0.39983389 0.29426895 0.89541728 0.71807369 0.3531823 ]
np.random.seed(1676)
print(np.random.rand(5))  # [0.39983389 0.29426895 0.89541728 0.71807369 0.3531823 ]


print("11 生成[0,1)之间的浮点数".center(100, "-"))
print('-----------random_sample--------------')
print(np.random.random_sample(size=(2,2)))
print('-----------random--------------')
print(np.random.random(size=(2,2)))
print('-----------ranf--------------')
print(np.random.ranf(size=(2,2)))
print('-----------sample--------------')
print(np.random.sample(7))