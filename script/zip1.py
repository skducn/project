# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2022-5-18
# Description: zip函数是Python的内置函数
# zip(*iters)函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表[]。
# 参数必须是可迭代对象；
# 迭代多个序列时，当其中一个序列迭代完毕，迭代过程终止
# 返回一个zip可迭代序列对象，如 <zip object at 0x00000212BDAD2840>；
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