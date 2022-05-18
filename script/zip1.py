# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2022-5-18
# Description: zip()函数
# zip()函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表[]。
# ********************************************************************************************************************

colors = ['red', 'yellow', 'green', 'black']
fruits = ['apple', 'pineapple', 'grapes', 'cherry']
for item in zip(colors, fruits):
    print(item)
# ('red', 'apple')
# ('yellow', 'pineapple')
# ('green', 'grapes')
# ('black', 'cherry')


# 当我们使用zip()函数时，如果各个迭代器的元素个数不一致，则返回列表长度与最短的对象相同。
prices =[100, 50, 120]
for item in zip(colors, fruits, prices):
    print(item)
# ('red', 'apple', 100)
# ('yellow', 'pineapple', 50)
# ('green', 'grapes', 120)