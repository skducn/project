# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-11-19
# Description: # abs(x) 绝对值
# 定义：返回一个数的绝对值。实参可以是整数或浮点数。如果实参是一个复数，返回它的模。
# 关于复数的模，将复数的实部与虚部的平方和的正的平方根的值称为该复数的模，如 z = a + bi , 复数z的模|z|=（a的平方+b的平方）的平方根

# 标准库：https://docs.python.org/zh-cn/3.7/library/functions.html#abs
# *****************************************************************

# 复数
complex = 2 + 5j
complex2 = 5 - 6j


print("1，整数或浮点数的绝对值".center(100, "-"))
print(abs(100))  # 100
print(abs(-100))  # 100
print(abs(-100.12))  # 100.12

print("2，复数的绝对值返回模".center(100, "-"))
print(type(complex))  # <类与实例 'complex'>
print(abs(complex))  # 5.385164807134504   //返回模


# 以下关于复数

print("3，复数的实部 real".center(100, "-"))
print(complex.real)  # 2.0

print("4，复数的虚部 imag".center(100, "-"))
print(complex.imag)  # 5.0

print("5，复数的共轭复数 conjugate".center(100, "-"))
# 共轭复数： 两个实部相等，虚部互为相反数的复数互为共轭复数。
# 轭是一个汉字，读作è，本意是指驾车时套在牲口脖子上的曲木，引申义是束缚，控制。
print(complex.conjugate())  # (2-5j)

# 复数的加法，实部加实部，虚部加虚部；
# 复数的减法，实部减实部，虚部减虚部；
# 复数的乘法： 设z1=a+bj，z2=c+dj是任意两个复数，那么它们的积(a+bj)(c+dj)=(ac-bd)+(bc+ad)j；

print("6，两复数相加，即两复数的实部相加，虚部相加；".center(100, "-"))
print(complex + complex2)  # (7-1j)

print("7，两复数相减，即两复数的实部相减，虚部相减；".center(100, "-"))
print(complex - complex2)  # (-3+11j)

print("8，两复数相乘，即实部由两复数的实部相乘后做减法（被乘数减乘数），虚部由被乘数的虚部乘以乘数的实部 加上 被乘数的实部乘以乘数的虚部 ；".center(100, "-"))
print(complex * complex2)  # (40+13j)   //(2*5-(5*-6)) + (5*5+2*(-6)j) = (40+13j)

