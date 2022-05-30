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
# *********************************************************************

'''
todo:【转换】
1.1 字典转json字符串     # print(json.dumps(dict(a=5, b=6)))  # {"a": 5, "b": 6}  双引号是字符串
1.2 字典转json字符串保存在文件里
    with open("dict.json", "w+") as f:
        json.dump(dict(a=5, b=6), f)
1.3 字典（单个或多个）key转列表（去重）dictKey2list(*dict1)   # ['a', 'b', 'dev', 'test']

todo:【组合、交换key与value、】
2.1 合并字典（合并时如遇重复key,则保留第一个字典键值）mergeDictReserveLeft(*dict1) mergeDictReserveLeft(d1, d2))  # {'a': 1, 'b': 2, 'dev': 444, 'test': 123}
2.2 合并字典（合并时如遇重复key,则保留最后一个字典键值）mergeDictReserveRight(*dict1)
2.3 获取2个字典交、并、对称差集的key getKeyBySet()
2.4 获取2个字典交、并、对称差集的keyvalue getKeyValueBySet()
2.5 字典key与value交换 {v:k for k,v in dict.item()} , 如：dic = {'Python': 1, 'Java': 2j} j交换后 {1: 'Python', 2: 'Java'}
2.6 获取2个字典差集的key（在a不在b的key）
2.7 获取2个字典差集的keyvalue （去掉交集，剩下在a的的keyvalue)

todo:【key】
4.1 删除字典中的key  delKey(dict，key) delKey({"a": 5, "b": 6, "c": 7, "d": 8}, "b", "d"))  # {'a': 5, 'c': 7}
4.2 保留字典中的key  reserveKey(dict，key) reserveKey({"a": 5, "b": 6, "c":7, "d":8}, "b", "d"))  # {'b': 6, 'd': 8}

todo:【value】
5.1 多个字典中相同的key值进行累加 sumValueByKey({"a": 10000, "b": 1}, {"a": 10000, "b": 1}, {"a": 40000, "b": 1, "c" : 333}))  # [('a', 60000), ('c', 333), ('b', 3)]
5.2 字典的数字value加法 addValue({"a": 6, "b": 7, "c": 8, "d": 9}, 2))  # {'a': 7, 'b': 8, 'c': 9, 'd': 10}
5.3 字典的数字value减法 minusValue()

todo:[高级用法 分组]
6.1 按性别分组显示姓名    Dict_PO.groupByValue(varTuple, 'gender', 'name')
6.2 按性别分组显示所有值



6.1 collections中defaultdict之字典的 value 是字典
6.1 collections中defaultdict之字典的 value 是列表
6.1 collections中defaultdict之字典的 value 是lambda表达式
6.4 collections中defaultdict之字典的 value 里又是字典


7.2 json字符串转字典
7.4 从 JSON 文件里恢复字典
'''

from collections import ChainMap
from collections import defaultdict
from collections import Counter
import json
from functools import reduce


class DictPO():


    # 1.3 字典key转换列表（去重）
    def dictKey2list(self, *varDict):
        if len(varDict) == 1:
            return list(ChainMap(varDict[0]))
        elif len(varDict) == 2:
            return list(ChainMap(varDict[0], varDict[1]))
        elif len(varDict) == 3:
            return list(ChainMap(varDict[0], varDict[1], varDict[2]))
        elif len(varDict) == 4:
            return list(ChainMap(varDict[0], varDict[1], varDict[2], varDict[3]))
        elif len(varDict) == 5:
            return list(ChainMap(varDict[0], varDict[1], varDict[2], varDict[3], varDict[4]))
        else:
            return 0

    # 2.1 合并字典（合并时如遇重复key,则保留第一个字典键值）
    def mergeDictReserveLeft(self, *varDict):
        '''
        # 1.1，合并字典（合并时如遇重复key,则保留第一个字典key的值）
        :param varDict:
        :return:
        '''
        d_varMerge = {}

        if len(varDict) == 2:
            c = ChainMap(varDict[0], varDict[1])
        elif len(varDict) == 3:
            c = ChainMap(varDict[0], varDict[1], varDict[2])
        elif len(varDict) == 4:
            c = ChainMap(varDict[0], varDict[1], varDict[2], varDict[3])
        elif len(varDict) == 5:
            c = ChainMap(varDict[0], varDict[1], varDict[2], varDict[3], varDict[4])
        for k, v in c.items():
            d_varMerge[k] = v
        return d_varMerge
    # 2.2，合并字典（合并时如遇重复key,则保留最后一个字典键值）
    def mergeDictReserveRight(self, *varDict):
        '''
        1.2，字典合并（如两字典中有重复的key, 保留第二个字典key）
        :param varDict:
        :return:
        '''
        d_varMerge = {}
        for i in range(len(varDict)):
            d_varMerge.update(varDict[i])
        return d_varMerge

    # 2.3 获取2个字典交、并、对称差集的key
    def getKeyBySet(self, varOperator, varDict1, varDict2):
        # 提供  '&', '|' 和'^' ，即交、并、对称差集四种运算符。
        if varOperator == "&":
            return([k for k in varDict1.keys() & varDict2.keys()])
        elif varOperator == "|":
            return([k for k in varDict1.keys() | varDict2.keys()])
        elif varOperator == "-":
            return([k for k in varDict1.keys() - varDict2.keys()])
        elif varOperator == "^":
            return([k for k in varDict1.keys() ^ varDict2.keys()])
        else:
            return None

    # 2.4 获取2个字典交、并、对称差集的keyvalue
    def getKeyValueBySet(self, varOperator, varDict1, varDict2):
        if varOperator == "&":
            return list((varDict1.items() & varDict2.items()))
        elif varOperator == "|":
            return list((varDict1.items() | varDict2.items()))
        elif varOperator == "-":
            return list((varDict1.items() - varDict2.items()))
        elif varOperator == "^":
            return list((varDict1.items() ^ varDict2.items()))

        else:
            return None






    # 4.1 删除字典中的key
    def delKey(self, varDict, *varKey):
        list1 = []
        for i in range(len(varKey)):
            list1.append(varKey[i])
        remove = set(list1)
        return ({k: v for k, v in varDict.items() if k not in remove})
    # 4.2 保留字典中的key
    def reserveKey(self, varDict, *varKey):
        list1 = []
        for i in range(len(varKey)):
            list1.append(varKey[i])
        reserve = set(list1)
        print({k: v for k, v in varDict.items() if k in reserve})


    # 5.1 多个字典中相同的key值进行累加
    def sumValueByKey(self, *varDict):
        # print(Dict_PO.sumValueByKey({"a": 10000, "b": 1}, {"a": 10000, "b": 1},
        #                             {"a": 40000, "b": 1, "c": 333}))  # [('a', 60000), ('c', 333), ('b', 3)]

        counter = Counter()
        for i in range(len(varDict)):
            counter.update(varDict[i])
        return (counter.most_common())

    # 5.2 批量更新字典value（数字）
    def addValue(self, varDict, n):
        return ({k: v + n for k, v in varDict.items()})

    # 5.2 批量更新字典value（数字）
    def minusValue(self, varDict, n):
        return ({k: v - n for k, v in varDict.items()})


    # 6.1 按性别分组显示姓名
    def groupByValueShowName(self, varMoreDict, varGroupBy, varValue):

        '''
        按某个值进行分组
        :param varDict:
        :return:
        '''

        def group_by_value(accumulator, value):
            # print(accumulator)
            accumulator[value[varGroupBy]].append(value[varValue])
            return accumulator

        dict2 = {}
        for t in range(len(varTuple)):
            for k, v in varTuple[t].items():
                if k == varGroupBy:
                    dict2[varTuple[t][k]] = []

        return reduce(group_by_value, varMoreDict, dict2)

    # 6.2 按性别分组显示所有值
    def groupByValueShowAll(self, varMoreDict, varGroupBy):
        import itertools
        return {item[0]: list(item[1]) for item in itertools.groupby(varMoreDict, lambda x: x[varGroupBy])}


if __name__ == "__main__":

    Dict_PO = DictPO()

    # d1 = dict(a=1, b=2, test=123)
    # d2 = dict(a=100, b=200, dev=444)
    # d3 = dict(a=700, b=4, prd=666)
    # print("1.3 字典key转列表（去重）".center(100, "-"))
    # print(Dict_PO.dictKey2list(d1))  # ['a', 'b', 'test']
    # print(Dict_PO.dictKey2list(d1, d2))  # ['a', 'b', 'dev', 'test']
    # print(Dict_PO.dictKey2list(d1, d2, d3))  # ['a', 'b', 'prd', 'dev', 'test']
    #
    # print("2.1 合并字典（合并时如遇重复key,则保留第一个字典key的值）".center(100, "-"))
    # print(Dict_PO.mergeDictReserveLeft(d1, d2))  # {'a': 1, 'b': 2, 'dev': 444, 'test': 123}
    # print(Dict_PO.mergeDictReserveLeft(d1, d2, d3))  # {'a': 1, 'b': 2, 'prd': 666, 'dev': 444, 'test': 123}
    #
    # print("2.2 合并字典（合并时如遇重复key,则保留最后一个字典key的值）".center(100, "-"))
    # print(Dict_PO.mergeDictReserveRight(d1, d2, d3))  # {'a': 5, 'b': 6, 'jj': 123, 'hh': 666, 'kk': 999}
    # print({**d1, **d2})  # {'a': 100, 'b': 200, 'test': 123, 'dev': 444}
    # print({**d1, **d2, **d3})  # {'a': 700, 'b': 4, 'test': 123, 'dev': 444, 'prd': 666}
    # print({**d1, **d2, "a": 10})  # 先合并再修改，最后输出  {'a': 10, 'b': 200, 'test': 123, 'dev': 444}


    a = {'python': 1, 'java': 2, 'c': 3}
    b = {'python': 10, 'java': 2, 'c++': 88}
    print("2.3，获取2个字典交、并、对称差集的key".center(100, "-"))
    print(Dict_PO.getKeyBySet("&", a, b))  # ['python', 'java'] //交集
    print(Dict_PO.getKeyBySet("|", a, b))  # ['c', 'python', 'java', 'c++'] //并集
    print(Dict_PO.getKeyBySet("^", a, b))  # ['c', 'c++'] //对称差集

    print("2.4 获取2个字典交、并、对称差集的keyvalue".center(100, "-"))
    print(Dict_PO.getKeyValueBySet("&", a, b))  # [('java', 2)] //交集(key和value都必须相同)
    print(Dict_PO.getKeyValueBySet("|", a, b))  # [('c', 3), ('python', 1), ('python', 10), ('java', 2), ('c++', 88)] //并集
    print(Dict_PO.getKeyValueBySet("^", a, b))  # [('c', 3), ('python', 1), ('python', 10), ('c++', 88)]  //对称差集（去掉交集）

    print("2.6 获取2个字典差集的key".center(100, "-"))
    print(Dict_PO.getKeyBySet("-", a, b))  # 差集（在a不在b的key），['c']

    print("2.7 获取2个字典差集的keyvalue".center(100, "-"))
    print(Dict_PO.getKeyValueBySet("-", a, b))  # [('python', 1), ('c', 3)] //差集（去掉交集，剩下在a的的keyvalue)


    # # 字典形式
    # b = {'one': 1, 'two': 2, 'three': 3}
    # c = {'one': 1, 'two': 2, 'three': 3}
    #
    # a = dict(one=1, two=2, three=3)
    # b = {'one': 1, 'two': 2, 'three': 3}
    # c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
    # d = dict([('two', 2), ('one', 1), ('three', 3)])
    # e = dict({'three': 3, 'one': 1, 'two': 2})
    # print(a == b == c == d == e)
    #


    # print("4.1 删除字典中的key".center(100, "-"))
    # print(Dict_PO.delKey({"a": 5, "b": 6, "c": 7, "d": 8}, "b", "d"))  # {'a': 5, 'c': 7}
    #
    # print("4.2 保留字典中的key".center(100, "-"))
    # print(Dict_PO.reserveKey({"a": 5, "b": 6, "c":7, "d":8}, "b", "d"))  # {'b': 6, 'd': 8}
    #
    #
    # print("5.1 多个字典中相同的key值进行累加".center(100, "-"))
    # print(Dict_PO.sumValueByKey({"a": 10000, "b": 1}, {"a": 10000, "b": 1}, {"a": 40000, "b": 1, "c" : 333}))  # [('a', 60000), ('c', 333), ('b', 3)]
    #
    # print("5.2 字典的数字value加法".center(100, "-"))
    # print(Dict_PO.addValue({"a": 6, "b": 7, "c": 8, "d": 9}, 2))  # {'a': 7, 'b': 8, 'c': 9, 'd': 10}
    #
    # print("5.3 字典的数字value减法".center(100, "-"))
    # print(Dict_PO.minusValue({"a": 6, "b": 7, "c": 8, "d": 9}, 2))  # {'a': 7, 'b': 8, 'c': 9, 'd': 10}


    print("6.1 按性别分组显示姓名".center(100, "-"))
    varTuple = ({'name': 'jinhao', 'age': 105, 'gender': 'male'},
                {'name': 'baba', 'age': 76, 'gender': 'male'},
                {'name': 'mama', 'age': 202, 'gender': 'female'},
                {'name': 'yoyo', 'age': 84, 'gender': 'female'})
    print(Dict_PO.groupByValueShowName(varTuple, 'gender', 'name'))  # {'male': ['jinhao', 'baba'], 'female': ['mama', 'yoyo']}

    print("6.2 按性别分组显示所有值".center(100, "-"))
    print(Dict_PO.groupByValueShowAll(varTuple, 'gender'))  # {'male': [{'name': 'jinhao', 'age': 105, 'gender': 'male'}, {'name': 'baba', 'age': 76, 'gender': 'male'}], 'female': [{'name': 'mama', 'age': 202, 'gender': 'female'}, {'name': 'yoyo', 'age': 84, 'gender': 'female'}]}


    # counter = Counter()
    # # counter 可以统计 list 里面元素的频率
    # # counter.update(['a', 'b', 'a'])
    # # # print(counter)  # Counter({'a': 2, 'b': 1})
    # # print(counter.most_common())  # [('a', 2), ('b', 1)]
    # #
    # # # 合并计数
    # dd = {"a": 10000, "b": 1}
    # counter.update(dd)
    # ww = {"a": 10000, "c":444, "b": -1}
    # counter.update(ww)
    # # print(counter)  # Counter({'a': 10002, 'b': 2})
    # # counter["b"] += 100 # Counter({'a': 10002, 'b': 102})
    # print(counter.most_common())  # [('a', 10002), ('b', 102)]
    # # print(counter.most_common()[0])  # ('a', 10002)


    # print("6.1 collections中defaultdict之字典的 value 是字典".center(100, "-"))
    # dict1 = defaultdict(dict)
    # dict1[5]["a"] = 125
    # dict1[5]["b"] = 1
    # print(dict1[5])  # {'a': 125, 'b': 1}
    # print(dict1)  # defaultdict(<class 'dict'>, {5: {'a': 125, 'b': 1}})
    #
    # print("6.2 collections中defaultdict之字典的 value 是列表".center(100, "-"))
    # list1 = defaultdict(list)
    # list1[5].append(3)
    # list1[5].append("45")
    # print(list1[5])  # [3, '45']
    #
    # print("6.3 collections中defaultdict之字典的 value 是lambda".center(100, "-"))
    # a = defaultdict(lambda: 10)
    # print(a[3])  # 10
    # print(a[6]+1)  # 11
    # print(a)  # defaultdict(<function <lambda> at 0x000001F2D17F0550>, {3: 10, 6: 10})
    #
    # print("6.4 collections中defaultdict之字典的 value 里又是字典".center(100, "-"))
    # dict4 = defaultdict(lambda: defaultdict(dict))
    # dict4[5]["a"] = dict(b=123, c=666)
    # print(dict4[5])  # defaultdict(<class 'dict'>, {'a': '123'})
    # print(dict4[5]['a'])  # {'b': 123, 'c': 666}


    # print("7.1 字典转json字符串".center(100, "-"))
    # print(json.dumps(dict(a=5, b=6)))  # {"a": 5, "b": 6}  双引号是字符串
    #
    # print("7.2 json字符串转字典".center(100, "-"))
    # print(json.loads('{"a": 5, "b": 6}'))  # {'a': 5, 'b': 6}  单引号是字典
    #
    # print("7.3 字典转 JSON 字符串文件".center(100, "-"))
    # with open("dict.json", "w+") as f:
    #      json.dump(dict(a=5, b=6), f)
    #
    # print("7.4 将 JSON 文件转字典".center(100, "-"))
    # with open("dict.json", "r") as f:
    #     print(json.load(f))  # {'a': 5, 'b': 6}




