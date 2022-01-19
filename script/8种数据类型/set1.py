# coding: utf-8
# *******************************************************************
# Author     : John
# Date       : 2021-1-27
# Description: 集合（set）是一个无序的、不可重复的、不可变的元素序列，用{}表示。
# 集合的元素是无序的
# 集合的元素是不可重复的（重复的元素自动去重）
# 集合的元素是不可变的
# 集合的元素不支持索引、切片、嵌套
# *******************************************************************

'''
1，创建集合 set()
2，整体添加add(), 拆分归并update()
3, 删除可报错remove(), 删除不报错discard()，随机删除pop()
4，清空clear()
5，集合的基本运算
    5.1,in：判断元素是否存在于集合中，not in 判断元素不在几何中"
    5.2，-：集合的差集，等价于x.difference(y)
    5.3，|：集合的并集，等价于x.union(y)
    5.4，&：集合的交集，等价于x.intersection(y)
    5.5，^：集合的异或"
    5.6，>：集合的超集，等价于x.isuperset(z)
    5.7，<：集合的子集，等价于z.issubset(x)
6，集合推导式
7，列表\元组\字符串\字典 转集合
8，统计元素个数

'''



print("1，创建集合".center(100, "-"))
print(set())  # set()  //注意：创建一个空集合只能用 set() 而不能用 {}，因为 {} 表示用来创建一个空字典。
print(set([1, 2, 3]))  # {1, 2, 3}
print(set('abc'))  # {'b', 'a', 'c'}
print({6, 7, 8})  # {8, 6, 7}


print("2，整体添加add(), 拆分归并update()".center(100, "-"))
s2 = set()
s2.add("facebook")   # 整体追加
print(s2)  # {'facebook'}
s2.update("123")  # 拆分追加
print(s2)  # {'u', 'b', 'd', 'a', 'i', 'facebook'}
s2.update({4: "abc"})   # 只追加字典的key
print(s2)  # {'d', 'facebook', 'a', 'i', 'u', 'b', 444}
s2.update([5, 6], [7, 8])  # 追加列表中所有元素
print(s2)  # {'d', 'facebook', 'i', 600, 400, 5555, 'u', 1111, 'a', 'b', 444}
s2.update((9, 10))  # 追加元组中所有元素
print(s2)  # {1, 4, 'd', 5, 6, 'i', 600, 400, 5555, 'u', 1111, 'a', 'b', 444}


print("3, 删除可报错remove(), 删除不报错discard()，随机删除pop()".center(100, "-"))
s2.remove("facebook")
print(s2)  # {1, 4, 5, 6, 'a', 'i', 'u', 'b', 400, 5555, 1111, 600, 444, 'd'}
# s2.remove("facebook")  # 如果facebook元素不存在，执行后不报错，但打印输出时报错 print(s1)，提示KeyError: 'facebook'
s2.discard("facebook")  # 如果facebook元素不存在，执行与打印都不报错
print(s2)  # {'b', 'd', 1, 4, 5, 'u', 6, 400, 5555, 1111, 600, 'a', 444, 'i'}
s2.pop()
print(s2)  # {'a', 4, 5, 'u', 6, 'b', 'i', 400, 'd', 5555, 1111, 600, 444}


print("4，清空clear()".center(100, "-"))
s2.clear()
print(s2)  # set()


print("5，集合的基本运算".center(100, "-"))
x = set('1234')
y = set('2345')
z = set('12')
print(x)  # {'4', '2', '3', '1'}
print(y)  # {'4', '2', '5', '3'}
print("5.1，in：判断元素是否存在于集合中，not in 判断元素不在几何中".center(100, "-"))
print('1' in x)  # True
print('a' in x)  # False
print("5.2，-：集合的差集，等价于x.difference(y)".center(100, "-"))
print(x - y)  # {'1'}   //在x中去掉与y中重复的元素
print(x.difference(y))
print("5.3，|：集合的并集，等价于x.union(y)".center(100, "-"))
print(x | y)  # {'2', '4', '5', '3', '1'}   //x与y元素合并，并去重
print(x.union(y))
print("5.4，&：集合的交集，等价于x.intersection(y)".center(100, "-"))
print(x & y)  # {'4', '2', '3'}
print(x.intersection(y))
print("5.5，^：集合的异或".center(100, "-"))
print(x ^ y)  # {'5', '1'}    //x和y非交集元素
print("5.6，>：集合的超集，等价于x.isuperset(z)".center(100, "-"))
print(x > z)  # True
print(x.issuperset(z))  # True    //判断x是否包含z
print("5.7，<：集合的子集，等价于z.issubset(x)".center(100, "-"))
print(z < x)  # True
print(z.issubset(x))   # True   //判断z是否在y中


print("6，集合推导式".center(100, "-"))
a = {x for x in 'abracadabra' if x not in 'abc'}
print(a)  # {'d', 'r'}  // 遍历abracadabra中每个元素，如果不在abc中，则保留


print("7，列表\元组\字符串\字典 转集合".center(100, "-"))
l7 = ['a', 1, False, True]
print(set(l7))  # {'a', 1}
t7 = ('a', 1, True, False)
print(set(t7))  # {False, 1, 'a'}
str7 = "123"
print(set(str7))  # {'3', '1', '2'}
d7 = {"a": 111, "b": 222}
print(set(d7))  # {'b', 'a'}


print("8，统计元素个数".center(100, "-"))
s5 = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
print(len(s5))  # 4

