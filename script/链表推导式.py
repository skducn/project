# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-18
# Description: 链表推导式
# 链表表达式在for语句前面，for后面就是对参数的限定。[XXX for yyy](必须要有方括号表示是链表），XXX表示链表，yyy限定XXX中参数。
# ********************************************************************************************************************


print("1，列表元素翻倍".center(100, "-"))
num = [1, 2, 3, 4, 5]
myvec = [x * 2 for x in num]
print(myvec)  # [2, 4, 6, 8, 10]


print("2，列表元素翻倍后，与原值组成子列表".center(100, "-"))
num = [1, 2, 3]
myvec = [[x, x * 2] for x in num]
print(myvec)  # [[1, 2], [2, 4], [3, 6]]


print("3，遍历列表，按条件修改列表值".center(100, "-"))
vec = [2, 4, 6]
print([3 * x for x in vec])  # [6, 12, 18]
print([3 * x for x in vec if x > 3])  # [12, 18]
print([3 * x for x in vec if x <= 2])  # []
print([[x, x ** 2] for x in vec])  # [[2, 4], [4, 16], [6, 36]]
print([(x, x ** 2) for x in vec])  # [(2, 4), (4, 16), (6, 36)]
vec = ["我的名字", "你的名字", "测试内容"]
print([x for x in vec if "名字" in x])  # ['我的名字', '你的名字']
print([x.replace("名字", "name") for x in vec if "名字" in x])  # ['我的name', '你的name']
print([x.replace("名字", "name") for x in vec])  # ['我的name', '你的name', '测试内容']


print("4，批量替换列表值".center(100, "-"))
abc = [['abc\n'], ['cde\n'], ['def\n']]
print([[x[i].replace("\n", "") for i in range(1)] for x in abc])  # [['abc'], ['cde'], ['def']]
abc = ['abc\n', 'cde\n', 'def\n']
print([x.replace("\n", "") for x in abc])  # ['abc', 'cde', 'def']
abc = ['a\tbc\n', 'cde\n', 'def\n']
print([x.replace("\n", "").replace("\t", "") for x in abc])  # ['abc', 'cde', 'def']


print("5，去掉列表中值前后空格".center(100, "-"))
mybag = [' glass', ' apple', ' green leaf ']
print([x.strip() for x in mybag])  # ['glass', 'apple', 'green leaf']


print("6，两个列所有值乘积（相加）后的列".center(100, "-"))
vec1 = [2, 4, 6]
vec2 = [4, 3, -9]
print([x * y for x in vec1 for y in vec2])  # [8, 6, -18, 16, 12, -36, 24, 18, -54]
print([x+y for x in vec1 for y in vec2])  # [6, 5, -7, 8, 7, -5, 10, 9, -3]
print([vec1[i]*vec2[i] for i in range(len(vec1))])  # [8, 12, -54]


print("7，在推导之外保留循环变量值".center(100, "-"))
x = 100
print([x ** 3 for x in range(5)])  # [0, 1, 8, 27, 64]
print(x)  # 100  //保留原变量值。


print("8，100以内的能够被3整除的正整数".center(100, "-"))
print([n for n in range(1,100) if n % 3 == 0])
# [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96, 99]


print("9，输出 1-9 的2次方值".center(100, "-"))
print([x ** 2 for x in range(1, 10)])  # # [1, 4, 9, l_s4, 25, 36, 49, 64, 81]


print("10，找出100以内的能够被3整除的正整数".center(100, "-"))
print([n for n in range(1, 100) if n % 3 == 0])  # [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96, 99]


print("11，range对象转列表".center(100, "-"))
print(list(range(1, 5)))  # <class 'list'> [1, 2, 3, 4]

