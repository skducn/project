# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-18
# Description: 列表推导式（list comprehension）
# 它可以用来快速生成列表，根据特定的条件或逻辑来生成满足要求的列表。提高代码效率和可读性。
# 语法：[expression for item in iterable if condition] , [表达式 for 变量 in 列表 if 条件]
# ********************************************************************************************************************
from functools import reduce
import sys

# todo 生成/更新/重组
print("生成/更新".center(100, "-"))
# 生成一个包括1到10平方的列表
print([x**2 for x in range(1, 11)])  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
# 生成一个包括1到10平方中偶数的列表（过滤）
print([x**2 for x in range(1, 11) if x**2 % 2 == 0])  # [4, 16, 36, 64, 100]
# 生成一个包含1到3平方的列表，且每个元素重复3次（多重循环）
print([x**2 for x in range(1, 4) for _ in range(3)])  # [1, 1, 1, 4, 4, 4, 9, 9, 9]
# 列表元素翻倍（更新）
print([x * 2 for x in [1, 2, 3, 4, 5]])  # [2, 4, 6, 8, 10]
# 列表元素翻倍后，与原值组成子列表（重组）
print([[x, x * 2] for x in [1, 2, 3, 4, 5]])  # [[1, 2], [2, 4], [3, 6], [4, 8], [5, 10]]



# todo 过滤
print("过滤".center(100, "-"))
# 只包含偶数的列表
print([x for x in [1,2,3,4,5,6] if x % 2 == 0])  # [2, 4, 6]
# 10以内的能被3整除的正整数
print([n for n in range(1, 10) if n % 3 == 0])  # [3, 6, 9]
# 只包含带'名字'值的列表
print([x for x in ["A名字", "B名字", "C内容"] if "名字" in x])  # ['A名字', 'B名字']
# 只包含带'名字'值的列表，且将'名字'改为'name'
print([x.replace("名字", "name") for x in ["A名字", "B名字", "C内容"] if "名字" in x])  # ['Aname', 'Bname']
# 去掉元素中\n
print([[x[i].replace("\n", "") for i in range(1)] for x in [['abc\n'], ['cde\n'], ['def\n']]])  # [['abc'], ['cde'], ['def']]
print([[x[i].replace("\n", "") for i in range(2)] for x in [['abc\n','555\n'], ['cde\n', '\nbaidu']]])  # [['abc', '555'], ['cde', 'baidu']]
print([x.replace("\n", "") for x in ['abc\n', 'cde\n', 'def\n']])  # ['abc', 'cde', 'def']
print([x.replace("\n", "").replace("\t", "") for x in ['a\tbc\n', 'cde\n', 'def\n']])  # ['abc', 'cde', 'def']
# 获取元素的index值
print([[2019, 2018, 2017, 2016].index(x) for x in [2019, 2018, 2017, 2016] if x == 2017])  # [2]
# 获取指定key的value
print([v for k, v in {'a': 1, 'b': 2, 'c': 3}.items() if k == 'c'])   #  [3]

# todo 字符串操作
print("字符串操作".center(100, "-"))
print([l.upper() for l in "testJinHao"])  # ['T', 'E', 'S', 'T', 'J', 'I', 'N', 'H', 'A', 'O']
print([l.upper() for l in ['testJinHao','aaBa']])  # ['TESTJINHAO', 'AABA']
print([l.lower() for l in ['testJinHao','aaBa']])  # ['testjinhao', 'aaba']
# 去掉列表中值前后空格
print([x.strip() for x in [' glass', ' apple', ' green leaf ']])  # ['glass', 'apple', 'green leaf']

# todo 列表扁平化（多重嵌套）
print("列表扁平化（多重嵌套）".center(100, "-"))
# 将列表元素扁平化之lambda
print(reduce(lambda x, y: x + y, [[1, 2, 3], [4, 5, 6], [7, 8, 9]]))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
# 将列表元素扁平化之列表推导式
print([i for sublist in [[1,2],[3,4],[5,6]] for i in sublist])  # [1, 2, 3, 4, 5, 6]
# 将列表元素扁平化之sum, 相当于 [] + [1, 2, 3] + [4, 5, 6] + [7, 8, 9]
l = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(sum(l, []))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
# # 同理，对三位数组做sum操作，就能使其变为二维数组，此时再对二维数组做sum操作，就能展开为一维数组。
l = [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]]
print(sum(l, []))  # [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(sum(sum(l, []), []))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
# 将列表中元素扁平化（字典只获取key，字符串不支持数字）
l = [[1, 2, 3], (9, 5), {111: 456}, "test", str(66), {"abc":('77','88')}]
print([e for sublist in l for e in sublist]) # [1, 2, 3, 9, 5, 111, 't', 'e', 's', 't', '6', '6', 'abc']

# 两列值乘积
print([x * y for x in [2, 4, 6] for y in [4, 3, -9]])  # [8, 6, -18, 16, 12, -36, 24, 18, -54]
# 两列值相加
print([x + y for x in [2, 4, 6] for y in [4, 3, -9]])  # [6, 5, -7, 8, 7, -5, 10, 9, -3]
print([[2, 4, 6][i] * [4, 3, -9][i] for i in range(3)])  # [8, 12, -54]



print("12，10阶乘".center(100, "-"))
print(reduce(lambda x, y: x * y, range(1, 11)))  # 3628800



print("13，将字典key与value互换".center(100, "-"))
print({v: k for k, v in {'a': 1, 'b': 2, 'c': 3}.items()})   # {1: 'a', 2: 'b', 3: 'c'}




