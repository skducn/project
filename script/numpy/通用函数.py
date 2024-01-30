# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2024-1-29
# Description: 通用函数
# 通用函数(即ufunc)是一种对ndarray中的数据执行元素级运算的函数。
# 你可以将其看做简单函数(接受一个或多个标量值，并产生一个 或多个标量值)的矢量化包装器。
# *****************************************************************

import numpy as np

arr = np.arange(10)

# todo 一元ufunc
# abs()  求整数、浮点数或复数的绝对值。对于非复数值，可以使用更快的fabs()
# sqrt() 求平方根，相当于 arr**0.5
# square() 求平方，相当于 arr**2
# exp() 求指数e的x次方
# log,log10,log2,log1p() 分别求自然对数底数e、底数10、底数2、log（1+x）
# sign() 求正负号 1（正数）、-1（负数）或0（0）
# ceil() 求整数的上取整，即求大于等于x的最小整数
# floor() 求整数的下取整，即求小于等于x的最大整数
# rint() 求整数的四舍五入，相当于 round(x)
# modf() 将数组的小数和整数部分以两个独立数组的形式返回
# isnan 返回一个布尔数组，数组元素是否为NaN
# isfinite、isinf、isnan、isfinite() 用于检测数组中是否含有NaN、正无穷和负无穷的元素
# cos、cosh、思念、sinh、tan、tanh() 用于计算数组中各元素的正弦、余弦、正切、hyperbolic sine等函数
# arccos、arccosh、arcsin arcsinh、arctan、arctanh() 用于计算数组中各元素的双曲余弦、双曲正切等函数
# logical_not 求not x的真值，相当于 -arr

print(np.sqrt(arr))
# [0.         1.         1.41421356 1.73205081 2.         2.23606798
#  2.44948974 2.64575131 2.82842712 3.        ]

print(np.modf(arr))  # (array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]), array([0., 1., 2., 3., 4., 5., 6., 7., 8., 9.]))

# todo 二元ufunc
# add 数组中对应的元素相加，相当于 arr1 + arr2
# subtract 从arr1中减去arr2的元素，相当于 arr1 - arr2
# multiply 数组中对应的元素相乘，相当于 arr1 * arr2
# divide 从arr1中减去arr2的元素，相当于 arr1 / arr2
# maximum 数组中对应位置的最大值，相当于 arr1 > arr2 ? arr1 : arr2 ，fmax() 忽略NaN
# minimum 数组中对应位置的最小值，相当于 arr1 < arr2 ? arr1 : arr2 ，fmin() 忽略NaN
# greater 数组中对应位置的真值，arr1 > arr2 ? 1 : 0
# divide、floor_divide、remainder、fmod、hypot() 用于计算两个数组中对应位置的除法、取整、余数、模、平方根的和
# power 数组中对应位置的幂，相当于 arr1 ** arr2
# copysign() 用于将两个数组对应位置的符号相同，符号不同则取符号 opposite() 用于将两个数组对应位置的符号相反，符号相同则取符号 opposite() 用于将两个数组对应位置的符号相反，符号相同则取符号
# less、less_equal、equal、not_equal、greater_equal、greater() 用于比较两个数组对应位置的元素
# bitwise_and 二进制位与，相当于 arr1 & arr2
# bitwise_or 二进制位或，相当于 arr1 | arr2
# bitwise_xor 二进制位异或，相当于 arr1 ^ arr2
# bitwise_not 二进制位非，相当于 ~arr1
# bitwise_and、bitwise_or、bitwise_xor、bitwise_not() 用于计算两个数组中对应位置
# logical_and() 用于计算两个数组中对应位置的真值，相当于 arr1 & arr2
# logical_or() 用于计算两个数组中对应位置的真值，相当于 arr1 | arr2
# logical_xor() 用于计算两个数组中对应位置的真值，相当于 arr1 ^ arr2
# logical_not() 用于计算两个数组中对应位置的真值，相当于 ~arr1
# maximum.reduce() 用于计算数组中最大值，相当于 arr.max()