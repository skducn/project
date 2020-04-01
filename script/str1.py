# coding: utf-8
# *******************************************************************
# Author     : John
# Date       : 2019-1-29
# Description: 字符串使用方法 common - str1.py
# *******************************************************************
'''
字符串内置函数 ，查看方法：dir('')
capitalize
casefold
center
count
encode
endswith
expandtabs
find
format
format_map
index
isalnum
isalpha
isascii
isdecimal
isdigit
isidentifier
islower
isnumeric
isprintable
isspace
istitle
isupper
join
ljust
lower
lstrip
maketrans
partition
replace
rfind
rindex
rjust
rpartition
rsplit
rstrip
split
splitlines
startswith
strip
swapcase
title
translate
upper
zfill
'''

# 1，字符串转换

# 字符串 转 元组
print(type(tuple(eval("1,2,3"))),tuple(eval("1,2,3"))) # <class 'tuple'> (1, 2, 3)

# 字符串 转 列表
print(type(list(eval("1,2,3"))),list(eval("1,2,3")))  # <class 'list'> [1, 2, 3]

# 字符串 转 字典，返回：<type 'dict'>
print(type(eval("{'a':'123', 'b':456}")),dict(eval("{'a':'123', 'b':456}")))  # <class 'dict'> {'a': '123', 'b': 456}

# 元组 转 字符串
tup = (1, 2, 3, 4, 5)
print(type(tup.__str__()),tup.__str__())  # <class 'str'> (1, 2, 3, 4, 5)

# 列表 转 字符串
list1 = [1, 3, 5, 7, 8, 13, 20]
print(type(str(list1)),str(list1)) # <class 'str'> [1, 3, 5, 7, 8, 13, 20]

# 字典 转 字符串
dict1 = {'name': 'Zara', 'age': 7, 'class': 'First'}
print(type(str(dict1)), str(dict1))  # <class 'str'> {'name': 'Zara', 'age': 7, 'class': 'First'}

# json实现 字典 与 字符串 互转换
dict7 = {'a':'192.168.1.1','b':'192.168.1.2'}
import json
# 字典 转 字符串，json.dumps()
str7 = json.dumps(dict7)
print(type(str7)) # <class 'str'>
print(str7)   # {"a": "192.168.1.1", "b": "192.168.1.2"} , 技巧，如果输出结果中是双引号，这一组就是字符串
# 字符串 转 字典，json.loads()
dict7 = json.loads(str7)
print(type(dict7)) # <class 'dict'>
print(dict7)  # {'a': '192.168.1.1', 'b': '192.168.1.2'} # 技巧，如果输出结果中是单引号，这一组就是字典


# 2，字符串转换大小写
s = 'hEllo pYthon'
# 全部大写
print(s.upper())  # HELLO PYTHON

# 全部小写
print(s.lower())  # hello python

# 首字母大写，其余小写
print(s.capitalize()) # Hello python

# 所有单词首字母大写，其余小写
print(s.title()) # Hello Python


# 3，字符串判断大小写
# 如果对空字符串使用isupper()，islower()，istitle()，返回的结果都为 False。
s = ''
print(s.isupper()) # False
print(s.islower()) # False
print(s.istitle()) # False
ss1 = 'ABC'
ss2 = 'abc'
ss3 = 'Python Is Good'
print(ss1.isupper()) # True , 判断全部是大写吗？
print(ss2.islower()) # True ，判断全部是小写吗？
print(ss3.istitle()) # True ，判断所有单词首字母是大写吗？
# 注意：没有提供 iscapitalize()方法
