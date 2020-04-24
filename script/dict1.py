# coding: utf-8
# *******************************************************************
# Author     : John
# Date       : 2019-1-29
# Description: 字典使用方法 common - dict1.py
# 字典的重点:
# 1，dict 的键是唯一的，如果存在重复的键，则排列最后的一个键值对有效。
# 2，dict 值可以取任何数据类型，但键必须是不可变类型，如字符串，数字或元组。
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

其他：
1、operator.eq(dict1,dict2)，operator.ne(dict1,dict2)，(for py3.x)比較两个字典元素，返回Ture或False
   cmp(dict1, dict2) ，(for py2.7)
'''

# ********************************************************************************************************************

# 1，字典的新增键值、修改值、删键、弹键、清空字典、删除字典
# dict1 = {"a": "123", "b": "456", "c": "789"}

# 使用dict关键字新增字典，注意key只能是字符串，不能是数字或元组
dict1 = dict(a='123',b='456',c='789')
print(dict1) # {'a': '123', 'b': '456', 'c': '789'}

# 新增键值
dict1[100] = "watermelon"
print(dict1)  # {'a': '123', 'b': '456', 'c': '789', 100: 'watermelon'}

# 新增默认键，setdefault(key)方法
dict1.setdefault("d") # 如果d不存在则新增这个键（默认值为None)。
print(dict1) # {'a': '123', 'b': '456', 'c': '789', 100: 'watermelon', 'd': None}
dict1["d"] = "apple"
dict1.setdefault("d", "default")  # 如果d已存在，则输出原值。
print(dict1) # {'a': '123', 'b': '456', 'c': '789', 100: 'watermelon', 'd': 'apple'}

# 修改值
dict1["b"] = "bananan"
print(dict1)  # {'a': '123', 'b': 'bananan', 'c': '789', 100: 'watermelon', 'd': 'apple'}

# 删除键 (没有返回值)
del (dict1["a"])
print(dict1) # {'b': 'bananan', 'c': '789', 'z': 'watermelon'}

# 弹出键 (有返回b的值）
print(dict1.pop("b"))  # banana
print(dict1)  # {'c': '789', 100: 'watermelon', 'd': 'apple'}
print(dict1.pop("b2",777))  # 777
print(dict1)  # {'c': '789', 100: 'watermelon', 'd': 'apple'}

# 清空字典（非删除）
dict1.clear()
print(dict1)  # {}

# 删除字典
del dict1
# print(dict1)  # 报错 NameError: name 'dict1' is not defined

# ********************************************************************************************************************

# 2，获取字典的值，字典的键不可变，只能用数字、字符串或元组作为键
dict2 = {4: ("apple",), "b": {"123": "banana", "o": "orange"}, (2,"yoyo"): ["grape", "grapefruit"]}
print(dict2[4])  # ('apple',)
print(dict2[4][0])  # apple
print(dict2["b"])  # {'123': 'banana', 'o': 'orange'}
print(dict2["b"]["123"])  # banana
print(dict2[(2,"yoyo")])  # ['grape', 'grapefruit']
print(dict2[(2,"yoyo")][1])  # grapefruit

# 获取字典值或设置默认值，get(key,defaultValue)方法
dict2 = {"a" : "123", "b" : "456", "c" : "789"}
print(dict2.get("c", "11111"))  # 1，如果键值c存在, 输出原值，如 789
print(dict2.get("z", "没有找到"))  # 2，如果键值z不存在, 则输出默认值 apple
# 场景：查找字典中的key，找到返回value，否则返回提示
def searchKeyValue(key):
    print(dict2.get(key, "error,没有找到!")) # 没有找到的话，返回：error,没有找到!
searchKeyValue("test")

# ********************************************************************************************************************

# 3，字典遍历
# 遍历dict，输出key与value
dict3 = {"a" : "123", "b" : "456", "c" : "789"}
for k in dict3:
    print("dict3[%s] =" % k, dict3[k])
    # print(k,dict3[k])

# 遍历itmes()，输出key与value (# Python3.5中 iteritems变为items())
for k, v in dict3.items():
    print("dict3[%s] =" % k, v)
    # print(k, dict[k])

# 只遍历keys()，输出keys
for k in dict3.keys():
    print(k)

# 只遍历values()，输出values
for v in dict3.values():
    print(v)

# ********************************************************************************************************************


# 4, 多个字典合并，update()方法，相同key则覆盖
dict41 = {"a" : "123", "b" : "456"}
dict42 = {"c" : "789", "d" : "john"}
dict43 = {"e" : "eee", "a" : "fff"}
dict41.update(dict42)  # 将dict2并入dict1
dict41.update(dict43)  # 将dict3并入dict1
print(dict41) # {'a': '123', 'b': '456', 'c': '789', 'd': 'john', 'e': 'eee', 'f': 'fff'}
print(dict42) # {'c': '789', 'd': 'john'}
print(dict43) # {'e': 'eee', 'f': 'fff'}

# 2个字典合并，传统遍历方法
dict41 = {"a" : "123", "b" : "456"}
dict42 = {"c" : "789", "d" : "haha"}
for k in dict42:
    dict41[k] = dict42[k]
print(dict41) # {'a': '123', 'b': '456', 'c': '789', 'd': 'haha'}

# 2个字典合并，相同key则覆盖。
dict41 = {"a" : "123", "b" : "456"}
dict42 = {"b" : "777", "c" : "888"}
for k in dict42:
    dict41[k] = dict42[k]
print(dict41) # {'a': '123', 'b': '777', 'c': '888'}

# ********************************************************************************************************************


# 5, 字典排序，sorted()方法，返回列表
dict5 = {"a" : "apple", "z" : "grape", "c" : "orange", "d" : "banana"}
# 对key排序
print(sorted(dict5.items(), key=lambda d: d[0])) # [('a', 'apple'), ('c', 'orange'), ('d', 'banana'), ('z', 'grape')]
# 对value排序
print(sorted(dict5.items(), key=lambda d: d[1])) # [('a', 'apple'), ('d', 'banana'), ('z', 'grape'), ('c', 'orange')]


# ********************************************************************************************************************

# 6，字典拷贝
# 1、直接赋值：就是对象的引用（别名）。
# 2、浅拷贝(copy)：# 拷贝父对象，引用子对象。{'父key': '父value', '父key': [子value, 子value]}
# 3、深拷贝(deepcopy)： copy 模块的 deepcopy 方法，全拷贝父子对象。
import copy
dict61 = {"a": "apple", "b": [1, 2, 3]}

# b = a: 赋值引用，a 和 b 都指向同一个对象。
dict62 = dict61

# b = a.copy(): 浅拷贝, a 和 b 是一个独立的对象，但他们的子对象还是指向统一对象（是引用）。
dict63 = dict61.copy()

# b = copy.deepcopy(a): 深度拷贝, a 和 b 完全拷贝了父对象及其子对象，两者是完全独立的。
dict64 = copy.deepcopy(dict61)  # 返回一个字典的深复制

dict61['a'] = "father"
dict61['b'].remove(1)  # 移除了b中子对象1

print(dict61)  # {'a': 'father', 'b': [2, 3]}
print(dict62)  # {'a': 'father', 'b': [2, 3]}
print(dict63)  # {'a': 'apple', 'b': [2, 3]}
print(dict64)  # {'a': 'apple', 'b': [1, 2, 3]}

# ********************************************************************************************************************
# 7，字典转换

# 1、字典
dict7 = {'name': 'Zara', 'age': 7, 'class': 'First'}

# 字典 转 字符串
print(type(str(dict7)), str(dict7)) # <type 'str'> {'age': 7, 'name': 'Zara', 'class': 'First'}

# 字典 转 元组keys (返回元组内容是keys的集合)
print(type(tuple(dict7)), tuple(dict7)) # <class 'tuple'> ('name', 'age', 'class')

# 字典 转 元组values (返回元组内容是values的集合)
print(tuple(dict7.values()))  # ('Zara', 7, 'First')

# 字典 转 列表keys (返回列表内容是keys的集合)
print(list(dict7))  # ['age', 'name', 'class']

# 字典 转 列表values (返回列表内容是values的集合)
print(list(dict7.values()))  # ['Zara', 7, 'First']

# 元组 转 字典，fromkeys()方法"
seq = ('Google', 'Runoob', 'Taobao')
print(dict7.fromkeys(seq)) # {'Google': None, 'Taobao': None, 'Runoob': None}
print(dict7.fromkeys(seq, 10)) # {'Google': 10, 'Taobao': 10, 'Runoob': 10}

# 列表 转 字典，列表中keys部分要符合字典要求，如只能是 数字、字符、元组
l3 = [(7, 'xidada'), ('age', 64),((1,2),444)]
print(dict(l3)) # {7: 'xidada', 'age': 64, (1, 2): 444}

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


# ********************************************************************************************************************

# 8，判断字典key是否存在，区分大小写，返回Ture或False
dict8 = {'Name': 'Zara', 'Age': 7}
# py3.X , 使用 __contains__()
print(dict8.__contains__('Name')) # True
print(dict8.__contains__('sex'))  # False
# py2.7 , 使用 has_key()
# print( "Value : %s" %  dict.has_key('name')  )# Value : True
# print( "Value : %s" %  dict8.has_key('Sex') ) # Value : False


dict7 = {'name': 'Zara', 'age': 7, 'class': 'First'}
# 字典 转 列表keys (返回列表内容是keys的集合)
print(list(dict7))  # ['age', 'name', 'class']

# 字典 转 列表values (返回列表内容是values的集合)
print(list(dict7.values()))  # ['Zara', 7, 'First']


# 字典 转 字符串
dict1 = {'name': 'Zara', 'age': 7, 'class': 'First'}
print(type(str(dict1)), str(dict1))  # <class 'str'> {'name': 'Zara', 'age': 7, 'class': 'First'}