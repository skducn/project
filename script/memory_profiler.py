# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2022-2-28
# Description: # memory_profiler 分析记录Python脚本中，执行到每一行时，内存的消耗及波动变化情况
# pip3.9 install memory_profiler
# profile并作为要分析的目标函数的装饰器即可
# Line #列记录了分析的各行代码具体行位置，
# Mem usage列记录了当程序执行到该行时，当前进程占用内存的量，
# Increment记录了当前行相比上一行内存消耗的变化量，
# Occurrences记录了当前行的执行次数(循环、列表推导等代码行会记作多次)，
# Line Contents列则记录了具体对应的行代码。
# *****************************************************************
import numpy as np
from memory_profiler import profile
import time
@profile
def demo():
    a = np.random.rand(10000000)
    b = np.random.rand(10000000)
    a_ = a[a < b]
    b_ = b[a < b]

    del a, b
    return a_, b_

if __name__ == '__main__':
    demo()