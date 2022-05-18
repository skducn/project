# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2021-5-25
# Description: map(function,iterable) 函数，对某个序列以给定的函数格式作映射。
# https://www.cnblogs.com/lincappu/p/8179475.html
# python3中map()返回iterators类型
# ********************************************************************************************************************


# 当seq只有一个时，将函数func作用于这个seq的每个元素上，并得到一个新的seq
squares = map(lambda x: x ** 2, range(5))
print(list(squares))  # [0,1,4,9,16]
# 当seq多于一个时，map可以并行（注意是并行）地对每个seq执行
x = map(lambda s:s[0:1].upper()+s[1:].lower(), ['adam', 'LISA', 'barT'])
print(list(x))  # ['Adam', 'Lisa', 'Bart']



print("1，，将列表里的数字型字符串转换成int/float/str".center(100, "-"))
a = ['1', '2', '3', 444]
b = list(map(int, a))
print(b)  # [1, 2, 3, 444]


a = ['1', '2', '0.03', 444]
b = list(map(float, a))
print(b)  # [1.0, 2.0, 0.03, 444.0]

a = ['1', '2', '0.03', 444]
b = list(map(str, a))
print(b)  # ['1', '2', '0.03', '444']



print("2，对列表里的值求绝对值".center(100, "-"))
a = [-1, 2, -5]
b = list(map(abs, a))
print(b)  # [1, 2, 5]


print("3，map()返回iterators类型".center(100, "-"))
a = ['1', '2', '3']
b = map(int, a)
print(b)  # <map object at 0x000002C04D600EE0>
print(type(b))  # <class 'map'>


l=map(str, '5678')
list1 = []
for i in l:
    list1.append(i*2)
print(list(l))
print(list1)