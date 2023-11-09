# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-4-21
# Description   : 字典对象层
# https://www.jb51.net/article/167029.htm
# https://www.cnblogs.com/it-tsz/p/10605021.html set集合
# 字典是Python语言中唯一的映射类型。
# 映射类型对象里哈希值（键，key）和指向的对象（值，value）是一对多的的关系，通常被认为是可变的哈希表。
# 字典对象是可变的，它是一个容器类型，能存储任意个数的Python对象，其中也可包括其他容器类型。
# # 字典形式
# a = dict(one=1, two=2, three=3)
# b = {'one': 1, 'two': 2, 'three': 3}
# c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
# d = dict([('two', 2), ('one', 1), ('three', 3)])
# e = dict({'three': 3, 'one': 1, 'two': 2})
# print(a == b == c == d == e)  # True
# *********************************************************************

"""
todo:【转换】
1.1 字典转字符串   json.dumps(dict1)
1.2 字符串转字典  json.loads('{"a": 5, "b": 6}')
1.3 字典转文件
    with open("dict.json", "w+") as f:
        json.dump(dict(a=5, b=6), f)
1.4 文件转字典
    with open("dict.json", "r") as f:
        print(json.load(f))  # {'a': 5, 'b': 6}
1.5 字典key转列表(ChainMap)  list(ChainMap(dict1))
1.6 列表转字典（fromkeys） dict.fromkeys(list1, value) => dict.fromkeys(['a',5], 1) => {'a':1, 5:1}

todo:【合并、键值覆盖互换、删除保留key、批量更新value】
2.1 覆盖合并当前字典(update)
覆盖合并当前字典（python 3.9之后版本支持，合并操作符｜= ， 等价于update）
2.2 覆盖合并新字典({**,**})  分析：将d2更新到d1，且后者覆盖前者重复的key
覆盖合并新字典（python 3.9之后版本支持，合并操作符｜）
2.3 覆盖合并当前字典（deepcopy）
2.4 覆盖合并新字典（可迭代对象itertools）
2.5 覆盖合并新字典（list）
2.6 不覆盖合并新字典（ChainMap）
2.7 非重合并新字典（dict{**,**}）分析：两个字典中不能有重复的key，否则报错
2.8 合并累加相同key的值
2.9 键值覆盖互转  {v:k for k,v in dict.items()} , 如：dict = {'Python': 1, 'Java': 2j}  =>  {1: 'Python', 2: 'Java'}
2.10 删除字典中的key  delKey(dict，key) delKey({"a": 5, "b": 6, "c": 7, "d": 8}, "b", "d"))  # {'a': 5, 'c': 7}
2.11 保留字典中的key  reserveKey(dict，key) reserveKey({"a": 5, "b": 6, "c":7, "d":8}, "b", "d"))  # {'b': 6, 'd': 8}
2.12 批量更新value   {k: v + 2 for k, v in varDict.items()} ， {"a": 5, "b": 6」 => {"a": 7, "b": 8}

3 判断是否是字典 isDict()

todo:【交集、并集、差集、对称差集】
4.1 字典key的交集 getKeyByIntersection
4.2 字典key的并集 getKeyByUnion
4.3 字典key的差集 getKeyByDifference
4.4 字典key的对称差集 getKeyBySemmetricDifference
4.5 字典Item的交集 getItemByIntersection
4.6 字典Item的并集 getItemByUnion
4.7 字典Item的差集 getItemByDifference
4.8 字典Item的对称差集 getItemBySemmetricDifference

todo:【分组】
5.1 对字段1分组并显示对应字段2的值（按性别分组显示姓名）    getOneByGroupField(varTuple, 'gender', 'name')
5.2 对字段1分组并显示所有字段的值（按性别分组显示所有值）  getAllByGroupField(varTuple, 'gender')

"""

from collections import ChainMap
from collections import Counter
import json
from functools import reduce
import itertools

class DictPO:

    def sumValueBySameKey(self, *varDict):
        # 2.8 合并累加相同key的值
        counter = Counter()
        for i in range(len(varDict)):
            counter.update(varDict[i])
        return counter.most_common()

    def delKey(self, varDict, *varKey):
        # 2.10 删除字典中的key
        list1 = []
        for i in range(len(varKey)):
            list1.append(varKey[i])
        remove = set(list1)
        return {k: v for k, v in varDict.items() if k not in remove}

    def reserveKey(self, varDict, *varKey):
        # 2.11 只保留部分key
        list1 = []
        for i in range(len(varKey)):
            list1.append(varKey[i])
        reserve = set(list1)
        return {k: v for k, v in varDict.items() if k in reserve}


    def isDict(self, str1):
        # 3 判断是否是字典
        try:
            json.loads(str1)
        except:
            return False
        return True


    def getKeyByIntersection(self, dict1, dict2):
        # 4.1 key交集（设A，B是两个集合，由所有属于集合A且属于集合B的元素所组成的集合，叫做集合A与集合B的交集（intersection），记作A∩B）
        return [k for k in dict1.keys() & dict2.keys()]

    def getKeyByUnion(self, dict1, dict2):
        # 4.2 key并集（给定两个集合A，B，把他们所有的元素合并在一起组成的集合，叫做集合A与集合B的并集，记作A∪B）
        return [k for k in dict1.keys() | dict2.keys()]

    def getKeyByDifference(self, dict1, dict2):
        # 4.3 key差集, dict1-dict2表示的是属于dict1但不属于dict2的所有元素组成的集合
        return [k for k in dict1.keys() - dict2.keys()]

    def getKeyBySemmetricDifference(self, dict1, dict2):
        # 4.4 key对称差 （两个集合的对称差是只属于其中一个集合，而不属于另一个集合的元素组成的集合。 ）
        # 即两个相对补集的并集
        # 即两个集合的并集减去它们的交集
        return [k for k in dict1.keys() ^ dict2.keys()]

    def getItemByIntersection(self, dict1, dict2):
        # 4.5 item交集（设A，B是两个集合，由所有属于集合A且属于集合B的元素所组成的集合，叫做集合A与集合B的交集（intersection），记作A∩B）
        return list((dict1.items() & dict2.items()))

    def getItemByUnion(self, dict1, dict2):
        # 4.6 item并集（给定两个集合A，B，把他们所有的元素合并在一起组成的集合，叫做集合A与集合B的并集，记作A∪B）
        return list((dict1.items() | dict2.items()))

    def getItemByDifference(self, dict1, dict2):
        # 4.7 item差集, dict1-dict2表示的是属于dict1但不属于dict2的所有元素组成的集合
        return list((dict1.items() - dict2.items()))

    def getItemBySemmetricDifference(self, dict1, dict2):
        # 4.8 item对称差 （两个集合的对称差是只属于其中一个集合，而不属于另一个集合的元素组成的集合。 ）
        # 即两个相对补集的并集
        # 即两个集合的并集减去它们的交集
        return list((dict1.items() ^ dict2.items()))


    def getOneByGroupField(self, varMoreDict, varGroupBy, varValue):
        # 5.1 对字段1分组并显示对应字段2的值（按性别分组显示姓名）
        def group_by_value(accumulator, value):
            # print(accumulator)
            accumulator[value[varGroupBy]].append(value[varValue])
            return accumulator

        dict2 = {}
        for t in range(len(varMoreDict)):
            for k, v in varMoreDict[t].items():
                if k == varGroupBy:
                    dict2[varMoreDict[t][k]] = []

        return reduce(group_by_value, varMoreDict, dict2)

    def getAllByGroupField(self, varTuple, varGroupByName):
        # 5.2 对字段1分组并显示所有字段的值（按性别分组显示所有值)
        return {
            item[0]: list(item[1]) for item in itertools.groupby(varTuple, lambda x: x[varGroupByName])
        }


if __name__ == "__main__":

    # todo main
    Dict_PO = DictPO()

    # d1 = dict(a=1, b=2, test=3)
    # d2 = dict(a=10, b=20, dev=30)
    # d3 = dict(a=200, b=200, prd=300)

    # print("1.1 字典转字符串(dumps)".center(100, "-"))
    # d1 = {'python': 1, 'java': 2, 'c': 3}
    # print(json.dumps(d1))  # {"python": 1, "java": 2, "c": 3}  //双引号是字符串
    #
    # print("1.2 json字符串转字典(loads)".center(100, "-"))
    # print(json.loads('{"a": 5, "b": 6}'))  # {'a': 5, 'b': 6}  //单引号是字典

    # print("1.3 字典转文件".center(100, "-"))
    # with open("./data/dictPO.json", "w+") as f:
    #     json.dump(dict(a=5, b=6), f)
    #
    # print("1.4 文件转字典".center(100, "-"))
    # with open("dict.json", "r") as f:
    #     print(json.load(f))  # {'a': 5, 'b': 6}

    # print("1.5 字典key转列表(ChainMap)".center(100, "-"))
    # d1 = {'python': 1, 'java': 2, 'c': 3}
    # print(list(ChainMap(d1)))  # ['python', 'java', 'c']

    # print("1.6 列表转字典(fromkeys)".center(100, "-"))
    print(dict.fromkeys(['a', 5], 1))  # {'a': 1, 5: 1}
    dict1 = dict.fromkeys(['a', 5])  # {'a': None, 5: None}
    print(dict1)

    d1 = {'name':'jinhao' , "age":43}
    d2 = {'gender':"male", "name":"yoyo"}
    dd = {'address':'pudong'}

    # print("2.1 覆盖合并当前字典(update)".center(100, "-"))
    # d1.update(d2)
    # print(d1)  # {'name': 'yoyo', 'age': 43, 'gender': 'male'}

    # print("覆盖合并当前字典（python 3.9之后版本支持，合并操作符｜= ， 等价于update）".center(100, "-"))
    # d1 |= d2
    # print(d1)  # {'name': 'yoyo', 'age': 43, 'gender': 'male'}

    # print("2.2 覆盖合并新字典({**,**})".center(100, "-"))
    # d4 = {**d1, **d2}
    # print(d4)  # {'name': 'yoyo', 'age': 43, 'gender': 'male'}

    # print("覆盖合并新字典（python 3.9之后版本支持，合并操作符｜）".center(100, "-"))
    # d7 = d1 | d2
    # print(d7)  # {'name': 'yoyo', 'age': 43, 'gender': 'male'}

    # print("2.3 覆盖合并当前字典（deepcopy）".center(100, "-"))
    # # 分析：使用深度拷贝一个新的字典即可,不影响原来的字典值
    # from copy import deepcopy
    # d3 = deepcopy(d1)
    # d3.update(d2)
    # print(d1)  # {'name': 'jinhao', 'age': 43}
    # print(d3)  # {'name': 'yoyo', 'age': 43, 'gender': 'male'}

    # print("2.4 覆盖合并新字典（可迭代对象itertools）".center(100, "-"))
    # import itertools
    # print(d1.items)  # <built-in method items of dict object at 0x7fb145b8c9c0>
    # d5 = dict(itertools.chain(d1.items(), d2.items()))  # <built-in method items of dict object at 0x7f892238c980>
    # print(d5)  # {'name': 'yoyo', 'age': 43, 'gender': 'male'}

    # print("2.5 覆盖合并新字典（list）".center(100, "-"))
    # d6 = dict(list(d1.items()) + list(d2.items()))
    # print(d6)  # {'name': 'yoyo', 'age': 43, 'gender': 'male'}

    # print("2.6 不覆盖合并新字典（ChainMap）".center(100, "-"))
    # from collections import ChainMap
    # d6 = dict(ChainMap(d1, d2))
    # print(d6)  # {'gender': 'male', 'name': 'jinhao', 'age': 43}

    # print("2.7 非重合并新字典（dict{**,**}）".center(100, "-"))
    # 分析：两个字典中不能有重复的key，否则报错
    # d4 = dict(**d1, **d2)
    # print(d4)  # TypeError: type object got multiple values for keyword argument 'name'  //因为有重复的key
    # d4 = dict(**d1, **dd)
    # print(d4)  # {'name': 'jinhao', 'age': 43, 'address': 'pudong'}

    # print("2.8 合并累加相同key的值".center(100, "-"))
    # print(Dict_PO.sumValueBySameKey({"a": 10000, "b": 1}, {"a": 10000, "b": 1},
    #                                 {"a": 40000, "b": 1, "c": 333}))  # [('a', 60000), ('c', 333), ('b', 3)]
    #
    # print("2.9 键值覆盖互转".center(100, "-"))
    # d1 = {'python': 1, 'java': 2, 'c': 3, 'hellp': 2}
    # print({v: k for k, v in d1.items()})  # {1: 'python', 2: 'hellp', 3: 'c'}

    # print("2.10 删除key".center(100, "-"))
    # print(Dict_PO.delKey({"a": 5, "b": 6, "c": 7, "d": 8}, "b", "d"))  # {'a': 5, 'c': 7}
    # #
    # print("2.11 只保留部分key".center(100, "-"))
    # print(Dict_PO.reserveKey({"a": 5, "b": 6, "c": 7, "d": 8}, "b", "d"))  # {'b': 6, 'd': 8}



    # # print("3 判断是不是字典".center(100, "-"))
    # print(Dict_PO.isDict('{}'))  # True
    # print(Dict_PO.isDict('{\"age\":100 }'))  # True
    # print(Dict_PO.isDict('{"age":100 }'))  # True
    # print(Dict_PO.isDict('{"foo":[5,6.8],"foo":"bar"}'))  # True
    # print(Dict_PO.isDict("{'age':100 }"))  # False  //最外层是双引号代表字符串，非字典



    # print("4.1-5 获取交、并、差集及对称差集的key".center(100, "-"))
    # d1 = {'python': 1, 'java': 2, 'c': 3}
    # d2 = {'python': 10, 'java': 2, 'c++': 88}
    # print(Dict_PO.getKeyByIntersection(d1, d2))  # ['python', 'java'] //交集
    # print(Dict_PO.getKeyByUnion(d1, d2))  # ['c', 'python', 'java', 'c++'] //并集
    # print(Dict_PO.getKeyByDifference(d1, d2))  # ['c']  //差集, d1-d2表示的是属于d1但不属于d2的所有元素组成的集合
    # print(Dict_PO.getKeyBySemmetricDifference(d1, d2))  # ['c', 'c++'] //对称差，两集合所有不相同的元素的集合，即并集减去交集

    # # print("4.5-8 获取交、并、差集及对称差集的item".center(100, "-"))
    # d1 = {'python': 1, 'java': 2, 'c': 3}
    # d2 = {'python': 10, 'java': 2, 'c++': 88}
    # print(Dict_PO.getItemByIntersection(d1, d2))  # [('java', 2)] //交集
    # print(Dict_PO.getItemByUnion(d1, d2))  # [('c', 3), ('python', 1), ('python', 10), ('java', 2), ('c++', 88)] //并集
    # print(Dict_PO.getItemByDifference(d1, d2))  # [('c', 3), ('python', 1)]  //差集
    # print(Dict_PO.getItemBySemmetricDifference(d1, d2))  # [('python', 1), ('python', 10), ('c++', 88), ('c', 3)] //对称差集



    # # print("5.1 按性别分组显示姓名".center(100, "-"))
    # tuple = ({'name': 'jinhao', 'age': 105, 'gender': 'male'},
    #             {'name': 'baba', 'age': 76, 'gender': 'male'},
    #             {'name': 'mama', 'age': 202, 'gender': 'female'},
    #             {'name': 'yoyo', 'age': 84, 'gender': 'female'})
    # print(Dict_PO.getOneByGroupField(tuple, 'gender', 'age'))  # {'male': ['jinhao', 'baba'], 'female': ['mama', 'yoyo']}
    # #
    # # print("5.2 按性别分组显示所有值".center(100, "-"))
    # print(Dict_PO.getAllByGroupField(tuple, 'gender'))  # {'male': [{'name': 'jinhao', 'age': 105, 'gender': 'male'}, {'name': 'baba', 'age': 76, 'gender': 'male'}], 'female': [{'name': 'mama', 'age': 202, 'gender': 'female'}, {'name': 'yoyo', 'age': 84, 'gender': 'female'}]}
