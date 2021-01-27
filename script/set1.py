# coding: utf-8
# *******************************************************************
# Author     : John
# Date       : 2021-1-27
# Description: 集合，集合（set）是一个无序的不重复元素序列。
# 1，使用大括号 { } 或者 set() 函数创建集合，注意：创建一个空集合必须用 set() 而不是 { }，因为 { } 是用来创建一个空字典。
# *******************************************************************


# 1， 集合去重
basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
print(basket)  # {'pear', 'orange', 'apple', 'banana'}


# 2，判断元素是否在集合内
if "banana" in basket:
    print(1)
else:
    print(0)


# 3，集合运算
a = set('aabbccdd')
b = set('alacazam')
print(a)  # {'c', 'b', 'd', 'a'}  # 打散去重
print(a - b)  # {'d', 'b'}    集合a中包含而集合b中不包含的元素
print(a | b)  # {'b', 'l', 'd', 'a', 'c', 'm', 'z'}    集合a或b中包含的所有元素
print(a & b)  # {'c', 'a'}    集合a和b中都包含了的元素
print(a ^ b)  # {'m', 'l', 'b', 'z', 'd'}    不同时包含于a和b的元素


# 4，集合推导式(Set comprehension)
a = {x for x in 'abracadabra' if x not in 'abc'}
print(a)  # {'d', 'r'}


# 5，基本操作之添加元素
# 注意：添加元素，且参数可以是列表，元组，字典，字符串等，但不支持数字
s_test = set()  # 创建一个空集合
s_test.add("facebook")   # 只能添加1个元素
print(s_test)  # {'facebook'}
print(type(s_test))  # <class 'set'>

s_test.update({1, 3, "facebook"})  # 可添加多个元素
print(s_test)  # {3, 1, 'facebook'}
s_test.update({4:"abc"})   #  {1, 3, 4, 'facebook'} 字典key方式添加多个元素
s_test.update([1, 4], [5, 6])  # {1, 3, 4, 5, 6, 'facebook'}   列表方式添加多个元素
# s_test.update((1, 4, 5, 6))  # {1, 3, 4, 5, 6, 'facebook'}  元组方式添加多个元素
print(s_test)  # {1, 3, 4, 5, 6, 'facebook'}


# 6，基本操作之移除元素
s_test.remove("facebook")
print(s_test)  # {1, 3, 4, 5, 6}
# s_test.remove("facebook")  # remove 方式移除，如果元素不存在，则会发生错误。
# print(s_test)  # 报错，因为 facebook 已不存在！
# s_test.discard("facebook")  # discard 方式移除，如果元素不存在，则不报错
# print(s_test)  # {1, 3, 4, 5, 6}

# 7，随机删除集合中的一个元素
# set 集合的 pop 方法会对集合进行无序的排列，然后将这个无序排列集合的左面第一个元素进行删除。
s_test.pop()
print(s_test)  # {3, 4, 5, 6}
s_test.pop()
print(s_test)  # {4, 5, 6}

# 9，计算集合元素个数
print(len(s_test))  # 3

# 8，清空集合
s_test.clear()
print(s_test)  # set()


