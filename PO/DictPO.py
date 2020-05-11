# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-4-21
# Description   : 字典对象层
# https://www.jb51.net/article/167029.htm
# https://www.cnblogs.com/it-tsz/p/10605021.html set集合
# *********************************************************************

from PO.MysqlPO import *

class DictPO():

    def __init__(self):
        pass

    # 1，将第二个字典合并到第一个字典中，如有重复key，只保留第一个字典的，同时可以去掉N个key
    def getKeyByIntersection(self, varDict1, varDict2):
        # # 获取两个字典交集key，放在字典里返回 # Return { 'x', 'y' }
        # # return(varDict1.keys() & varDict2.keys())
        # return(set(varDict1) & set(varDict2))
        #
        # # # Find keys in a that are not in b
        # # print(a.keys() - b.keys())  # Return { 'z' }
        # #
        # # print(b.keys() - a.keys())  # Return { 'w' }
        # #
        # # # Find (key,value) pairs in common
        # # print(a.items() & b.items())  # Return { ('y', 2) }
        # #
        # # 两个字典合并，去掉N个key
        c = {key: varDict1[key] for key in varDict2.keys() - {'w','x'}}
        # c = {key: a[key] for key in a.keys() - {'w', "z"}}
        return(c)
        # # {'y': 2, 'x': 1}


if __name__ == "__main__":

    Dict_PO = DictPO()

    # b = {'one': 1, 'two': 2, 'three': 3}
    # c = {'one': 1, 'two': 2, 'three': 3}
    #
    # a = dict(one=1, two=2, three=3)
    # b = {'one': 1, 'two': 2, 'three': 3}
    # c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
    # d = dict([('two', 2), ('one', 1), ('three', 3)])
    # e = dict({'three': 3, 'one': 1, 'two': 2})
    # print(a == b == c == d == e)

    a = {
        'x': 1,
        'y': 2,
        'z': 3
    }
    b = {
        'w': 10,
        'x': 11,
        'z': 2123
    }

    # a = [1,2,3,4,5]
    # b = [11,2,3,4,55]
    #
    # a = "12345"
    # b = "1234567"

    x = Dict_PO.getKeyByIntersection(a, b)
    print(x)
    print(type(x))
    print(len(x))


    #
    # # Find keys in common
    # print(a.keys() & b.keys())  # Return { 'x', 'y' }
    #
    # # Find keys in a that are not in b
    # print(a.keys() - b.keys())  # Return { 'z' }
    #
    # print(b.keys() - a.keys())  # Return { 'w' }
    #
    # # Find (key,value) pairs in common
    # print(a.items() & b.items())  # Return { ('y', 2) }



    # # 两个字典合并，去掉N个key
    # c = {key:a[key] for key in a.keys() - {'w'}}
    # c = {key:a[key] for key in a.keys() - {'w',"z"}}
    # print(c)
    # {'y': 2, 'x': 1}

    #
    varUpdateDate = '2020-03-22'
    Mysql_PO = MysqlPO("192.168.0.195", "root", "Zy123456", "bitest", 3306)

    # Mysql_PO.conn.cursor(MySQLdb.cursors.DictCursor)
    # Mysql_PO.cur.execute('select * from bi_outpatient_yard ')
    # Mysql_PO.cur.execute('SELECT deptName,antibioticRecipe from bi_dept_recipe_day WHERE statisticsDate ="2020-03-22" ORDER BY antibioticRecipe DESC limit 10')
    Mysql_PO.cur.execute('SELECT deptname,round(outPAccount,2)from bi_outpatient_dept where statisticsDate ="2020-03-22" ORDER BY outpaccount DESC LIMIT 15')
    tmpTuple = Mysql_PO.cur.fetchall()
    # desc = Mysql_PO.cur.description  # 获取单表的字段名信息
    # print(desc)
    print(tmpTuple)
    # print(Mysql_PO.cur.rowcount)  # 获取结果集的条数/

    dict1={}
    for k,v in tmpTuple:
        print(k)
        print(v)
        dict1[k]=v

    print(dict1)
    #
