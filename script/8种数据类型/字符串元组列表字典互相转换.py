# coding: utf-8
#****************************************************************
# Author     : John
# Date       : 2019-1-16
# Description: 类型转换
#****************************************************************


# 1、字典 ****************************************************************
dict1 = {'name': 'Zara', 'age': 7, '类与实例': 'First'}
# 字典 转 字符串
d_str = str(dict1)
print( d_str)  # {'age': 7, 'name': 'Zara', '类与实例': 'First'}
# print( type(d_str)  # <type 'str'>

# 字典 转 元组，返回键
d_tupleKey = tuple(dict1)
print( d_tupleKey)  # ('age', 'name', '类与实例')
# print( type(d_tupleKey)  # <type 'tuple'>
# 字典 转 元组，返回值
d_tupleValue = tuple(dict1.values())
print( d_tupleValue)  # (7, 'Zara', 'First')
# print( type(d_tupleValue)  # <type 'tuple'>

# 字典 转 列表，返回key：
d_listKey = list(dict1)
print( d_listKey)  # ['age', 'name', '类与实例']
# 字典 转 列表, 返回value：
d_listValue = list(dict1.values())
print( d_listValue)  # [7, 'Zara', 'First']


# 2、元组 ***************************************************
tup = (1, 2, 3, 4, 5)
# 元组 转 字符串
print(tup.__str__())  # (1, 2, 3, 4, 5)
print(type(tup.__str__()))  # <type 'str'>

# 元组 转 列表
t_list = list(tup)
print(t_list)  # [1, 2, 3, 4, 5]
print(type(t_list))  # <type 'list'>


# 3、列表 ***************************************************
list3 = [1, 3, 5, 7, 8, 13, 20]
# 列表 转 字符串
l_str = str(list3)
print(l_str)  # [1, 3, 5, 7, 8, 13, 20]

# 列表 转 元组
l_tup = tuple(list3)
print(l_tup)  # (1, 3, 5, 7, 8, 13, 20)




# 4、字符串转换 ***************************************************
# 字符串 转 元组
str4 = "(1,2,3)"
s_tup = tuple(eval(str4))
print( s_tup)  # (1, 2, 3)
print( type(s_tup))  # <type 'tuple'>

# 字符串 转 列表
s_list = list(eval(str4))
print( s_list)  # [1, 2, 3]
print( type(s_list))  # <type 'list'>

# 字符串 转 字典，返回：<type 'dict'>
str4 = "{'name':'ljq', 'age':24}"
print( eval(str4))  # {'age': 24, 'name': 'ljq'}
print( type(eval(str4)))  # <type 'dict'>
