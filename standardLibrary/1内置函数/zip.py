# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2022-5-18
# Description: zip(*iterables)
# 定义：创建一个聚合了来自每个可迭代对象中的元素的迭代器。
# 返回一个元组的迭代器，其中的第 i 个元组包含来自每个参数序列或可迭代对象的第 i 个元素。
# 当所输入可迭代对象中最短的一个被耗尽时，迭代器将停止迭代。
# 当只有一个可迭代对象参数时，它将返回一个单元组的迭代器。 不带参数时，它将返回一个空迭代器。

# 标准库：https://docs.python.org/zh-cn/3.7/library/functions.html#zip
# ********************************************************************************************************************

colors = ['red', 'yellow', 'green', 'black']
fruits = ('apple', 'pineapple', 'grapes', 'cherry')
prices = [100, 50, 120]


print("1，zip返回一个可迭代序列对象".center(100, "-"))
print(zip(colors, fruits))  # <zip object at 0x00000212BDAD2840>


print("2，将两个迭代序列中相同位置值组成一个元组".center(100, "-"))
for item in zip(colors, fruits):
    print(item)
# ('red', 'apple')
# ('yellow', 'pineapple')
# ('green', 'grapes')
# ('black', 'cherry')


for item in zip('ABCD', 'xy'):
    print(item)
# ('A', 'x')
# ('B', 'y')

print("3，将两个迭代序列中相同位置值组成一个元组，当其中一个序列迭代完毕，迭代过程终止".center(100, "-"))
for item in zip(colors, fruits, prices):
    print(item)
# ('red', 'apple', 100)
# ('yellow', 'pineapple', 50)
# ('green', 'grapes', 120)


print("4，将两个迭代序列合并成字典".center(100, "-"))
dict1 = {}
for k, v in zip(colors, fruits):
    dict1[k] = v
print(dict1)  # {'red': 'apple', 'yellow': 'pineapple', 'green': 'grapes', 'black': 'cherry'}


print("5，将两个列表转两个元组".center(100, "-"))
x = [1, 2, 3]
y = [4, 5, 6]
x, y = zip(*zip(x,y))
print(x, y)  # (1, 2, 3) (4, 5, 6)


print("6，将两个迭代序列中相同位置值组成一个元组，且每个元组重复n次".center(100, "-"))
for item in zip(*(x, y)*4):
    print(item)
# (1, 4, 1, 4, 1, 4, 1, 4)
# (2, 5, 2, 5, 2, 5, 2, 5)
# (3, 6, 3, 6, 3, 6, 3, 6)




