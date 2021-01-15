# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2021-1-8
# Description: itertools 无限迭代器，高效循环的迭代函数集合
# https://www.cnblogs.com/fengshuihuan/p/7105545.html
# https://docs.python.org/zh-cn/3.8/library/itertools.html
# pymotw 链接 http://pymotw.com/2/itertools/
# https://blog.csdn.net/weixin_41084236/article/details/81626968
# 迭代器模块：itertools
# 无限迭代器
# count()
# cycle()：复读机一号
# repeat()：复读机二号
# 终止于最短输入的迭代器
# accumulate()
# chain()
# chain.from_iterable()
# compress()
# dropwhile()
# filterfalse()
# groupby()
# islice()
# starmap()
# takewhile()
# tee()
# zip_longest()
# 组合生成器
# product()
# permutations()
# combinations()和combinations_with_replacement()
# ********************************************************************************************************************

import itertools


# # count() 无限迭代器
# for i in itertools.count():
#     print(i)

# # cycle() 复读机一号
# for i in itertools.cycle([2,3,4,5]):
#     print(i)

# # repeat()：复读机二号
# for i in itertools.repeat("你好"):
#     print(i)

# accumulate() 终止于最短输入的迭代器
for i in itertools.accumulate([1, 2, 3, 4], lambda x,y : x+y ):
    print(i)

# chain() 将所有输入拼接输出。
a='把你的心'
b=' 我的心'
c=' 串一串'
for i in itertools.chain(a,b,c):
    print(i)
d=['串一株幸运草',' 串一个同心圆']
for i in itertools.chain.from_iterable(d):
    print(i)


# compress() 返回 items 中对应 selectors 为True的元素,selectors作为滤镜套在了items上。
selec=[True,False,42,0,-42,'shuang']
items=['mole','xiangxiangji','tazhenmei','wodene','migang','shuangsile']
for i in itertools.compress(items,selec):
    print(i)
# mole
# tazhenmei
# migang
# shuangsile


# dropwhile() 从头开始，干掉不符合的元素，直到第一个正确元素。？
for i in itertools.dropwhile(lambda x: x<7, [1, 2, 3, 6, 7, 8, 2, 4, 5, 9]):
    print(i)
# 7
# 8
# 2
# 4
# 5
# 9

# filterfalse() 输出为错的要素：
for i in itertools.filterfalse(lambda x:x=='moyu',['moyu','jinye']):
    print(i)
# jinye

for i in itertools.filterfalse(lambda x: 1 if x >5 else 0, range(9)):
    print(i)
# 0
# 1
# 2
# 3
# 4
# 5

for i in itertools.filterfalse(lambda x: 1 if 'jin' in x else 0, ['moyu','jinye','moyinu','ajinye']):
    print(i)
# moyu
# moyinu


# groupby() 将iterable 相邻元素聚合成列表
for k,g in itertools.groupby('aaAAaBBBCCCCC'):
    print(k)
    print(list(g))
# a
# ['a', 'a']
# A
# ['A', 'A']
# a
# ['a']
# B
# ['B', 'B', 'B']
# C
# ['C', 'C', 'C', 'C', 'C']


# islice() 切片操作的迭代器版本
for i in itertools.islice('1234567890',0,None,2):
    print(i)
# 1
# 3
# 5
# 7
# 9

# starmap() map的迭代器版本
for i in itertools.starmap(lambda x, y: x + y, [(1, 2), (3, 4), (5, 6)]):
    print(i)
# 3
# 7
# 11

# takewhile() 与filterfalse()的判断条件相反。
for i in itertools.takewhile(lambda x:x=='moyu',['moyu','jinye']):
    print(i)
# moyu

# tee() 创建n个与iterable相同的独立迭代器。(?)
for i in itertools.tee([1,2,3,4,5,6]):
    for j in i:
        print(j)


# zip_longest() 用最长序列来zip，短序列填充fillvalue
for i in itertools.zip_longest('jinhao', 'yoyo', 'Fluttershy', 'App',fillvalue='*'):
    print(i)
# ('j', 'y', 'F', 'A')
# ('i', 'o', 'l', 'p')
# ('n', 'y', 'u', 'p')
# ('h', 'o', 't', '*')
# ('a', '*', 't', '*')
# ('o', '*', 'e', '*')
# ('*', '*', 'r', '*')
# ('*', '*', 's', '*')
# ('*', '*', 'h', '*')
# ('*', '*', 'y', '*')

for i in itertools.zip_longest('*', '**', '***', '**', '*', fillvalue=' '):
    print(i)
# ('*', '*', '*', '*', '*')
# (' ', '*', '*', '*', ' ')
# (' ', ' ', '*', ' ', ' ')


# product() 对*iterables进行笛卡尔积运算。
for x,y,z in itertools.product(['a','b','c'],['d','e','f'],['m','n']):
    print(x,y,z)



# permutations() 返回连续长度为r（默认为最大长度）的迭代对象。
# itertools.permutations(iterable[,r])
digi=[1,2,3]
for item in itertools.permutations(digi,2):
    print(item)
# (1, 2)
# (1, 3)
# (2, 1)
# (2, 3)
# (3, 1)
# (3, 2)

for item in itertools.permutations(range(3)):
    print(item)
# (0, 1, 2)
# (0, 2, 1)
# (1, 0, 2)
# (1, 2, 0)
# (2, 0, 1)
# (2, 1, 0)


# combinataions() , 与permutations类似，但由前到后返回不重复（索引组合）的迭代。
digi=[1,2,3]
for item in itertools.combinations(digi,2):
    print(item)
# (1, 2)
# (1, 3)
# (2, 3)

for item in itertools.combinations(range(3),2):
    print(item)
# (0, 1)
# (0, 2)
# (1, 2)

print("-------------")
# combinations_with_replacement() , 与combinataions类似，但是将自身索引也作为一次对象。
digi=[1,2,3]
for item in itertools.combinations_with_replacement(digi,2):
    print(item)
# (1, 1)
# (1, 2)
# (1, 3)
# (2, 2)
# (2, 3)
# (3, 3)