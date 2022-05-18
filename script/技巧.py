# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2021-5-18
# Description: ...对象，获取矩阵第二列的值，解压迭代对象，展开的艺术，异常处理中巧用else，迭代器切片slice获取区间项
# Python编程进阶，常用八大技巧！ http://www.51testing.com/html/11/n-6391311.html
# ********************************************************************************************************************

#todo 技巧1 ...对象，即Ellipsis对象，一个特殊值，可表示空函数的占位符和numpy中的切片操作。
#以下三个函数功能是一样的
def myfunc():
    ...

def myfunb():
    Ellipsis

def myfuna():
    pass


#todo 技巧2，获取矩阵第二列的值(只用于numpy)
import numpy as np
arr = np.arange(27).reshape(3,3,3)
print(arr)
# [[[ 0  1  2]
#   [ 3  4  5]
#   [ 6  7  8]]
#
#  [[ 9 10 11]
#   [12 13 14]
#   [15 16 17]]
#
#  [[18 19 20]
#   [21 22 23]
#   [24 25 26]]]
print(arr[..., 1])
# [[ 1  4  7]
#  [10 13 16]
#  [19 22 25]]


#todo 技巧3，解压迭代对象
a, *b, c = range(1, 11)
print(a)  # 1
print(b)  # [2, 3, 4, 5, 6, 7, 8, 9]
print(c)  # 10


#todo 技巧4，展开的艺术之列表数组（不支持数字）
l = [[1, 2, 3], [4, 5, 6,333], (9,5), {"abc":123},"jinhao",str(66),[7, 8, 9]]
flattened = [e for sublist in l for e in sublist]
print(flattened)  # [1, 2, 3, 4, 5, 6, 333, 9, 5, 'abc', 'j', 'i', 'n', 'h', 'a', 'o', '6', '6', 7, 8, 9]


#todo 技巧，展开的艺术之reduce
# reduce和lambda组合起来，就能针对 l 数组内的每个子数组做拼接操作。
from functools import reduce
l = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(reduce(lambda x,y: x+y, l)) # [1, 2, 3, 4, 5, 6, 7, 8, 9]


#todo 技巧6，展开的艺术之sum降维合并
# 即对二维数组做sum操作，就能展开为一维数组。其实相当于 [] + [1, 2, 3] + [4, 5, 6] + [7, 8, 9]
l = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(sum(l, []))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
# 同理，对三位数组做sum操作，就能使其变为二维数组，此时再对二维数组做sum操作，就能展开为一维数组。
l = [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]]
print(sum(l, []))  # [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(sum(sum(l, []), []))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]


#todo 技巧7，异常处理中巧用else，即在 try ... except ... 中使用 else 编写未捕获到异常时的逻辑

try:
    t = 123
except:
    print("test")
else:
    print("未出错here")
# 未出错here


#todo 技巧8，迭代器切片slice获取区间项
import itertools
s = itertools.islice([1, 2, 3, 4, 5], 3, 5)  # <itertools.islice object at 0x7f70fab88138>
for val in s:
    print(val)
# 4
# 5

