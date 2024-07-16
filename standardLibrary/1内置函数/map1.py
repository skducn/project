# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2021-5-25
# Description: map(function,iterable) 函数，对某个序列以给定的函数格式作映射。
# https://www.cnblogs.com/lincappu/p/8179475.html
# python3中map()返回iterators类型
# map()是 Python 内置的高阶函数，它接收一个函数 f 和一个 list，并通过把函数 f 依次作用在 list 的每个元素上，得到一个新的 list 并返回。
# 注意：map()函数不改变原有的 list，而是返回一个新的 list。
# ********************************************************************************************************************


print("1，生成0-4的倍数".center(100, "-"))
l_1 = list(map(lambda x: x ** 2, range(5)))
print(l_1)  # [0,1,4,9,16]


print("2，将列表中每个元素的首字母大写，其余字母小写".center(100, "-"))
l_2 = list(map(lambda s:s[0:1].upper() + s[1:].lower(), ['adam', 'LISA', 'barT']))
print(l_2)  # ['Adam', 'Lisa', 'Bart']


print("3, 将列表里的数字型字符串转换成int/float/str".center(100, "-"))
print(list(map(int, ['1', '2', '3', 444])))  # [1, 2, 3, 444]
print(list(map(float, ['1', '2', '0.03', 444])))  # [1.0, 2.0, 0.03, 444.0]
print(list(map(str, ['1', '2', '0.03', 444])))  # ['1', '2', '0.03', '444']


print("4，对列表里的值求绝对值".center(100, "-"))
print(list(map(abs, [-1, 2, -5])))


print("5，将字符串打散成列表".center(100, "-"))
list1 = []
for i in map(str, '5678'):
    list1.append(i*2)
print(list(map(str, '5678')))  # ['5', '6', '7', '8']
print(list1)  # ['55', '66', '77', '88']


print("6，获取列表中偶数的平方".center(100, "-"))
filtered = filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5])  # 就是x除以2余数为0 ,代表能被2整除
# print(filtered)  # <filter object at 0x7f9aec478be0>
squared = list(map(lambda x: x**2, filtered))
print(squared)  # [4, 16]


# reduce求和
from functools import reduce
print("6，列表里元素求和".center(100, "-"))
squared = [1,2,3]
print(reduce(lambda acc, x: acc + x, squared, 0))


print("7，第一个列表是底，第二个列表是次方".center(100, "-"))
l2 = map(lambda x,y:x**y,[3,4,5],[1,2,2])
for i  in l2:
    print(i)
# 3，16，25

