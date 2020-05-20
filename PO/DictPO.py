# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-4-21
# Description   : 字典对象层
# https://www.jb51.net/article/167029.htm
# https://www.cnblogs.com/it-tsz/p/10605021.html set集合
# *********************************************************************
from collections import ChainMap

from PO.MysqlPO import *

class DictPO():

    def __init__(self):
        pass

    # 1.1，获取2个字典交、并、差和对称差集的key
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


    # 1.2，获取2个字典交、并、差和对称差集的键值对
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


     # 1.3， 两个字典合并，去掉N个key
    def getMergeDictDelKey(self, varOperator, varDict1, varDict2):
        pass
        # # 两个字典合并，去掉N个key
        # c = {key: varDict1[key] for key in varDict2.keys() - {'w','x'}}
        # c = {key: varDict1[key] for key in varDict2.keys()}
        # c = {key: a[key] for key in a.keys() - {'w', "z"}}
        # return(c)
        # # {'y': 2, 'x': 1}

    # 2，将2个字典合并成一个字典
    def getMergeDict2(self,varDict1, varDict2):
        # 如2个字典有重复key，则字典从左到右，只保留第一个字典的key。
        tmpDict = {}
        c = ChainMap(varDict1, varDict2)
        for k, v in c.items():
            tmpDict[k] = v
        return (tmpDict)

    # 3，将3个字典合并成一个字典
    def getMergeDict3(self, varDict1, varDict2, varDict3):
        # 如多个字典有重复key，则字典从左到右，只保留第一个字典的key。
        tmpDict = {}
        c = ChainMap(varDict1, varDict2, varDict3)
        for k, v in c.items():
            tmpDict[k] = v
        return (tmpDict)



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

if __name__ == "__main__":

    Dict_PO = DictPO()

    a = {'x': 1, 'y': 2, 'z': 3}
    b = {'w': 10, 'x': 1, 'z': 88}
    c = {'x1': 1, 'y1': 2, 'z1': 3}

    print("1.1，获取2个字典交、并、差和对称差集的key".center(100, "-"))
    print(Dict_PO.getKeyByDict("&", a, b))  # 交集，{'x', 'z'}
    print(Dict_PO.getKeyByDict("|", a, b))  # 并集，{'w', 'x', 'z', 'y'}
    print(Dict_PO.getKeyByDict("-", a, b))  # 差集（在a不在b的key），{'y'}
    print(Dict_PO.getKeyByDict("^", a, b))  # 对称差集（不会同时出现在二者中），{'w', 'y'}

    print("1.2，获取2个字典差集的key".center(100, "-"))
    print(Dict_PO.getKeyValueByDict("&", a, b))  # 交集(key和value都必须相同)，{('x', 1)}
    print(Dict_PO.getKeyValueByDict("|", a, b))  # 并集，{('z', 88), ('y', 2), ('z', 3), ('w', 10), ('x', 1)}
    print(Dict_PO.getKeyValueByDict("-", a, b))  # 差集（去掉交集，剩下在a的的keyvalue），{('z', 3), ('y', 2)}
    print(Dict_PO.getKeyValueByDict("^", a, b))  # 对称差集（不会同时出现在二者中的keyvalue），{('z', 88), ('y', 2), ('z', 3), ('w', 10)}

    d1 = {'a': 1, 'b': 2}
    d2 = {'c': 3, 'd': 4}
    d3 = {'b': 5, 'c': 6, "z":88}

    print("2，将2个字典合并成一个字典".center(100, "-"))
    print(Dict_PO.getMergeDict2(d1, d2))  # {'c': 3, 'd': 4, 'a': 1, 'b': 2}

    print("3，将3个字典合并成一个字典".center(100, "-"))
    print(Dict_PO.getMergeDict3(d1, d2, d3))  # {'b': 2, 'c': 3, 'z': 88, 'd': 4, 'a': 1}




    # varUpdateDate = '2020-03-22'
    # Mysql_PO = MysqlPO("192.168.0.195", "root", "Zy123456", "bitest", 3306)
    #
    # # Mysql_PO.conn.cursor(MySQLdb.cursors.DictCursor)
    # # Mysql_PO.cur.execute('select * from bi_outpatient_yard ')
    # # Mysql_PO.cur.execute('SELECT deptName,antibioticRecipe from bi_dept_recipe_day WHERE statisticsDate ="2020-03-22" ORDER BY antibioticRecipe DESC limit 10')
    # Mysql_PO.cur.execute('SELECT deptname,round(outPAccount,2)from bi_outpatient_dept where statisticsDate ="2020-03-22" ORDER BY outpaccount DESC LIMIT 15')
    # tmpTuple = Mysql_PO.cur.fetchall()
    # # desc = Mysql_PO.cur.description  # 获取单表的字段名信息
    # # print(desc)
    # print(tmpTuple)
    # # print(Mysql_PO.cur.rowcount)  # 获取结果集的条数/
    #
    # dict1={}
    # for k,v in tmpTuple:
    #     print(k)
    #     print(v)
    #     dict1[k]=v
    # print(dict1)
    #
