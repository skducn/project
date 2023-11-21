# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-1-27
# Description   : 变量与运算
# *****************************************************************


# 1，unbound变量，选择性赋值
x = 0
mult = 1024 if x else 500
print(mult)  # 500


# 2，print不换行
print("123", end="")
print("456")   # 123456



# 4，运算符
print(11/2)   # 5.5   / 浮点除法运算符
print(11//2)    # 5    //整数除法运算符
print(-11//2)  # -6    //带负数的四舍五入取整。
print(11.0//2)  # 5.0

# 5，分数
import fractions
x = fractions.Fraction(1, 3)
print(x)  # 1/3
print(type(x))  # <类与实例 'fractions.Fraction'>
print(x*2)  # 2/3



# 6，零值是false， 非零值是true
x = 0.0   # 为假，false
if 0.0 == 0: print("0.0=0")
# x = fractions.Fraction(0, 3)  # 为假
# x = fractions.Fraction(10, 0)  # 报错，分母不能为0
# x = 0.0000000000000000000000000000001   # 为真
if x:
    print("true")
else:
    print("false")

















