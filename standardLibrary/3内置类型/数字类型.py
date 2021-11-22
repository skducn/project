# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-11-19
# Description: # 内置类型 -  数字类型 int, float, complex
# https://docs.python.org/zh-cn/3.7/library/stdtypes.html#truth-value-testing
# *****************************************************************

import sys

print("1，用sys.float_info 查看程序运行所在机器上浮点数的精度".center(100, "-"))
print(sys.float_info)

print("2，/求商".center(100, "-"))
print(6//2)  # 3

print("3，//求商数（整数除法），结果值是一个整数，但结果的类型不一定是 int。".center(100, "-"))
print(5//3)  # 1
print(type(5//3))  # <class 'int'>
# 运算结果总是向负无穷的方向舍入，如下：
print(1//2)  # 0
print(-1//2)  # -1
print(1//-2)  # -1
print(-1//-2)  # 0

print("4，x 的 y 次幂(等同于 x**y)".center(100, "-"))
# 注意：0**0 =1 这是编程语言的普遍做法。
print(pow(0, 0))  # 1
print(0**0)  # 1

print("5，float也接受字符串 nan 和 inf".center(100, "-"))
# 5，float 也接受字符串 "nan" 和附带可选前缀 "+" 或 "-" 的 "inf" 分别表示非数字 (NaN) 以及正或负无穷。
# INF / inf：这个值表示“无穷大 (infinity 的缩写)”，即超出了计算机可以表示的浮点数的最大范围(或者说超过了 double 类型的最大值)。
x = "nan"
print(float(x))  # nan
print(type(float(x)))  # <class 'float'>
x = "-inf"
print(float(x))  # -inf
x = "+inf"
print(float(x))  # inf
x = "inf"
print(float(x))  # inf
print(type(float(x)))  # <class 'float'>
print(1 + float('inf'))  # inf    //用 inf 做简单加、乘算术运算仍会得到 inf
print(2 * float("inf"))  # inf
print(0 * float("inf"))  # nan   //但是用 inf 乘以0会得到 not-a-number(NaN)
print(889 / float('inf'))  # 0.0   //除了inf外的其他数除以inf，会得到0
print(float('inf')/float('inf'))  # nan
# 不等式： 当涉及 > 和 < 运算时， 所有数都比 -inf 大；所有数都比 +inf 小；等式： +inf 和 +inf 相等；-inf 和 -inf 相等。


# print("6，x % y 的余数，不可用于复数".center(100, "-"))
# 6，x % y 的余数，不可用于复数。 而应在适当条件下使用 abs() 转换为浮点数。

print("7，divmod（x, y） 表示求商数求余数".center(100, "-"))
# 如(x // y, x % y)
print(divmod(5, 3))  # (1,2)


print("8，关于复数".center(100, "-"))
# 从浮点数转换为整数会被舍入或是像在 C 语言中一样被截断；请参阅 math.floor() 和 math.ceil() 函数查看转换的完整定义。
x = 2.4 + 5.6j
print(x)  # (2.4+5.6j)
y = 4.4j
print(y)  # 4.4j    //没有实部


print("9，浮点数转整数".center(100, "-"))
import math
print(math.trunc(111.73))   # 111  //x 截断为 Integral
print(math.floor(100.56))  # 100   //<= x 的最大 Integral
print(math.ceil(100.01))   # 101   //>= x 的最小 Integral
print(round(123.45, 1))   # 123.5   //四舍五入保留1位
print(round(123.44, 1))   # 123.4   //四舍五入保留1位



