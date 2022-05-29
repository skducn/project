# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2017-12-19
# Description: 匿名函数 lambda：是指一类无需定义标识符（函数名）的函数或子程序。
# 用途：一般将它用在需要封装特殊的、非重用代码上，避免令代码充斥着大量单行函数。
# lambda 函数可接收多个参数 (包括可选参数) 并且返回单个表达式的值。
# 格式：lambda [arg1 [,arg2,...argn]]:expression 即 函数对象地址 = lambda [参数列表] : 表达式
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

# 要点：
# 1，lambda 函数不能包含命令；
# 2，包含的表达式不能超过一个；
# ********************************************************************************************************************


print("1，标准匿名函数格式".center(100, "-"))
p = lambda x, y: x+y
print(p(1, 4))   # 5
f1 = lambda x, y, z: (x+8) * y - z
print(f1(5, 6, 8))   # 70
print(f1)  # <function <lambda> at 0x000001F75FE0E160>  //即函数对象地址
print(type(f1))  # <class 'function'>   //lambda它是函数


print("2，非标匿名函数格式，即直接在匿名函数后接实参".center(100, "-"))
print((lambda x: x**2)(3))  # 9


print("3， 获取列表中偶数，且每个偶数加2".center(100, "-"))
import numpy as np
list1 = list(np.arange(1, 15, 3))
newlist1 = [(lambda x:x+2)(x) for x in list1 if x%2==0]
print(f"original list1 is: {list1}")  # [1, 4, 7, 10, 13]
print(newlist1)  # [6, 12]


#todo 将lambda函数作为参数传递给其他函数，如filter、map、sorted、reduce等Python内置函数使用
print("4，filter函数，过滤掉不符合条件的元素".center(100, "-"))
# filter(func，iterable) 过滤序列，过滤掉不符合条件的元素，返回一个迭代器对象，如果要转换为列表，可以使用 list() 来转换。
# 该函数接收两个参数，第一个为函数，第二个为序列，序列的每个元素作为参数传递给函数进行判，然后返回 True 或 False，最后将返回 True 的元素放到新列表中。
x = filter(lambda x: x % 3 == 0, [1, 2, 3, 4, 5, 6])
print(list(x))  # [3, 6]


print("5，map函数，将函数映射到列表的所有元素上".center(100, "-"))
# map(func,iterable)
# map()不改变原有的 list，而是返回一个新的 list。
# map返回的结果需要用list输出
# https://www.cnblogs.com/lincappu/p/8179475.html
squares = map(lambda x: x ** 2, range(5))
print(list(squares))  # [0,1,4,9,16]

# 由于list包含的元素可以是任何类型，因此，map() 不仅仅可以处理只包含数值的 list，事实上它可以处理包含任意类型的 list，只要传入的函数f可以处理这种数据类型。
# 将列表中名字改为首字母大写其余小写
x = map(lambda s:s[0:1].upper()+s[1:].lower(), ['adam', 'LISA', 'barT'])
print(list(x))  # ['Adam', 'Lisa', 'Bart']

# 当seq多于一个时，map可以并行地对每个list执行
l2 = map(lambda x,y : x**y, [1,2,3], [1,2,4])
for i in l2:
    print(i)
# 1
# 4
# 81


print("6，sorted函数，对所有可迭代的对象进行排序".center(100, "-"))
a=[('b',3),('a',2),('d',4),('c',1)]
# 对每个元素中第1项进行排序
print(sorted(a, key=lambda x: x[0]))  # [('a', 2), ('b', 3), ('c', 1), ('d', 4)]
# 对每个元素中第2项进行排序
print(sorted(a, key=lambda x: x[1]))  # [('c', 1), ('a', 2), ('b', 3), ('d', 4)]


print("7.1，reduce函数，参数序列中元素进行累加".center(100, "-"))
# 序列就是python中 tuple  list  dictionary string  以及其他可迭代物，别的编程语言可能有数组
# reduce(func,iterable[,initializer])
# reduce工作流 ：在迭代sequence(tuple ，list ，dictionary， string等可迭代物)的过程中，
# 首先把 前两个元素传给 函数参数，函数加工后，然后把得到的结果和第三个元素作为两个参数传给函数
# 参数， 函数加工后得到的结果又和第四个元素作为两个参数传给函数参数，依次类推。 如果传入了
# initial 值， 那么首先传的就不是 sequence 的第一个和第二个元素，而是 initial值和 第一个元
# 素。经过这样的累计计算之后合并序列到一个单一返回值
from functools import reduce
print(reduce(lambda a, b:'{},{}'.format(a, b), [1, 2, 3, 4, 5, "sasa", 7, 8, 9]))   # 1,2,3,4,5,sasa,7,8,9
print(reduce(lambda a, b: a + b, [1, 2, 3, 4, 5, 6, 7, 8, 9]))  # 45
print(reduce(lambda x, y: x * 10 + y, [1, 2, 3, 4, 5]))  # 12345


print("7.2，reduce函数，按性别分组".center(100, "-"))
# https://www.cnblogs.com/lonkiss/p/understanding-python-reduce-function.html
scientists =({'name':'jinhao', 'age':105, 'gender':'male'},
             {'name':'baba', 'age':76, 'gender':'male'},
             {'name':'mama', 'age':202, 'gender':'female'},
             {'name':'yoyo', 'age':84, 'gender':'female'})
def group_by_gender(accumulator , value):
    # print(accumulator)
    accumulator[value['gender']].append(value['name'])
    return accumulator
grouped = reduce(group_by_gender, scientists, {'male':[], 'female':[]})
print(grouped)  # {'male': ['jinhao', 'baba'], 'female': ['mama', 'yoyo']}


grouped = reduce(lambda acc, val: {**acc, **{val['gender']: acc[val['gender']] + [val['name']]}}, scientists, {'male':[], 'female':[]})
print(grouped)  # {'male': ['jinhao', 'baba'], 'female': ['mama', 'yoyo']}
# 分析：先 accumulator = {'male':[], 'female':[]} ，value= {'name':'jinhao', 'age':105, 'gender':'male'}
# 即 {'male':[], 'female':[]}['male'].append('jinhao') 得到结果 {'male': ['jinhao'], 'female': []} 然后进行遍历，
# 最后{'male': ['jinhao', 'baba'], 'female': ['mama', 'yoyo']}


print("7.3，reduce函数，按性别分组显示所有值".center(100, "-"))
import itertools
grouped = {item[0]:list(item[1]) for item in itertools.groupby(scientists, lambda x: x['gender'])}
print(grouped) # {'male': [{'name': 'jin', 'age': 105, 'gender': 'male'}, {'name': 'baba', 'age': 76, 'gender': 'male'}], 'female': [{'name': 'mama', 'age': 202, 'gender': 'female'}, {'name': 'yoyo', 'age': 84, 'gender': 'female'}]}


print("8，使用lambda选择菜单执行函数".center(100, "-"))
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


print("9，使用lambda输入运算符，执行相应操作".center(100, "-"))
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

