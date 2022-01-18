# coding: utf-8
# *******************************************************************
# Author     : John
# Date       : 2021-1-27
# Description: 集合（set）是一个无序的不重复元素序列。
# 1，用大括号 { } 或 set() 函数创建集合
# 注意：创建一个空集合必须用 set() 而不能用 { }，因为 { } 只用来创建一个空字典。
# *******************************************************************

'''
1，集合去重
2，in判断元素是否在集合内
3，集合运算
4，集合推导式
5，创建一个空集合
6，add整体追加，update拆分追加
7，remove移除可报错, discard移除不报错
8，pop随机删除集合中的一个元素
9，统计元素个数
10，清空集合
11，列表\元组\字符串\字典 转集合
12，issubset子集与issuperset父集的关系
'''

basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}


print("1，集合去重".center(100, "-"))
print(basket)  # {'pear', 'orange', 'apple', 'banana'}
print({'apple', 'orange', 'apple', 'pear', 'orange', 'banana'})  # {'pear', 'orange', 'apple', 'banana'}


print("2，in判断元素是否在集合内".center(100, "-"))
if "banana" in basket:
    print(1)
else:
    print(0)


print("3，集合运算".center(100, "-"))
a = set('aabbccdd')
b = set('alacazam')
print(a)  # {'c', 'b', 'd', 'a'}  //打散去重
print(b)  # {'z', 'a', 'c', 'm', 'l'}
print(a - b)  # {'d', 'b'}    //在a中去掉与b中重复的元素
print(a | b)  # {'b', 'l', 'd', 'a', 'c', 'm', 'z'}    //a与b元素合并，并去重
print(a & b)  # {'c', 'a'}    //a和b交集元素
print(a ^ b)  # {'m', 'l', 'b', 'z', 'd'}    //a和b非交集元素


print("4，集合推导式".center(100, "-"))
a = {x for x in 'abracadabra' if x not in 'abc'}
print(a)  # {'d', 'r'}  // 遍历abracadabra中每个元素，如果不在abc中，则保留


# 注意：添加元素，不支持数字
print("5，创建一个空集合".center(100, "-"))
s1 = set()  # 创建一个空集合
print(s1)  # set()


print("6，add整体追加，update拆分追加".center(100, "-"))
s1.add("facebook")   # 整体追加
print(s1)  # {'facebook'}
s1.update("baidu")  # 拆分追加
print(s1)  # {'u', 'b', 'd', 'a', 'i', 'facebook'}
s1.update({444: "abc"})   # 只追加字典的key
print(s1)  # {'d', 'facebook', 'a', 'i', 'u', 'b', 444}
s1.update([1111, 400], [5555, 600])  # 追加列表中所有元素
print(s1)  # {'d', 'facebook', 'i', 600, 400, 5555, 'u', 1111, 'a', 'b', 444}
s1.update((1, 4, 5, 6))  # 追加元组中所有元素
print(s1)  # {1, 4, 'd', 5, 6, 'i', 600, 400, 5555, 'u', 1111, 'a', 'b', 444}


print("7，remove移除可报错, discard移除不报错".center(100, "-"))
s1.remove("facebook")
print(s1)  # {1, 4, 5, 6, 'a', 'i', 'u', 'b', 400, 5555, 1111, 600, 444, 'd'}
# s1.remove("facebook")  # 如果facebook元素不存在，执行后不报错，但打印输出时报错 print(s1)，提示KeyError: 'facebook'
s1.discard("facebook")  # 如果facebook元素不存在，执行与打印都不报错
print(s1)  # {'b', 'd', 1, 4, 5, 'u', 6, 400, 5555, 1111, 600, 'a', 444, 'i'}


print("8，pop随机删除集合中的一个元素".center(100, "-"))
s1.pop()
print(s1)  # {'a', 4, 5, 'u', 6, 'b', 'i', 400, 'd', 5555, 1111, 600, 444}
s1.pop()
print(s1)  # {4, 5, 'u', 6, 'b', 'i', 400, 'd', 5555, 1111, 600, 444}


print("9，统计元素个数".center(100, "-"))
print(len(s1))  # 12


print("10，清空集合".center(100, "-"))
s1.clear()
print(s1)  # set()


print("11，列表\元组\字符串\字典 转集合".center(100, "-"))
l_test2 = ['a', 'b', 'mpilgrim', True, False, 42]
print(set(l_test2))  # {False, True, 'mpilgrim', 42, 'a', 'b'}   # 列表转集合
l_test3 = (9, 6, 'baidu', True)
print(set(l_test3))  # {9, 'baidu', 6, True}  # 元组转集合
l_test4 = "123"
print(set(l_test4))  # {'1', '2', '3'}  # 字符串打散转集合
l_test5 = {"a": 111, "b": 222}
print(set(l_test5))  # {'b', 'a'}  # 字典key转集合


print("12，issubset子集与issuperset父集的关系".center(100, "-"))
s5 = {1, 2, 3}
s500 = {1, 2, 3, 4}
print(s5.issubset(s500))   # True   //判断s5是s500的子集
print(s500.issuperset(s5))  # True    //判断s500是s5的父集