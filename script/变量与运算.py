# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-1-27
# Description   : 变量与运算
# *****************************************************************

'''

1.1，选择性赋值
1.2，解压迭代赋值

2，print不换行用end=""
3，运算符
4，分数

'''


print("1.1，选择性赋值".center(100, "-"))
x = 0
mult = 1024 if x else 500
print(mult)  # 500


print("1.2，解压迭代赋值".center(100, "-"))
a, *b, c = range(1, 11)
print(a)  # 1
print(b)  # [2, 3, 4, 5, 6, 7, 8, 9]
print(c)  # 10



print("2，print不换行".center(100, "-"))
print("123", end="")
print("456")   # 123456


print("3，运算符".center(100, "-"))
print(11/2)   # 5.5   / 浮点除法运算符
print(11//2)    # 5    //整数除法运算符
print(-11//2)  # -6    //带负数的四舍五入取整。
print(11.0//2)  # 5.0


print("4，分数".center(100, "-"))
import fractions
x = fractions.Fraction(1, 3)
print(x)  # 1/3
print(type(x))  # <class 'fractions.Fraction'>
print(x*2)  # 2/3


print("5，0等于false，非0等于true".center(100, "-"))
x = 0.0   # false
if x:
    print("true")
else:
    print("false")

if 0.0 == 0:
    print("是的，0.0=0 你没看错")

# x = fractions.Fraction(0, 3)  # 为假
# x = fractions.Fraction(10, 0)  # 报错，分母不能为0
# x = 0.0000000000000000000000000000001   # 为真


















