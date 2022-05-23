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

from collections import ChainMap

'''
1.1，字典合并（第一个字典重复的key不替换）
1.2，字典合并（重复key被第二个字典替换）

2.1，获取2个字典交、并、差和对称差集的key
2.2，获取2个字典交、并、差和对称差集的键值对
2.3， 两个字典合并，去掉N个key

3 将多个字典key（重复）转换列表（去重）


'''


class DictPO():


    def getMergeDictReserve(self, *varDict):
        '''
        # 1 字典合并（第一个字典重复的key不替换）
        # 多个字典合并，如有重复key，则保留第一个字典的key
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

    def getMergeDictReplace(self, *varDict):
        '''
        1.2，字典合并（重复key被第二个字典替换）
        :param varDict:
        :return:
        '''
        d_varMerge = {}
        for i in range(len(varDict)):
            d_varMerge.update(varDict[i])
        return d_varMerge


    # 2.1，获取2个字典交、并、差和对称差集的key
    def getKeyByDict(self, varOperator, varDict1, varDict2):
        # 提供  '&', '|', '-' 和'^' ，即交、并、差和对称差集四种运算符。
        if varOperator == "&":
            return(varDict1.keys() & varDict2.keys())
        elif varOperator == "|":
            return(varDict1.keys() | varDict2.keys())
        elif varOperator == "-":
            return(varDict1.keys() - varDict2.keys())
        elif varOperator == "^":
            return(varDict1.keys() ^ varDict2.keys())
        else:
            return None

    # 2.2，获取2个字典交、并、差和对称差集的键值对
    def getKeyValueByDict(self, varOperator, varDict1, varDict2):
        if varOperator == "&":
            return(varDict1.items() & varDict2.items())
        elif varOperator == "|":
            return(varDict1.items() | varDict2.items())
        elif varOperator == "-":
            return(varDict1.items() - varDict2.items())
        elif varOperator == "^":
            return(varDict1.items() ^ varDict2.items())
        else:
            return None

    # 2.3， 两个字典合并，去掉N个key
    def getMergeDictDelKey(self, varOperator, varDict1, varDict2):
        pass
        # # 两个字典合并，去掉N个key
        # c = {key: varDict1[key] for key in varDict2.keys() - {'w','x'}}
        # c = {key: varDict1[key] for key in varDict2.keys()}
        # c = {key: a[key] for key in a.keys() - {'w', "z"}}
        # return(c)
        # # {'y': 2, 'x': 1}

    def test(self):
        pass
        # b = {'one': 1, 'two': 2, 'three': 3}
        # c = {'one': 1, 'two': 2, 'three': 3}
        #
        # a = dict(one=1, two=2, three=3)
        # b = {'one': 1, 'two': 2, 'three': 3}
        # c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
        # d = dict([('two', 2), ('one', 1), ('three', 3)])
        # e = dict({'three': 3, 'one': 1, 'two': 2})
        # print(a == b == c == d == e)

    def getKey2list(self, *varDict):
        '''
        3 将多个字典key（重复）转换列表（去重）
        :return:
        '''
        if len(varDict) == 1:
            return list(ChainMap(varDict[0]))
        elif len(varDict) == 2:
            return list(ChainMap(varDict[0], varDict[1]))
        elif len(varDict) == 3:
            return list(ChainMap(varDict[0], varDict[1], varDict[2]))



if __name__ == "__main__":

    Dict_PO = DictPO()

    d1 = {'a': 1, 'b': 2, "jj":123}
    d2 = {'a': 3, 'b': 4, "hh":666}
    d3 = {'a': 5, 'bb': 6, "hh":999}


    # print("1.1，字典合并（重复key不替换）".center(100, "-"))
    print(Dict_PO.getMergeDictReserve(d1, d2))  # {'c': 3, 'd': 4, 'a': 1, 'b': 2}
    print(Dict_PO.getMergeDictReserve(d1, d2, d3))  # {'c': 3, 'd': 4, 'a': 1, 'b': 2}
    #
    #
    # print("1.2，字典合并（重复key被后者替换）".center(100, "-"))
    # # print(Dict_PO.getMergeDictReplace(d1, d2, d3))  # {'a': 5, 'b': 6, 'jj': 123, 'hh': 666, 'kk': 999}



    # a = {'x': 1, 'y': 2, 'z': 3}
    # b = {'w': 10, 'x': 1, 'z': 88}
    # c = {'x1': 1, 'y1': 2, 'z1': 3}
    #
    # print("2.1，获取2个字典交、并、差和对称差集的key".center(100, "-"))
    # print(Dict_PO.getKeyByDict("&", a, b))  # 交集，{'x', 'z'}
    # print(Dict_PO.getKeyByDict("|", a, b))  # 并集，{'w', 'x', 'z', 'y'}
    # print(Dict_PO.getKeyByDict("-", a, b))  # 差集（在a不在b的key），{'y'}
    # print(Dict_PO.getKeyByDict("^", a, b))  # 对称差集（不会同时出现在二者中），{'w', 'y'}
    #
    # print("2.2，获取2个字典差集的key".center(100, "-"))
    # print(Dict_PO.getKeyValueByDict("&", a, b))  # 交集(key和value都必须相同)，{('x', 1)}
    # print(Dict_PO.getKeyValueByDict("|", a, b))  # 并集，{('z', 88), ('y', 2), ('z', 3), ('w', 10), ('x', 1)}
    # print(Dict_PO.getKeyValueByDict("-", a, b))  # 差集（去掉交集，剩下在a的的keyvalue），{('z', 3), ('y', 2)}
    # print(Dict_PO.getKeyValueByDict("^", a, b))  # 对称差集（不会同时出现在二者中的keyvalue），{('z', 88), ('y', 2), ('z', 3), ('w', 10)}

    # print("3 将多个字典key（重复）转换列表（去重）".center(100, "-"))
    # print(Dict_PO.getKey2list(d1))  # ['a', 'b', 'jj']
    # print(Dict_PO.getKey2list(d1, d2))  # ['a', 'b', 'hh', 'jj']
    # print(Dict_PO.getKey2list(d1, d2, d3))  # ['a', 'bb', 'hh', 'b', 'jj']