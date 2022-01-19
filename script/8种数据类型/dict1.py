# coding: utf-8
# *******************************************************************
# Author     : John
# Date       : 2019-1-29
# Description: 字典（dict）是一个无序的、不可重复的、可变元的素序列，用{}表。
# 字典的键是无序的，所以无法通过偏移来访问元素
# 字典的键是不可重复，如果存在重复的键，则排列最右（最后的）一个键值对有效。
# 字典的元素是可变的
# 字典的键只能取 字符串、数字、元组、布尔型及None。
# 字典的值可以取任何数据类型
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

1，创建字典用dict()时，key只能是字母、中文开头
2，新增键值
3，新增默认键 setdefault(key)，如果key不存在则新增，默认值为None，否则忽略)
4，删除键/删除字典 del 字典
5，返回值 pop(key)
6，清空字典.clear()

7，获取字典的值
8，获取原值或设预设值 get()

9，遍历字典的key
10，用itmes()遍历字典的key和value
11，遍历字典key和value，用keys()和values()

12，字典合并update()，相同key则被覆盖
13，字典排序sorted()，返回列表
14，字典拷贝，浅拷贝copy()，深拷贝(deepcopy)
15，判断字典key是否存在，区分大小写 __contains__()

todo: 转换
16.1，元组转字典fromkeys(键,值)
16.2.1，列表转字典 dict()
16.2.2，两列表转字典 dict(zip(list1,list2))
16.3，字符串转字典 json()
16.4，字典转字符串、元组、列表
'''



print("1，创建字典用dict()时，key只能是字母、中文开头".center(100, "-"))
print(dict(a='1', b1=22, 中国={1: "aaa"})) # {'a': '1', 'b1': 22, '中国': {1: 'aaa'}}


print("2，新增键值，前提先定义一个字典".center(100, "-"))
dict2 = {}
dict2["abc"] = "watermelon"
dict2[100] = 88
dict2[(12,)] = "watermelon"
dict2[("姓名")] = "金浩"
dict2[("姓名")] = "武则天"
dict2[(True)] = "12"
dict2[(None)] = "44"
print(dict2)  # {'abc': 'watermelon', 100: 88, (12,): 'watermelon', '姓名': '武则天', True: '12', None: '44'}


print("3，新增默认键 setdefault(key)，如果key不存在则新增，默认值为None，否则忽略)".center(100, "-"))
dict3 = {}
dict3.setdefault("d")
print(dict3)  # {'d': None}
dict3["d"] = "apple"
dict3.setdefault("d", "default")  # 如果d已存在，则忽略此函数。
dict3.setdefault("e", "bananan")  # 如果e不存在，则新增键值对。
dict3.setdefault("d")
print(dict3)  # {'d': 'apple', 'e': 'bananan'}


print("4，删除键/删除字典".center(100, "-"))
del (dict3["d"])
print(dict3)  # {'e': 'bananan'}
# del (dict3["d"])  # 报错，因为已经没有这个”b“
del dict3  # 删除字典
# del dict3  # 报错，上一步已删除dict3,再次删除一个不存在的字典是不对的，NameError: name 'dict3' is not defined


print("5，返回值 pop(key)".center(100, "-"))
dict6 = {'a': 'b', 'age': 7, 5:4, (12,):"123"}
print(dict6.pop("age"))  # 7
print(dict6)  # {'a': 'b', 5: 4, (12,): '123'}
print(dict6.pop(5))  # 4
print(dict6)  # {'a': 'b', (12,): '123'}
# print(dict6.pop())  # 报错，pop必须要有一个存在的key


print("6，清空字典（非删除）".center(100, "-"))
dict6.clear()
print(dict6)  # {}


print("7，获取字典的值".center(100, "-"))
dict8 = {4: ("apple",), "b": {"123": "banana", "o": "orange"}, (2,"yoyo"): ["grape", "grapefruit"]}
print(dict8[4])  # ('apple',)
print(dict8[4][0])  # apple
print(dict8["b"])  # {'123': 'banana', 'o': 'orange'}
print(dict8["b"]["123"])  # banana
print(dict8[(2, "yoyo")])  # ['grape', 'grapefruit']
print(dict8[(2, "yoyo")][1])  # grapefruit


print("8，获取原值或设预设值 get()".center(100, "-"))
dict9 = {"a": 1, "b": 2, "c": 3}
print(dict9.get("a", "11111"))  # 1   //如果键a存在, 则返回对应的value值。
print(dict9.get("zz", "没有找到"))  # 没有找到   //如果键值zz不存在, 则返回“没有找到”


print("9，遍历字典key".center(100, "-"))
# 注意：只能遍历key，不能遍历value
dict10 = {"a": "123", "b": "456", "c": "789"}
for k in dict10:
    # print("dict10[%s] =" % k, dict10[k])
    print('dict10[{}] = {}'.format(k, dict10[k]))


print("10，遍历字典key和value 用itmes()".center(100, "-"))
dict11 = {"a": "123", "b": "456", "c": "789"}
for k, v in dict11.items():
    print('dict11[{}] = {}'.format(k, v))


print("11，遍历字典key和value，用keys()和values()".center(100, "-"))
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


print("12，字典合并update()，相同key则被覆盖".center(100, "-"))
dictA = {"a": "123", "b": "456"}
dictB = {"c": "789", "d": "john"}
dictC = {"e": "eee", "a": "fff"}
dictA.update(dictB)  # 合并到dictA
print(dictA)
dictA.update(dictC)
print(dictA)  # {'a': 'fff', 'b': '456', 'c': '789', 'd': 'john', 'e': 'eee'}  相同的a被覆盖后者覆盖


print("13，字典排序sorted()，返回列表".center(100, "-"))
dict13 = {"a" : "apple", "z" : "grape", "c" : "orange", "d" : "banana"}
# 对key排序
print(sorted(dict13.items(), key=lambda d: d[0])) # [('a', 'apple'), ('c', 'orange'), ('d', 'banana'), ('z', 'grape')]
# 对value排序
print(sorted(dict13.items(), key=lambda d: d[1])) # [('a', 'apple'), ('d', 'banana'), ('z', 'grape'), ('c', 'orange')]


print("14，字典拷贝，浅拷贝copy()，深拷贝(deepcopy)".center(100, "-"))
# 浅拷贝(copy)， 拷贝父对象，引用子对象。{'父key': '父value', '父key': [子value, 子value]}
import copy
dict14 = {"a": "apple", "b": [1, 2, 3]}
dictA = dict14.copy()
# 深拷贝(deepcopy)： 完全复制
dictB = copy.deepcopy(dict14)
# 修改原数据
dict14['a'] = "father"
dict14['b'].remove(1)  # 移除了b中子对象1
print(dict14)  # {'a': 'father', 'b': [2, 3]}
print(dictA)  # {'a': 'apple', 'b': [2, 3]}
print(dictB)  # {'a': 'apple', 'b': [1, 2, 3]}


print("15，判断字典key是否存在，区分大小写 __contains__()".center(100, "-"))
dict15 = {'Name': 'Zara', 'Age': 7}
# py3.X , 使用 __contains__()
print(dict15.__contains__('Name'))  # True
print(dict15.__contains__('NAme'))  # False
print(dict15.__contains__('sex'))  # False
# py2.7 , 使用 has_key()
# print( "Value : %s" %  dict.has_key('name')  )# Value : True
# print( "Value : %s" %  dict8.has_key('Sex') ) # Value : False



print("16.1，元组转字典fromkeys(键,值)".center(100, "-"))
# 注意：如无值，则转换后字典值默认是None
dict16 = dict.fromkeys(('Google', 'baidu', 'Taobao'))
dict162 = dict.fromkeys((1, 2, 3), "test")
dict163 = dict.fromkeys((1, ), "test")  # {1: 'test'}
print(dict16)
print(dict162)  # {1: 'test', 2: 'test', 3: 'test'}
print(dict163)  # {'Google': None, 'baidu': None, 'Taobao': None}
d = {}.fromkeys({'1', '2'}, '000000')  # 生成1个新的字典
print(d)  # {'1': '000000', '2': '000000'}


print("16.2.1，列表转字典 dict()".center(100, "-"))
# 注意：列表格式必须符合字典keys和values格式，如key只能是 数字、字符、元组
print(dict([(7, 'xidada'), ('age', 64), ((1, 2), 444)]))  # {7: 'xidada', 'age': 64, (1, 2): 444}


print("16.2.2，两列表转字典 dict(zip(list1,list2))".center(100, "-"))
key = ['root', 'westos']
value = ['111', '222']
# print(zip(key, value))  # <zip object at 0x0000024EDE418640>
# print(list(zip(key, value)))  # [('root', '111'), ('westos', '222')]
print(dict(zip(key, value)))  # {'root': '111', 'westos': '222'}



print("16.3，字符串转字典 json.loads(string)".center(100, "-"))
# 注意：字符串格式必须符合字典keys和values格式
import json
dict20 = {'a': '192.168.1.1', 'b':'192.168.1.2'}
# 字典 转 字符串，json.dumps()
str20 = json.dumps(dict20)
print(str20)   # {"a": "192.168.1.1", "b": "192.168.1.2"}  //双引号是字符串
# 字符串 转 字典，json.loads()
dict20 = json.loads(str20)
print(dict20)  # {'a': '192.168.1.1', 'b': '192.168.1.2'}  //单引号是字典


print("16.4，字典转字符串、元组、列表".center(100, "-"))
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


dict18 = {'name': 'Zara', 'age': 7, 'class': 'First'}
print(dict18[1])
