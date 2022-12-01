# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2021-5-18
# Description: ...对象，获取矩阵第二列的值，解压迭代对象，展开的艺术，异常处理中巧用else，迭代器切片slice获取区间项
# Python编程进阶，常用八大技巧！ http://www.51testing.com/html/11/n-6391311.html
# ********************************************************************************************************************

import numpy as np


'''
1，表示空函数的占位符的三种方法'... pass Ellipsis'

'''


print("1，表示空函数的占位符的三种方法'... pass Ellipsis'".center(100, "-"))
#以下三个函数功能是一样的
def myfunc():
    ...

def myfunb():
    Ellipsis

def myfuna():
    pass


print("2，将列表中对象(字典只获取key且不打散)或元素(不支持数字)打撒。".center(100, "-"))
l = [[1, 2, 3], (9,5), {111:456}, "test",str(66), {"abc":('77','88')}]
flattened = [e for sublist in l for e in sublist]
print(flattened)  # [1, 2, 3, 9, 5, 111, 't', 'e', 's', 't', '6', '6', 'abc']



print("3，将列表中子列表元素进行降维拼接".center(100, "-"))
from functools import reduce
l = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(reduce(lambda x, y: x+y, l))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
#
#
# #todo 技巧6，展开的艺术之sum降维合并
# # 即对二维数组做sum操作，就能展开为一维数组。其实相当于 [] + [1, 2, 3] + [4, 5, 6] + [7, 8, 9]
# l = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# print(sum(l, []))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
# # 同理，对三位数组做sum操作，就能使其变为二维数组，此时再对二维数组做sum操作，就能展开为一维数组。
# l = [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]]
# print(sum(l, []))  # [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# print(sum(sum(l, []), []))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
#
#
# #todo 技巧7，异常处理中巧用else，即在 try ... except ... 中使用 else 编写未捕获到异常时的逻辑
#
# try:
#     t = 123
# except:
#     print("test")
# else:
#     print("未出错here")
# # 未出错here
#
#
# #todo 技巧8，迭代器切片slice获取区间项
# import itertools
# s = itertools.islice([1, 2, 3, 4, 5], 3, 5)  # <itertools.islice object at 0x7f70fab88138>
# for val in s:
#     print(val)
# # 4
# # 5
#



def function2(name, age):
    print("name: %s, age: %s" % (name, age))
    return 2

x = eval("function2")("Alice", 11)
print(x)
