# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2019-2-17
# Description: mysql数据库表结构、字段数、注释、搜索内容 框架。 common - db - dbMysql.py
# *****************************************************************
import MySQLdb
from time import sleep

varHost = "192.168.0.164"
varUser = 'sa'
varPasswd = 'qwert123!@#!'
varDB = 'pim'

conn = MySQLdb.connect(host=varHost, user=varUser, passwd=varPasswd, db=varDB, port=3306, use_unicode=True)
cur = conn.cursor();cur.execute('SET NAMES utf8;');conn.set_character_set('utf8');cur.execute('show tables')

def dbDesc(*args):

    ''' 查看数据库表结构（字段、类型、DDL）
    无参：查看所有表结构
    一个参数：表名或表头*，支持通配符*
    二个参数：字段名（区分大小写），指定查看的字段名，多个字段名用逗号分隔，不支持通配符*
    '''

    l_name = []; l_type = []; l_comment = []
    x = y = 0
    if len(args) == 0:
        # 查看所有表结构
        cur.execute('select TABLE_NAME,TABLE_COMMENT from information_schema.`TABLES` where table_schema="%s" ' % varDB)
        tblName = cur.fetchall()
        for k in range(len(tblName)):
            cur.execute(
                'select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (
                varDB, tblName[k][0]))
            tblFields = cur.fetchall()
            print("\n" + varDB + "." + tblName[k][0] + "(" + tblName[k][1] + ") > " + str(len(tblFields)) + "f" + "\n" + "-" * 60)
            for i in tblFields:
                # 字段与类型对齐
                if len(i[0]) > x: x = len(i[0])
                if len(i[1]) > y: y = len(i[1])
            for i in tblFields:
                l_name.append(i[0] + " " * (x - len(i[0]) + 1))
                l_type.append(i[1] + " " * (y - len(i[1]) + 1))
                l_comment.append(i[2].replace("\r\n", ",").replace("  ", ""))
            for i in range(len(tblFields)):
                print(l_name[i], l_type[i], l_comment[i])
            l_name = [];l_type = []; l_comment = []
    elif len(args) == 1 :
        # 查看单表或多表的所有表结构
        varTable = args[0]
        if "*" in varTable:
            # 多个表格的所有表结构
            varTable2 = varTable.split("*")[0] + "%"  # t_store_%
            cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name like "%s"' % (varDB,varTable2))
            tblCount = cur.fetchall()
            if len(tblCount) != 0:
                for p in range(len(tblCount)):
                    # 遍历N张表
                    varTable = tblCount[p][0]
                    n = cur.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (varDB,varTable))
                    if n == 1:
                        tblDDL = cur.fetchone()
                        cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (varDB,varTable))
                        tblFields = cur.fetchall()
                        print("\n" + varDB + "." + varTable + "(" + tblDDL[0] + ") > " + str(len(tblFields)) + "f" + "\n" + "-" * 60)
                        for i in tblFields:
                            if len(i[0]) > x: x = len(i[0])
                            if len(i[1]) > y: y = len(i[1])
                        for i in tblFields:
                            l_name.append(i[0] + " "*(x-len(i[0])+1))
                            l_type.append(i[1] + " "*(y-len(i[1])+1))
                            l_comment.append(i[2].replace("\r\n", ",").replace("  ", ""))
                        for i in range(len(tblFields)):
                            print(l_name[i], l_type[i], l_comment[i])
                    l_name = []; l_type = []; l_comment = []
            else: print("[errorrrrrrr , 数据库("+ varDB +")中没有找到 " + varTable.split("*")[0] + " 前缀的表!]")
        elif "*" not in varTable:
            # 单个表格的所有表结构
            n = cur.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (varDB,varTable))
            if n == 1:
                tblDDL = cur.fetchone()
                cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (varDB,varTable))
                tblFields = cur.fetchall()
                print("\n" + varDB + "." + varTable + "(" + tblDDL[0] + ") > " + str(len(tblFields)) + "f" + "\n" + "-" * 60)
                for i in tblFields:
                    # 字段与类型对齐
                    if len(i[0]) > x: x = len(i[0])
                    if len(i[1]) > y: y = len(i[1])
                for i in tblFields:
                    l_name.append(i[0] + " "*(x-len(i[0])+1))
                    l_type.append(i[1] + " "*(y-len(i[1])+1))
                    l_comment.append(i[2].replace("\r\n", ",").replace("  ", ""))
                for i in range(len(tblFields)):
                    print(l_name[i], l_type[i], l_comment[i])
            else:
                print("[errorrrrrrr , 数据库(" + varDB + ")中没有找到 " + varTable + "表!]")
    elif len(args) == 2:
        # 查看单表或多表的可选字段表结构
        varTable = args[0]
        varFields = args[1]
        if "*" in varTable:
            # 多个表格可选字段表结构
            varTable2 = varTable.split("*")[0] + "%"  # t_store_%
            cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" and table_name like "%s"' % (varDB,varTable2))
            tblCount = cur.fetchall()
            for p in range(len(tblCount)):
                #  遍历N张表
                varTable = tblCount[p][0]
                n = cur.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (varDB,varTable))
                if n != 0:
                    tblDDL = cur.fetchone()
                    cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (varDB,varTable))
                    tblFields = cur.fetchall()
                    print("\n" + varDB + "." + varTable + "(" + tblDDL[0] + ") > " + str(len(tblFields)) + "f" + "\n" + "-" * 60)
                    for i in tblFields :
                        if len(i[0]) > x: x = len(i[0])
                        if len(i[1]) > y: y = len(i[1])
                    for i in tblFields :
                        for j in range(len(varFields.split(","))):
                            if i[0] == varFields.split(",")[j]:
                                l_name.append(i[0] + " " * (x - len(i[0]) + 1))
                                l_type.append(i[1] + " " * (y - len(i[1]) + 1))
                                l_comment.append(i[2].replace("\r\n", ",").replace("  ", ""))
                    for i in range(len(varFields.split(","))):
                        try:
                            print(l_name[i], l_type[i], l_comment[i])
                        except:
                            print("[errorrrrrrr , (" + varFields + ")中部分字段不存在!]")
                    l_name = []; l_type = []; l_comment = []
                else:
                    print("[errorrrrrrr , 数据库("+ varDB +")中没有找到 " + varTable.split("*")[0] + " 前缀的表!]")
        elif "*" not in varTable:
            # 单个表格可选字段表结构
            n = cur.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (varDB,varTable))
            if n == 1:
                tblDDL = cur.fetchone()
                cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (varDB,varTable))
                tblFields = cur.fetchall()
                print("\n" + varDB + "." + varTable + "(" + tblDDL[0] + ") > " + str(len(tblFields)) + "f" + "\n" + "-" * 60)
                for i in tblFields:
                    if len(i[0]) > x: x = len(i[0])
                    if len(i[1]) > y: y = len(i[1])
                for i in tblFields:
                    for j in range(len(varFields.split(","))):
                        if i[0] == varFields.split(",")[j]:
                            l_name.append(i[0] + " "*(x-len(i[0])+1))
                            l_type.append(i[1] + " "*(y-len(i[1])+1))
                            l_comment.append(i[2].replace("\r\n", ",").replace("  ", ""))
                for i in range(len(varFields.split(","))):
                    try:
                        print(l_name[i], l_type[i], l_comment[i])
                    except:
                        print("[errorrrrrrr , (" + varFields + ")中部分字段不存在!]")
            else:
                print("[errorrrrrrr , 数据库(" + varDB + ")中没有找到 " + varTable + "表!]")
    else:
        print("[errorrrrrrr , 参数溢出！]")

def dbCreateDate(*args):

    '''查看表创建时间及区间
    无参：查看所有表的创建时间
    一个参数：表名
    二个参数：第一个是时间前后，如 before指定日期之前创建、after指定日期之后创建，第二个是日期
    '''

    if len(args) == 0:
        try:
            cur.execute('select table_name,create_time from information_schema.`TABLES` where table_schema="%s"' % (varDB))
            tbl = cur.fetchall()
            print("\n" + varDB + "下 " + str(len(tbl)) + " 张表的创建时间" + "\n" + "-"*60)
            for r in range(len(tbl)):
                print(str(tbl[r][1]) + " => " + tbl[r][0])
        except:
            print("[warning , 数据库为空!]")
    elif len(args) == 1:
        if "*" in args[0]:
            varTable = args[0].split("*")[0] + "%"  # t_store_%
            cur.execute('select table_name,create_time from information_schema.`TABLES` where table_schema="%s" and table_name like "%s" ' % (varDB, varTable))
            tbl = cur.fetchall()
            print("\n" + varDB + "." + args[0] + " 表的创建时间" + "\n" + "-"*60)
            for r in range(len(tbl)):
                print(str(tbl[r][1]) + " => " + tbl[r][0])
        else:
            try:
                cur.execute('select create_time from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (varDB, args[0]))
                tbl = cur.fetchone()
                print("\n" + varDB + "." + args[0] + " 表的创建时间" + "\n" + "-"*60)
                print(str(tbl[0]) + " => " + args[0])
            except:
                print("[errorrrrrrr , " + args[0] +  "表不存在!]")
    elif len(args) == 2:
        if args[0] == "after" or args[0] == ">":
            cur.execute('select table_name,create_time from information_schema.`TABLES` where table_schema="%s" and create_time>"%s"' % (varDB, args[1]))
            tbl = cur.fetchall()
            print("\n" + varDB + "下 " + str(len(tbl)) + " 张表在 " + str(args[1]) + " 之后被创建" + "\n" + "-"*60)
            for r in range(len(tbl)):
                print(str(tbl[r][1]) + " => " + tbl[r][0])
        elif args[0] == "before" or args[0] == "<":
            cur.execute('select table_name,create_time from information_schema.`TABLES` where table_schema="%s" and create_time<"%s"' % (varDB, args[1]))
            tbl = cur.fetchall()
            print("\n" + varDB + "下 " + str(len(tbl)) + " 张表在 " + str(args[1]) + " 之前被创建" + "\n" + "-"*60)
            for r in range(len(tbl)):
                print(str(tbl[r][1]) + " => " + (tbl[r][0]))
        else:
            print("[errorrrrrrr , 参数1必须是 after 或 before ]")
    else:
        print("[errorrrrrrr , 参数溢出！]")

def dbRecord(varTable, varType, varValue):

    '''
    # 搜索记录
    # 参数1：varTable = 表名（*表示所有的表）
    # 参数2：varType = 数据类型(char,int,double,timestamp)
    # 参数3：varValue = 值 (支持%模糊查询，如 %yy%)
    # dbRecord('myclass','char', 'yoyo')  # 报错？
    dbRecord('*','char', u'%yoy%')  # 模糊搜索所有表中带yoy的char类型。
    # dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
    # dbRecord('*','timestamp', u'%2019-01%')  # 模糊搜索所有表中带2019-01的timestamp类型。
    '''

    list0 = []
    list1 = []
    x = y = 0
    print()
    if varType in "int,char,double,timestamp":
        if "*" in varTable :
            # 遍历所有表
            tblCount = cur.execute('select table_name from information_schema.`TABLES` where table_schema="%s" ' % (varDB))
            if tblCount != 0:
                tbl = cur.fetchall()
                for b in range(tblCount):
                    # 遍历所有的表 de 列名称、列类别、类注释
                    varTable = tbl[b][0]
                    # 获取表的注释
                    cur.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (varDB,varTable))
                    tblDDL = cur.fetchone()
                    # 获取列名称、列类别、类注释
                    cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (varDB,varTable))
                    tblFields = cur.fetchall()
                    for i in tblFields:
                        if len(i[0]) > x: x = len(i[0])
                        if len(i[1]) > y: y = len(i[1])
                    for j in tblFields:
                        if varType in j[1]:
                            list0.append(j[0])
                            list1.append(j[1])
                    for i in range(0,len(list0)):
                        cur.execute('select * from %s where %s LIKE "%s"' % (varTable,list0[i],varValue))
                        t4 = cur.fetchall()
                        if len(t4) != 0:
                            print("search: " + varValue + " > " + varDB + "." + varTable + "(" + str(tblDDL[0]) + ")." + list0[i] + " > [" + str(len(t4)) + " records]" + "\n" + "-"*60)
                            for j in range(len(t4)):
                                print(list(t4[j]))
                            print()
                    list0 = []; list1 = []
            else: print("[errorrrrrrr , 数据库(" + varDB + ")中没有找到 " + varTable.split("*")[0] + " 前缀的表!]")
        elif "*" not in varTable:
            cur.execute('select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (varDB, varTable))
            tblDDL = cur.fetchone()
            # 获取列名称、列类别、类注释
            cur.execute('select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (varDB, varTable))
            tblFields = cur.fetchall()
            for i in tblFields:
                if len(i[0]) > x: x = len(i[0])
                if len(i[1]) > y: y = len(i[1])
            for j in tblFields:
                if varType in j[1]:
                    list0.append(j[0])
                    list1.append(j[1])
            for i in range(0, len(list0)):
                cur.execute('select * from %s where %s LIKE "%s"' % (varTable, list0[i], varValue))
                t4 = cur.fetchall()
                if len(t4) != 0:
                    print("search: " + varValue + " > " + varDB + "." + varTable + "(" + str(tblDDL[0]) + ")." + list0[
                        i] + " > [" + str(len(t4)) + " records]" + "\n" + "-" * 60)
                    for j in range(len(t4)):
                        print(list(t4[j]))
                    print()
            list0 = []
            list1 = []


# *****************************************************************

dbDesc()   # 查看所有表结构
# dbDesc('t_upms_user')   # 查看myclass表结构
# dbDesc('b*')  # 查看所有b开头的表结构（通配符*）
# dbDesc('book', 'id,page')   # 查看book表id,page字段的结构
# dbDesc('b*', 'id,page')  # 查看所有b开头的表中id字段的结构（通配符*）

# *****************************************************************

# dbCreateDate()   # 查看所有表的创建时间
# dbCreateDate('book')   # 查看book表创建时间
# dbCreateDate('b*')   # 查看所有b开头表的创建时间，通配符*
# dbCreateDate('after', '2019-02-18')  # 查看所有在2019-02-18之后创建的表
# dbCreateDate('>', '2019-02-18')  # 查看所有在2019-02-18之后创建的表
# dbCreateDate('before', "2019-12-08")  # 显示所有在2019-12-08之前创建的表
# dbCreateDate('<', "2019-02-18")  # 显示所有在2019-12-08之前创建的表

# *****************************************************************

# dbRecord('myclass','char', '%yoyo%')  # 搜索myclass表中内容包含yoyo的char类型记录。
# dbRecord('*','char', u'%yoyo%')  # 模糊搜索所有表中带yoy的char类型。
# dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# dbRecord('*','timestamp', u'%2019-01%')  # 模糊搜索所有表中带2019-01的timestamp类型。

