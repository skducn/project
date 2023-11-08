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
1.1 字典转字符串     json.dumps(dict(a=5, b=6)))  # {"a": 5, "b": 6}  双引号是字符串
1.2 json字符串转字典  json.loads('{"a": 5, "b": 6}')
1.3 字典转字符串并保存到文件
    with open("dict.json", "w+") as f:
        json.dump(dict(a=5, b=6), f)
1.4 将 JSON 转字典并保持到文件
    with open("dict.json", "r") as f:
        print(json.load(f))  # {'a': 5, 'b': 6}
1.5 字典key转列表（去重） dictKey2list(*dict1)
1.6 判断字符串是否是json格式的字典 is_json()

todo:【合并、交集、并集、差集、对称差集、键值覆盖互换】
    d1 = {'name':'jinhao' , "age":43}
    d2 = {'gender':"male", "name":"yoyo"}
    dd = {'address':'pudong'}
合并字典
# 2.1 覆盖合并当前字典(update)
# d1.update(d2)
# print(d1)  # {'name': 'yoyo', 'age': 43, 'gender': 'male'}

# 覆盖合并当前字典（python 3.9之后版本支持，合并操作符｜= ， 等价于update）
# d1 |= d2
# print(d1)  # {'name': 'yoyo', 'age': 43, 'gender': 'male'}

# 2.2 覆盖合并新字典({**,**})
# 分析：将d2更新到d1，且后者覆盖前者重复的key
# d4 = {**d1, **d2}
# print(d4)  # {'name': 'yoyo', 'age': 43, 'gender': 'male'}

# 覆盖合并新字典（python 3.9之后版本支持，合并操作符｜）
# d7 = d1 | d2
# print(d7)  # {'name': 'yoyo', 'age': 43, 'gender': 'male'}

# 2.3 覆盖合并当前字典（deepcopy）
# # 分析：使用深度拷贝一个新的字典即可,不影响原来的字典值
# from copy import deepcopy
# d3 = deepcopy(d1)
# d3.update(d2)
# print(d1)  # {'name': 'jinhao', 'age': 43}
# print(d3)  # {'name': 'yoyo', 'age': 43, 'gender': 'male'}

# 2.4 覆盖合并新字典（可迭代对象itertools）
# import itertools
# print(d1.items)  # <built-in method items of dict object at 0x7fb145b8c9c0>
# d5 = dict(itertools.chain(d1.items(), d2.items()))  # <built-in method items of dict object at 0x7f892238c980>
# print(d5)  # {'name': 'yoyo', 'age': 43, 'gender': 'male'}

# 2.5 覆盖合并新字典（list）
# d6 = dict(list(d1.items()) + list(d2.items()))
# print(d6)  # {'name': 'yoyo', 'age': 43, 'gender': 'male'}

# 2.6 不覆盖合并新字典（ChainMap）
# from collections import ChainMap
# d6 = dict(ChainMap(d1, d2))
# print(d6)  # {'gender': 'male', 'name': 'jinhao', 'age': 43}

# 2.7 非重合并新字典（dict{**,**}）
# 分析：两个字典中不能有重复的key，否则报错
# d4 = dict(**d1, **d2)
# print(d4)  # TypeError: type object got multiple values for keyword argument 'name'  //因为有重复的key
# d4 = dict(**d1, **dd)
# print(d4)  # {'name': 'jinhao', 'age': 43, 'address': 'pudong'}

2.8.1 字典key的交集 getKeyByIntersection
2.8.2 字典key的并集 getKeyByUnion
2.8.3 字典key的差集 getKeyByDifference
2.8.4 字典key的对称差集 getKeyBySemmetricDifference
2.8.5 字典Item的交集 getItemByIntersection
2.8.6 字典Item的并集 getItemByUnion
2.8.7 字典Item的差集 getItemByDifference
2.8.8 字典Item的对称差集 getItemBySemmetricDifference

2.9 键值覆盖互转  # print({v:k for k,v in dict.items()}) , 如：dict = {'Python': 1, 'Java': 2j}  =>  {1: 'Python', 2: 'Java'}

todo:【key】
4.1 删除字典中的key  delKey(dict，key) delKey({"a": 5, "b": 6, "c": 7, "d": 8}, "b", "d"))  # {'a': 5, 'c': 7}
4.2 保留字典中的key  reserveKey(dict，key) reserveKey({"a": 5, "b": 6, "c":7, "d":8}, "b", "d"))  # {'b': 6, 'd': 8}

todo:【value】
5.1 累加相同key的值 sumValueBySameKey({"a": 10000, "b": 1}, {"a": 10000, "b": 1}, {"a": 40000, "b": 1, "c" : 333}))  # [('a', 60000), ('c', 333), ('b', 3)]
5.2 字典value的加减乘除 countValue('+', d5, 2)

todo:[分组]
6.1 对字段1分组并显示对应字段2的值（按性别分组显示姓名）    getOneByGroupField(varTuple, 'gender', 'name')
6.2 对字段1分组并显示所有字段的值（按性别分组显示所有值）  getAllByGroupField(varTuple, 'gender')


6.1 collections中defaultdict之字典的 value 是字典
6.1 collections中defaultdict之字典的 value 是列表
6.1 collections中defaultdict之字典的 value 是lambda表达式
6.4 collections中defaultdict之字典的 value 里又是字典


"""

from collections import ChainMap
from collections import Counter
import json
from functools import reduce
import itertools

class DictPO:

    def dictKey2list(self, *varDict):

        """
        1.5 字典key转换列表（去重）
        :return: list
        此函数最多接收5个字典
        """

        if len(varDict) == 1:
            return list(ChainMap(varDict[0]))
        elif len(varDict) == 2:
            return list(ChainMap(varDict[0], varDict[1]))
        elif len(varDict) == 3:
            return list(ChainMap(varDict[0], varDict[1], varDict[2]))
        elif len(varDict) == 4:
            return list(ChainMap(varDict[0], varDict[1], varDict[2], varDict[3]))
        elif len(varDict) == 5:
            return list(
                ChainMap(varDict[0], varDict[1], varDict[2], varDict[3], varDict[4])
            )
        else:
            return 0

    def is_json(self, str1):

        """
        1.6 判断字符串是否是json格式的字典
        :return:
        """

        try:
            json_object = json.loads(str1)
        except:
            return False
        return True


    def getKeyByIntersection(self, dict1, dict2):
        # key交集（设A，B是两个集合，由所有属于集合A且属于集合B的元素所组成的集合，叫做集合A与集合B的交集（intersection），记作A∩B）
        return [k for k in dict1.keys() & dict2.keys()]

    def getKeyByUnion(self, dict1, dict2):
        # key并集（给定两个集合A，B，把他们所有的元素合并在一起组成的集合，叫做集合A与集合B的并集，记作A∪B）
        return [k for k in dict1.keys() | dict2.keys()]

    def getKeyByDifference(self, dict1, dict2):
        # key差集, dict1-dict2表示的是属于dict1但不属于dict2的所有元素组成的集合
        return [k for k in dict1.keys() - dict2.keys()]

    def getKeyBySemmetricDifference(self, dict1, dict2):
        # key对称差 （两个集合的对称差是只属于其中一个集合，而不属于另一个集合的元素组成的集合。 ）
        # 即两个相对补集的并集
        # 即两个集合的并集减去它们的交集
        return [k for k in dict1.keys() ^ dict2.keys()]


    def getItemByIntersection(self, dict1, dict2):
        # item交集（设A，B是两个集合，由所有属于集合A且属于集合B的元素所组成的集合，叫做集合A与集合B的交集（intersection），记作A∩B）
        return list((dict1.items() & dict2.items()))

    def getItemByUnion(self, dict1, dict2):
        # item并集（给定两个集合A，B，把他们所有的元素合并在一起组成的集合，叫做集合A与集合B的并集，记作A∪B）
        return list((dict1.items() | dict2.items()))

    def getItemByDifference(self, dict1, dict2):
        # item差集, dict1-dict2表示的是属于dict1但不属于dict2的所有元素组成的集合
        return list((dict1.items() - dict2.items()))

    def getItemBySemmetricDifference(self, dict1, dict2):
        # item对称差 （两个集合的对称差是只属于其中一个集合，而不属于另一个集合的元素组成的集合。 ）
        # 即两个相对补集的并集
        # 即两个集合的并集减去它们的交集
        return list((dict1.items() ^ dict2.items()))


    def delKey(self, varDict, *varKey):

        """
        4.1 删除字典中的key
        :param varDict:
        :return:
        """

        list1 = []
        for i in range(len(varKey)):
            list1.append(varKey[i])
        remove = set(list1)
        return {k: v for k, v in varDict.items() if k not in remove}

    def reserveKey(self, varDict, *varKey):

        """
        4.2 保留字典中的key
        :param varDict:
        :return:
        """

        list1 = []
        for i in range(len(varKey)):
            list1.append(varKey[i])
        reserve = set(list1)
        return {k: v for k, v in varDict.items() if k in reserve}

    def sumValueBySameKey(self, *varDict):

        """
        5.1 累加相同key的值
        :param varDict:
        :return:
        """

        counter = Counter()
        for i in range(len(varDict)):
            counter.update(varDict[i])
        return counter.most_common()

    def countValue(self, varOperator, varDict, n):

        """
        5.2 字典value的加减乘除
        :param varDict:
        :return:
        """

        try:
            if varOperator == "+":
                return {k: v + n for k, v in varDict.items()}
            if varOperator == "-":
                return {k: v - n for k, v in varDict.items()}
            if varOperator == "*":
                return {k: v * n for k, v in varDict.items()}
            if varOperator == "/":
                return {k: v / n for k, v in varDict.items()}
            else:
                return None
        except:
            return None

    def getOneByGroupField(self, varMoreDict, varGroupBy, varValue):

        """
        6.1 对字段1分组并显示对应字段2的值（按性别分组显示姓名）
        :param varDict:
        :return:
        """

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

    def getAllByGroupField(self, varMoreDict, varGroupBy):

        """
        6.2 对字段1分组并显示所有字段的值（按性别分组显示所有值
        :param varDict:
        :return:
        """

        return {
            item[0]: list(item[1])
            for item in itertools.groupby(varMoreDict, lambda x: x[varGroupBy])
        }


if __name__ == "__main__":

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

    print("1.5 key转list(ChainMap)".center(100, "-"))
    d1 = {'python': 1, 'java': 2, 'c': 3}
    print(list(ChainMap(d1)))  # ['python', 'java', 'c']
    # print(Dict_PO.dictKey2list(d1))  # ['a', 'b', 'test']
    # print(Dict_PO.dictKey2list(d1, d2))  # ['a', 'b', 'dev', 'test']
    # print(Dict_PO.dictKey2list(d1, d2, d3))  # ['a', 'b', 'prd', 'dev', 'test']
    #
    # print("1.6 判断字符串是否是json格式的字典".center(100, "-"))
    # print(Dict_PO.is_json("{}"))  # True
    # print(Dict_PO.is_json("{abcd}"))  # False
    # print(Dict_PO.is_json('{ "age":100}'))  # True
    # print(Dict_PO.is_json("{'age':100 }"))  # False
    # print(Dict_PO.is_json("{\"age\":100 }"))  # True
    # print(Dict_PO.is_json('{"age":100 }'))  # True
    # print(Dict_PO.is_json('{"foo":[5,6.8],"foo":"bar"}'))  # True



    # print("2.8.1-4 获取交、并、差集及对称差集的key".center(100, "-"))
    # d1 = {'python': 1, 'java': 2, 'c': 3}
    # d2 = {'python': 10, 'java': 2, 'c++': 88}
    # print(Dict_PO.getKeyByIntersection(d1, d2))  # ['python', 'java'] //交集
    # print(Dict_PO.getKeyByUnion(d1, d2))  # ['c', 'python', 'java', 'c++'] //并集
    # print(Dict_PO.getKeyByDifference(d1, d2))  # ['c']  //差集, d1-d2表示的是属于d1但不属于d2的所有元素组成的集合
    # print(Dict_PO.getKeyBySemmetricDifference(d1, d2))  # ['c', 'c++'] //对称差，两集合所有不相同的元素的集合，即并集减去交集

    # # print("2.8.5-8 获取交、并、差集及对称差集的item".center(100, "-"))
    # d1 = {'python': 1, 'java': 2, 'c': 3}
    # d2 = {'python': 10, 'java': 2, 'c++': 88}
    # print(Dict_PO.getItemByIntersection(d1, d2))  # [('java', 2)] //交集
    # print(Dict_PO.getItemByUnion(d1, d2))  # [('c', 3), ('python', 1), ('python', 10), ('java', 2), ('c++', 88)] //并集
    # print(Dict_PO.getItemByDifference(d1, d2))  # [('c', 3), ('python', 1)]  //差集
    # print(Dict_PO.getItemBySemmetricDifference(d1, d2))  # [('python', 1), ('python', 10), ('c++', 88), ('c', 3)] //对称差集


    # print("2.9 键值覆盖互转".center(100, "-"))
    # d1 = {'python': 1, 'java': 2, 'c': 3, 'hellp': 2}
    # print({v: k for k, v in d1.items()})  # {1: 'python', 2: 'hellp', 3: 'c'}

    # print("4.1 删除字典中的key".center(100, "-"))
    # print(Dict_PO.delKey({"a": 5, "b": 6, "c": 7, "d": 8}, "b", "d"))  # {'a': 5, 'c': 7}
    #
    # print("4.2 保留字典中的key".center(100, "-"))
    # print(Dict_PO.reserveKey({"a": 5, "b": 6, "c": 7, "d": 8}, "b", "d"))  # {'b': 6, 'd': 8}

    # print("5.1 累加相同key的值".center(100, "-"))
    # print(Dict_PO.sumValueBySameKey({"a": 10000, "b": 1}, {"a": 10000, "b": 1}, {"a": 40000, "b": 1, "c" : 333}))  # [('a', 60000), ('c', 333), ('b', 3)]
    #
    # d5 = {"a": 6, "b": 8, "c": 12.2, "d": 9}
    #
    # print("5.2 字典value的加减乘除".center(100, "-"))
    # print(Dict_PO.countValue('+', d5, 2))  # {'a': 8, 'b': 10, 'c': 14.2, 'd': 11}
    # print(Dict_PO.countValue('-', d5, 2))  # {'a': 4, 'b': 6, 'c': 10.2, 'd': 7}
    # print(Dict_PO.countValue('*', d5, 2))  # {'a': 12, 'b': 16, 'c': 24.4, 'd': 18}
    # print(Dict_PO.countValue('/', d5, 2))  # {'a': 3.0, 'b': 4.0, 'c': 6.1, 'd': 4.5}

    # print("6.1 按性别分组显示姓名".center(100, "-"))
    # varTuple = ({'name': 'jinhao', 'age': 105, 'gender': 'male'},
    #             {'name': 'baba', 'age': 76, 'gender': 'male'},
    #             {'name': 'mama', 'age': 202, 'gender': 'female'},
    #             {'name': 'yoyo', 'age': 84, 'gender': 'female'})
    # print(Dict_PO.getOneByGroupField(varTuple, 'gender', 'name'))  # {'male': ['jinhao', 'baba'], 'female': ['mama', 'yoyo']}
    #
    # print("6.2 按性别分组显示所有值".center(100, "-"))
    # print(Dict_PO.getAllByGroupField(varTuple, 'gender'))  # {'male': [{'name': 'jinhao', 'age': 105, 'gender': 'male'}, {'name': 'baba', 'age': 76, 'gender': 'male'}], 'female': [{'name': 'mama', 'age': 202, 'gender': 'female'}, {'name': 'yoyo', 'age': 84, 'gender': 'female'}]}
