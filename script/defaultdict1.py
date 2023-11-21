# coding: utf-8
# *******************************************************************
# Author     : John
# Date       : 2021-12-21
# Description: defaultdict
# collections.defaultdict类的介绍：
# defaultdict是Python内建dict类的一个子类，第一个参数为default_factory属性提供初始值，默认为None。
# 它覆盖一个方法并添加一个可写实例变量。它的其他功能与dict相同，但会为一个不存在的键提供默认值，从而避免KeyError异常。

# 键可以是任何不可变（immutable）数据类型（不可变数据类型：数字，字符串、元组）（也就是说key不能为列表和字典类型）

# 1, 当查询一个字典中不存的元素时，返回的不是keyError而是一个默认值。
# 语法：dict = defaultdict(factory_function) ,
# factory_function可以是int，list、set、str等等，作用是当key不存在时，返回的是工厂函数的默认值，比如list对应[ ]，str对应的是空字符串，set对应set( )，int对应0.

# https://blog.csdn.net/u014248127/article/details/79338543
# *******************************************************************

from collections import defaultdict

# dict1 = defaultdict(int)
# dict2 = defaultdict(list)
# dict3 = defaultdict(set)
# dict4 = defaultdict(str)
# print(dict1[0])  # 0
# print(dict2[0])  # []
# print(dict3[0])  # set()
# print(dict4[0])  #


def zero():
    return 10
dd = defaultdict(zero)
print(dd['bbb'])  # 10
print(dd['a'])  # 10
print(dd)  # defaultdict(<function zero at 0x00000186C1D2F040>, {'bbb': 10, 'a': 10})



# print("6.1 collections中defaultdict之字典的 value 是字典".center(100, "-"))
dict1 = defaultdict(dict)
dict1[5]["a"] = 125
dict1[5]["b"] = 1
print(dict1[5])  # {'a': 125, 'b': 1}
print(dict1)  # defaultdict(<类与实例 'dict'>, {5: {'a': 125, 'b': 1}})

# #
# # print("6.2 collections中defaultdict之字典的 value 是列表".center(100, "-"))
# list1 = defaultdict(list)
# list1[5].append(3)
# list1[5].append("45")
# print(list1[5])  # [3, '45']
# #
# # print("6.3 collections中defaultdict之字典的 value 是lambda".center(100, "-"))
# a = defaultdict(lambda: 10)
# print(a[3])  # 10
# print(a[6]+1)  # 11
# # print(a)  # defaultdict(<function <lambda> at 0x000001F2D17F0550>, {3: 10, 6: 10})
# #
# # print("6.4 collections中defaultdict之字典的 value 里又是字典".center(100, "-"))
# dict4 = defaultdict(lambda: defaultdict(dict))
# dict4[5]["a"] = dict(b=123, c=666)
# # print(dict4[5])  # defaultdict(<类与实例 'dict'>, {'a': '123'})
# print(dict4[5]['a'])  # {'b': 123, 'c': 666}
