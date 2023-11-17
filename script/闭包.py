# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2023-2-13
# Description   : 闭包
# 函数嵌套, 将内部函数作为外部函数的返回值，内部函数调用外部函数的变量
# https://www.cnblogs.com/yssjun/p/9887239.html
# *********************************************************************

def make_average():

    # 自由变量
    l_nums = []

    # 闭包函数
    def average(n):
        # 计算列表的平均值，将数值添加到列表中
        l_nums.append(n)
        # 返回平均值
        return sum(l_nums) / len(l_nums)
    return average

# 调用外部函数，并将其复制给一个变量，注意：此时返回的是内函数的内存地址
a = make_average()
print(a)  # <function make_average.<locals>.average at 0x7fdfa94c4af0>
print(a(20))  # 给average函数传入参数20， 20/1 = 20
print(a(30))  # 给average函数传入参数30，（20+30）/2 = 25
print(a(100)) # 给average函数传入参数100，（20+30+100）/3 = 50

def my_func(*args):
    fs = []
    for i in range(3):
        def func():
            return i * i
        fs.append(func)
    return fs

fs1, fs2, fs3 = my_func()
print(fs1())  # 0
print(fs2())  # 1
print(fs3())  # 4

def my_func(*args):
    fs = []
    for i in range(3):
        def func(_ = i):
            return _ * _
        fs.append(func)
    return fs

fs1, fs2, fs3 = my_func()
print(fs1())  # 0
print(fs2())  # 1
print(fs3())  # 4
