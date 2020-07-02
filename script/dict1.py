# coding: utf-8
# *******************************************************************
# Author     : John
# Date       : 2019-1-29
# Description: 字典
# 1，dict 的键是唯一的，如果存在重复的键，则排列最后的一个键值对有效。
# 2，dict 值可以取任何数据类型，但键只能取不可变类型，如字符串，数字或元组。
# *******************************************************************
'''
字典内置函数，查看方法：dir(dict):
1、dict.clear()：清空字典内全部元素（字典未删除）
2、dict.copy()：返回一个字典的浅复制
3、dict.fromkeys()：创建一个新字典，以序列seq中元素做字典的键，val为字典全部键相应的初始值
4、dict.get(key, default=None)：返回指定键的值。假设值不在字典中返回default值
5、dict.items()：以列表返回可遍历的(键, 值) 元组数组
6、dict.keys()：以列表返回一个字典全部的键
7、dict.pop(key[, default])：如果key存在，返回key的值并删除key，否则key不存在，返回default值。
8、dict.popitem()	remove and return an arbitrary (key, value) pair
9、dict.setdefault(key, default=None)：和get()相似, 但假设键不存在，将会加入键并将值设为default
10、dict.update(dict2)：把字典dict2的键/值对更新到dict里
11、dict.values()：以列表返回字典中的全部值
dict.has_key(key)：假设键在字典dict里返回true，否则返回false (for py2.7)
dict.iteritems()	return an iterator over (key, value) pairs (for py2.7)
dict.iterkeys()	return an iterator over the mapping's keys (for py2.7)
dict.itervalues() return an iterator over the mapping's values (for py2.7)
其他：operator.eq(dict1,dict2)，operator.ne(dict1,dict2)，(for py3.x)比較两个字典元素，返回Ture或False  cmp(dict1, dict2) ，(for py2.7)

1，用dict函数新增字典时（key=value），key只能是字母、字母与数字组合且字母开头、中文
2，新增键值，前提先定义一个字典
3，setdefault(key)方法，如果key不存在则新增，默认值为None，否则忽略)
4，编辑值
5，删除键/删除字典
6，弹出值 (有value返回值）
7，清空字典（非删除）
8，获取字典的值
9，用get()函数获取原值或预设值
10，遍历字典的key
11，用itmes()遍历字典的key和value
12，遍历字典key/value
13，多个字典合并，update()方法，相同key则被覆盖
14，sorted()方法对字典进行排序，返回列表
15，字典拷贝
16，用fromkeys(seq，默认值)方法将元组（seq）转字典
17，判断字典key是否存在，区分大小写
18，字典转字符串、元组、列表
19，列表转字典
20，json模块实现字典与字符串互转换
'''


# ********************************************************************************************************************
# 合法的字典（一个合法的字典，键可以是字母，数字，元组，但不能是列表）
# dict1 = {'a': 'b', 'age': 7, 5:4, (12,):"123"}
# 不合法的字典
# dict1 = {[1,2,3]:'a'}


print("1，用dict函数新增字典时（key=value），key只能是字母、字母与数字组合且字母开头、中文".center(100, "-"))
dict1 = dict(a='1', b1=22, c=["a", 123], 中国={1: "aaa"}, ewer=(12,))
print(dict1)  # {'a': '1', 'b1': 22, 'c': ['a', 123], '中国': {1: 'aaa'}, 'ewer': (12,)}


print("2，新增键值，前提先定义一个字典".center(100, "-"))
dict2 = {}
dict2["abc"] = "watermelon"
dict2[100] = 88
dict2[(12,)] = "watermelon"
dict2[("姓名")] = "金浩"
dict2[("姓名")] = "金浩"
print(dict2)  # {'abc': 'watermelon', 100: 88, (12,): 'watermelon', '姓名': '金浩'}


print("3，setdefault(key)方法，如果key不存在则新增，默认值为None，否则忽略)".center(100, "-"))
dict3 = {}
dict3.setdefault("d")
print(dict3)  # {'d': None}
dict3["d"] = "apple"
dict3.setdefault("d", "default")  # 如果d已存在，则忽略此函数。
print(dict3)  # {'d': 'apple'}


print("4，编辑值".center(100, "-"))
dict4 = {"b" : "watermelen"}
dict4["b"] = "bananan"
print(dict4)  # {'b': 'bananan'}


print("5，删除键/删除字典".center(100, "-"))
del (dict4["b"])
print(dict4)  # {}
# del (dict4["b"])  # 报错，因为已经没有这个”b“
del dict4  # 删除字典
# del dict4  # 删除一个不存在的字典，报错，NameError: name 'dict4' is not defined


print("6，弹出值 (有value返回值）".center(100, "-"))
# 注意：这里pop(元素)
dict6 = {'a': 'b', 'age': 7, 5:4, (12,):"123"}
print(dict6.pop("age"))  # 7
print(dict6)  # {'a': 'b', 5: 4, (12,): '123'}
print(dict6.pop(5))  # 4
print(dict6)  # {'a': 'b', (12,): '123'}
# print(dict6.pop())  # 报错，pop必须要有一个存在的key


print("7，清空字典（非删除）".center(100, "-"))
dict6.clear()  # {}
print(dict6)


print("8，获取字典的值".center(100, "-"))
dict8 = {4: ("apple",), "b": {"123": "banana", "o": "orange"}, (2,"yoyo"): ["grape", "grapefruit"]}
print(dict8[4])  # ('apple',)
print(dict8[4][0])  # apple
print(dict8["b"])  # {'123': 'banana', 'o': 'orange'}
print(dict8["b"]["123"])  # banana
print(dict8[(2, "yoyo")])  # ['grape', 'grapefruit']
print(dict8[(2, "yoyo")][1])  # grapefruit


print("9，用get()函数获取原值或预设值".center(100, "-"))
dict9 = {"a": 1, "b": 2, "c": 3}
print(dict9.get("a", "11111"))  # 1   //如果键a存在, 则返回对应的value值。
print(dict9.get("zz", "没有找到"))  # 没有找到   //如果键值zz不存在, 则返回“没有找到”
# 实例，判断字典中某个key是否存在，存在返回原值，不存在返回预设值。
def searchKeyValue(key):
    print(dict2.get(key, "error,没有找到!"))  # error,没有找到!
searchKeyValue("test")


print("10，遍历字典的key".center(100, "-"))
# 注意：只能遍历key，不能遍历value
dict10 = {"a": "123", "b": "456", "c": "789"}
for k in dict10:
    # print(k, dict10[k])
    # print("dict10[%s] =" % k, dict10[k])
    print('dict10[{}] = {}'.format(k, dict10[k]))


print("11，用itmes()遍历字典的key和value".center(100, "-"))
dict11 = {"a": "123", "b": "456", "c": "789"}
for k, v in dict11.items():
    # print("dict11[%s] =" % k, v)
    print('dict11[{}] = {}'.format(k, v))


print("12，遍历字典key/value".center(100, "-"))
dict12 = {"a": "123", "b": "456", "c": "789"}
for k in dict12.keys():
    print(k)
# a
# b
# c
for v in dict12.values():
    print(v)
# 123
# 456
# 789


print("13，多个字典合并，update()方法，相同key则被覆盖".center(100, "-"))
dict131 = {"a": "123", "b": "456"}
dict132 = {"c": "789", "d": "john"}
dict133 = {"e": "eee", "a": "fff"}
dict131.update(dict132)  # 将dict134并入dict133
dict131.update(dict133)  # 将dict135并入dict133
print(dict131)  # {'a': 'fff', 'b': '456', 'c': '789', 'd': 'john', 'e': 'eee'}   //"a": "123" 被覆盖


print("14，sorted()方法对字典进行排序，返回列表".center(100, "-"))
dict14 = {"a" : "apple", "z" : "grape", "c" : "orange", "d" : "banana"}
# 对key排序
print(sorted(dict14.items(), key=lambda d: d[0])) # [('a', 'apple'), ('c', 'orange'), ('d', 'banana'), ('z', 'grape')]
# 对value排序
print(sorted(dict14.items(), key=lambda d: d[1])) # [('a', 'apple'), ('d', 'banana'), ('z', 'grape'), ('c', 'orange')]


print("15，字典拷贝".center(100, "-"))
# 浅拷贝(copy)， 拷贝父对象，引用子对象。{'父key': '父value', '父key': [子value, 子value]}
# 深拷贝(deepcopy)： 完全复制
import copy
dict15 = {"a": "apple", "b": [1, 2, 3]}
dict152 = dict15.copy()
dict153 = copy.deepcopy(dict15)
dict15['a'] = "father"
dict15['b'].remove(1)  # 移除了b中子对象1
print(dict15)  # {'a': 'father', 'b': [2, 3]}
print(dict152)  # {'a': 'apple', 'b': [2, 3]}
print(dict153)  # {'a': 'apple', 'b': [1, 2, 3]}


print("16，用fromkeys(seq，默认值)方法将元组（seq）转字典".center(100, "-"))
# 注意：如无默认值，则转换后字典值全部是None
dict16 = dict.fromkeys(('Google', 'baidu', 'Taobao'))
dict162 = dict.fromkeys((1, 2, 3), "test")
dict163 = dict.fromkeys((1, ), "test")  # {1: 'test'}
print(dict16)
print(dict162)  # {1: 'test', 2: 'test', 3: 'test'}
print(dict163)  # {'Google': None, 'baidu': None, 'Taobao': None}


print("17，判断字典key是否存在，区分大小写".center(100, "-"))
dict18 = {'Name': 'Zara', 'Age': 7}
# py3.X , 使用 __contains__()
print(dict18.__contains__('Name'))  # True
print(dict18.__contains__('NAme'))  # False
print(dict18.__contains__('sex'))  # False
# py2.7 , 使用 has_key()
# print( "Value : %s" %  dict.has_key('name')  )# Value : True
# print( "Value : %s" %  dict8.has_key('Sex') ) # Value : False


print("18，字典转字符串、元组、列表".center(100, "-"))
dict18 = {'name': 'Zara', 'age': 7, 'class': 'First'}
# 字典 转 字符串
print(type(str(dict18)), str(dict18))  # <type 'str'> {'age': 7, 'name': 'Zara', 'class': 'First'}
# 字典 转 元组keys (返回的元组内容是keys的集合)
print(type(tuple(dict18)), tuple(dict18))  # <class 'tuple'> ('name', 'age', 'class')
print(tuple(dict18)[1])  # age
# 字典 转 元组values (返回的元组内容是values的集合)
print(tuple(dict18.values()))  # ('Zara', 7, 'First')
print(tuple(dict18.values())[1])  # 7
# 字典 转 列表keys (返回的列表内容是keys的集合)
print(list(dict18))  # ['age', 'name', 'class']
# 字典 转 列表values (返回的列表内容是values的集合)
print(list(dict18.values()))  # ['Zara', 7, 'First']


print("19，列表转字典".center(100, "-"))
# 注意：列表格式必须符合字典keys和values格式，如只能是 数字、字符、元组
print(dict([(7, 'xidada'), ('age', 64), ((1, 2), 444)]))  # {7: 'xidada', 'age': 64, (1, 2): 444}


print("20，json模块实现字典与字符串互转换".center(100, "-"))
import json
dict20 = {'a': '192.168.1.1', 'b':'192.168.1.2'}
# 字典 转 字符串，json.dumps()
str20 = json.dumps(dict20)
print(str20)   # {"a": "192.168.1.1", "b": "192.168.1.2"} , 技巧，如果输出结果中是双引号，这一组就是字符串

# 字符串 转 字典，json.loads()
dict20 = json.loads(str20)
print(dict20)  # {'a': '192.168.1.1', 'b': '192.168.1.2'} # 技巧，如果输出结果中是单引号，这一组就是字典

