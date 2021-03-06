# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2017-12-19
# Description: 匿名函数 lambda：是指一类无需定义标识符（函数名）的函数或子程序。
# lambda 函数可接收多个参数 (包括可选参数) 并且返回单个表达式的值。
# 要点：
# 1，lambda 函数不能包含命令；
# 2，包含的表达式不能超过一个；
# 格式： 函数对象地址 = lambda 参数列表 : 表达式 ， lambda返回值是一个函数的地址，也就是函数对象。
# 用途：一般将它用在需要封装特殊的、非重用代码上，避免令代码充斥着大量单行函数。

# 参数列表如：
# a,b
# a=1,b=2
# *args
# **kwargs
# a,b=1,*args
# 空
# ....

# 表达式如：
# 1
# None
# a+b
# sum(a)
# 1 if a >10 else 0
# ......
# ********************************************************************************************************************


lambda x:y: x+y


def test(x,y):
    ee
    exit(e
         e
    e
    exit())
    return x+y



# 1，标准匿名函数格式
p = lambda x, y: x+y
p(1, 4)     # 注意：这样是可以执行的，不会报错，只是没有print的话不会输出结果。
print(p(1, 4))   # 5
a = lambda x, y, z: (x+8) * y - z
print(a(5, 6, 8))   # 70
print(a)  # <function <lambda> at 0x000001F75FE0E160>
print(type(a))  # <class 'function'>  lambda它是函数


# 2，非标准函数写法，直接在匿名函数后接实参
print((lambda x: x**2)(3))  # 9



# 3，将lambda函数作为参数传递给其他函数，如filter、map、sorted、reduce等Python内置函数使用
# filter() 过滤序列，过滤掉不符合条件的元素，返回一个迭代器对象，如果要转换为列表，可以使用 list() 来转换。
# 该函数接收两个参数，第一个为函数，第二个为序列，序列的每个元素作为参数传递给函数进行判，然后返回 True 或 False，最后将返回 True 的元素放到新列表中。
x = filter(lambda x: x % 3 == 0, [1, 2, 3, 4, 5, 6])
print(list(x))  # [3, 6]
print(tuple(x))
print(set(x))


# https://www.cnblogs.com/lincappu/p/8179475.html
# map() 对函数做序列做映射
# 当seq只有一个时，将函数func作用于这个seq的每个元素上，并得到一个新的seq
squares = map(lambda x: x ** 2, range(5))
print(list(squares))  # [0,1,4,9,16]
# 当seq多于一个时，map可以并行（注意是并行）地对每个seq执行
x = map(lambda s:s[0:1].upper()+s[1:].lower(), ['adam', 'LISA', 'barT'])
print(list(x))  # ['Adam', 'Lisa', 'Bart']

# sorted() 对所有可迭代的对象进行排序
a=[('b',3),('a',2),('d',4),('c',1)]
print(sorted(a, key=lambda x: x[0]))  # [('a', 2), ('b', 3), ('c', 1), ('d', 4)]
print(sorted(a, key=lambda x: x[1]))  # [('c', 1), ('a', 2), ('b', 3), ('d', 4)]

# reduce() 对参数序列中元素进行累积。
from functools import reduce
print(reduce(lambda a,b:'{},{}'.format(a,b),[1,2,3,4,5,"sasa",7,8,9]))   # 1,2,3,4,5,sasa,7,8,9
print(reduce(lambda a, b: a + b, [1, 2, 3, 4, 5, 6, 7, 8, 9]))  # 45
print(reduce(lambda x, y: x * 10 + y, [1, 2, 3, 4, 5]))  # 12345



# reduce() 按性别分组
# https://www.cnblogs.com/lonkiss/p/understanding-python-reduce-function.html
scientists =({'name':'jinhao', 'age':105, 'gender':'male'},
             {'name':'baba', 'age':76, 'gender':'male'},
             {'name':'mama', 'age':202, 'gender':'female'},
             {'name':'yoyo', 'age':84, 'gender':'female'})
def group_by_gender(accumulator , value):
    accumulator[value['gender']].append(value['name'])
    return accumulator
grouped = reduce(group_by_gender, scientists, {'male':[], 'female':[]})
print(grouped)  # {'male': ['jinhao', 'baba'], 'female': ['mama', 'yoyo']}

import itertools
scientists =({'name':'jin', 'age':105, 'gender':'male'},
             {'name':'baba', 'age':76, 'gender':'male'},
             {'name':'mama', 'age':202, 'gender':'female'},
             {'name':'yoyo', 'age':84, 'gender':'female'})
grouped = {item[0]:list(item[1])
           for item in itertools.groupby(scientists, lambda x: x['gender'])}
print(grouped) # {'male': [{'name': 'jin', 'age': 105, 'gender': 'male'}, {'name': 'baba', 'age': 76, 'gender': 'male'}], 'female': [{'name': 'mama', 'age': 202, 'gender': 'female'}, {'name': 'yoyo', 'age': 84, 'gender': 'female'}]}

scientists =({'name':'Alan Turing', 'age':105, 'gender':'male'},
             {'name':'Dennis Ritchie', 'age':76, 'gender':'male'},
             {'name':'Ada Lovelace', 'age':202, 'gender':'female'},
             {'name':'Frances E. Allen', 'age':84, 'gender':'female'})
grouped = reduce(lambda acc, val: {**acc, **{val['gender']: acc[val['gender']]+ [val['name']]}}, scientists, {'male':[], 'female':[]})
print(grouped)


# 4，实例选择菜单执行函数
# msgCtrl = "1 : pause\n2 : stop\n3 : restart\nother to quit\n"
# ctrlMap = {
#     '1': lambda: doPause(),
#     '2': lambda: doStop(),
#     '3': lambda: doRestart()}
# def doPause():
#     print('do pause')
# def doStop():
#     print('do stop')
# def doRestart():
#     print('do restart')
#
# if __name__ == '__main__':
#     print(msgCtrl)
#     cmdCtrl = input('Input : ')
#     if cmdCtrl  in ctrlMap:
#         ctrlMap[cmdCtrl]()
#     print(ctrlMap["1"])  # <function <lambda> at 0x00000270D88EF040>
#     ctrlMap['3']()  # do restart



# # 5，输入运算符，执行相应操作
# '''
# 输入1，计算10+2，返回12
# 输入2，计算10-2，返回8
# 输入3，计算10*2，返回20
# 输入其他数字，退出程序，否则循环提示输入信息
# '''
#
# tips = "1 : +\n2 : -\n3 : *\nother to quit\n"
# d1 = {
#     '1': lambda x, y: x + y,
#     '2': lambda x, y: x - y,
#     '3': lambda x, y: x * y}
#
# if __name__ == '__main__':
#     while True:
#         print(tips)
#         inputInfo = input('Input : ')
#         if inputInfo not in d1:
#             break
#         print(d1[inputInfo](10, 2), "\n")

