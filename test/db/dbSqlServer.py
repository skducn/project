# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2019-4-11
# Description: sqlserver , 显示表、字段、comment结构 ， common - db - dbSqlServer.py
# pymssql托管在Github上：https://github.com/pymssql
# 关于python 3 输出中文乱码，因为输出的是位串，而不是可读的字符串，需要对其进行转换 str(string[, encoding])对数组进行转换，如：str(OID2, 'utf-8')
# *****************************************************************

import pymssql

# server = "192.168.0.195"
# user = "DBuser"
# password = "qwer#@!"
# varDB = "bmlpimpro"

server = "192.168.0.35"
user = "test"
password = "123456"
varDB = "healthcontrol_test"

def dbDesc(*args):
    '''搜索表结构，表名区分大小写'''

    conn = pymssql.connect(server, user, password, varDB)
    cursor = conn.cursor()

    if len(args) == 0:
        # 查看所有表结构，获取数据库下有多少张表
        allTable = "select * from sysobjects where xtype = 'u' and name != 'sysdiagrams'"
        cursor.execute(allTable)
        allTable = cursor.fetchall()
        print("数据库<" + varDB + ">共有<"+ str(len(allTable)) +">张表")
        for tbl in allTable:
            # 遍历表
            sql = "SELECT A.name AS table_name,B.name AS column_name,C.value AS column_description,d.name AS colType FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'" % (
                tbl[0])
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                tblName = results[0][0]
                x = y = 0
                for i in results:
                    if len(i[1]) > x: x = len(i[1])
                    if len(i[3]) > y: y = len(i[3])
                print("字段" + " " * (x - 3), "类型" + " " * (y - 3), "注释" + " " * (x - 3),
                      (str(tblName) + " - " + str(len(results)) + "(fields)"), "\n" + "-" * 60)
                for row in results:
                    # 遍历字段、类型、comment
                    if row[2] != None:
                        print(row[1] + " " * (x - len(row[1]) + 1), row[3] + " " * (y - len(row[3]) + 1),
                              str(row[2], 'utf-8'))
                    else:
                        print(row[1] + " " * (x - len(row[1]) + 1), row[3] + " " * (y - len(row[3]) + 1),
                              row[2])
            except Exception as e:
                raise e
            finally:
                print("\n")
    elif len(args) == 1 :
        varTable = args[0]
        if "*" in varTable:
            # 模糊匹配多个表格的所有表结构，搜索XXX开头的表结构（通配符*）
            tblHead = varTable.split("*")[0]
            # 查看所有表结构，获取数据库下有多少张表
            allTable = "select * from sysobjects where xtype = 'u' and name != 'sysdiagrams'"
            cursor.execute(allTable)
            allTable = cursor.fetchall()
            tblCount = 0
            for tbl in allTable:
                if tblHead in tbl[0]:
                    tblCount += 1
            print("数据库<" + varDB + ">中<" + tblHead + ">开头的表共有<" + str(tblCount) + ">张")
            allTable = "select * from sysobjects where xtype = 'u' and name != 'sysdiagrams'"
            cursor.execute(allTable)
            allTable = cursor.fetchall()
            for tbl in allTable:
                # 遍历表
                if tblHead in tbl[0]:
                    sql = "SELECT A.name AS table_name,B.name AS column_name,C.value AS column_description,d.name AS colType FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'" % (
                        tbl[0])
                    try:
                        cursor.execute(sql)
                        results = cursor.fetchall()
                        tblName = results[0][0]
                        x = y = 0
                        for i in results:
                            if len(i[1]) > x: x = len(i[1])
                            if len(i[3]) > y: y = len(i[3])
                        print("字段" + " " * (x - 3), "类型" + " " * (y - 3), "注释" + " " * (x - 3),
                              (str(tblName) + " - " + str(len(results)) + "(fields)"), "\n" + "-" * 60)
                        for row in results:
                            # 遍历字段、类型、comment
                            if row[2] != None:
                                print(row[1] + " " * (x - len(row[1]) + 1), row[3] + " " * (y - len(row[3]) + 1),
                                      str(row[2], 'utf-8'))
                            else:
                                print(row[1] + " " * (x - len(row[1]) + 1), row[3] + " " * (y - len(row[3]) + 1),
                                      row[2])
                    except Exception as e:
                        raise e
                    finally:
                        print("\n")
        elif "*" not in varTable:
            # 单个表格的所有表结构
            sql= "SELECT A.name AS table_name,B.name AS column_name,C.value AS column_description,d.name AS colType FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'" % (varTable)
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                tblName = results[0][0]
                x = y = 0
                for i in results:
                    if len(i[1]) > x: x = len(i[1])
                    if len(i[3]) > y: y = len(i[3])
                print("字段" + " " * (x-3), "类型" + " " * (y-3), "注释"+ " " * (x-3), (str(tblName) + " - " + str(len(results)) + "(fields)"), "\n" + "-" * 60)
                for row in results:
                    # 遍历字段、类型、comment
                    if row[2] != None:
                        print(row[1] + " " * (x - len(row[1]) + 1), row[3] + " " * (y - len(row[3]) + 1), str(row[2], 'utf-8'))
                    else:
                        print(row[1] + " " * (x - len(row[1]) + 1), row[3] + " " * (y - len(row[3]) + 1), row[2])
            except Exception as e:
                print(e, ",很抱歉，您搜索的表<" + varTable + ">不存在！")
            finally:
                print("\n")
    elif len(args) == 2:
        # 查看单表或多表的可选字段表结构
        varTable = args[0]
        varFields = args[1]

        if "*" in varTable:
            # 模糊匹配多个表格可选字段表结构，搜索XXX开头的表结构（通配符*）
            tblHead = varTable.split("*")[0]
            # 查看所有表结构，获取数据库下有多少张表
            allTable = "select * from sysobjects where xtype = 'u' and name != 'sysdiagrams'"
            cursor.execute(allTable)
            allTable = cursor.fetchall()
            tblCount = 0
            for tbl in allTable:
                if tblHead in tbl[0]:
                    tblCount += 1
            print("数据库<" + varDB + ">中<" + tblHead + ">开头的表共有<" + str(tblCount) + ">张")
            allTable = "select * from sysobjects where xtype = 'u' and name != 'sysdiagrams'"
            cursor.execute(allTable)
            allTable = cursor.fetchall()
            for tbl in allTable:
                # 遍历表
                if tblHead in tbl[0]:
                    sql = "SELECT A.name AS table_name,B.name AS column_name,C.value AS column_description,d.name AS colType FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'" % (
                        tbl[0])
                    try:
                        cursor.execute(sql)
                        results = cursor.fetchall()
                        tblName = results[0][0]
                        x = y = 0
                        for i in results:
                            if len(i[1]) > x: x = len(i[1])
                            if len(i[3]) > y: y = len(i[3])
                        print("字段" + " " * (x - 3), "类型" + " " * (y - 3), "注释" + " " * (x - 3),
                              (str(tblName) + " - " + str(len(results)) + "(fields)"), "\n" + "-" * 60)
                        for row in results:
                            # 遍历字段、comment
                            if row[1] in varFields:
                                if row[2] != None:
                                    print(row[1] + " " * (x - len(row[1]) + 1), row[3] + " " * (y - len(row[3]) + 1),
                                          str(row[2], 'utf-8'))
                                else:
                                    print(row[1] + " " * (x - len(row[1]) + 1), row[3] + " " * (y - len(row[3]) + 1),
                                          row[2])
                    except Exception as e:
                        raise e
                    finally:
                        print("\n")
        elif "*" not in varTable:
            # 单个表格可选字段表结构
            sql = "SELECT A.name AS table_name,B.name AS column_name,C.value AS column_description,d.name AS colType FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'" % (
                varTable)
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                tblName = results[0][0]
                x = y = 0
                for i in results:
                    if len(i[1]) > x: x = len(i[1])
                    if len(i[3]) > y: y = len(i[3])
                print("字段" + " " * (x - 3), "类型" + " " * (y - 3), "注释" + " " * (x - 3),
                      (str(tblName) + " - " + str(len(results)) + "(fields)"), "\n" + "-" * 60)
                for row in results:
                    # 遍历字段、comment
                        if row[1] in varFields:
                            if row[2] != None:
                                print(row[1] + " " * (x - len(row[1]) + 1), row[3] + " " * (y - len(row[3]) + 1),
                                      str(row[2], 'utf-8'))
                            else:
                                print(row[1] + " " * (x - len(row[1]) + 1), row[3] + " " * (y - len(row[3]) + 1), row[2])
            except Exception as e:
                print(e, ",很抱歉，您搜索的表<" + varTable + ">不存在！")
            finally:
                print("\n")

    conn.close()

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
    conn = pymssql.connect(server, user, password, varDB)
    cur = conn.cursor()


    list0 = []
    list1 = []
    x = y = 0
    if varType in "double,timestamp,float,money,int,nchar,nvarchar,datetime":
        if "*" in varTable:
            # 遍历所有表
            cur.execute("SELECT NAME FROM SYSOBJECTS WHERE TYPE='U'")
            tbl = cur.fetchall()
            for b in range(len(tbl)):
                # 遍历所有的表 的 列名称、列类别、类注释
                varTable = tbl[b][0]
                cur.execute(
                    "select syscolumns.name,systypes.name from syscolumns,systypes where syscolumns.xusertype=systypes.xusertype and syscolumns.id=object_id('%s')" % (
                        varTable))
                tblFields = cur.fetchall()
                for i in tblFields:
                    if len(i[0]) > x: x = len(i[0])
                    if len(i[1]) > y: y = len(i[1])
                for j in tblFields:
                    if varType in j[1]:
                        list0.append(j[0])
                        list1.append(j[1])
                # print(varTable + " - " + str(list0))   # 遍历输出所有表与字段名
                for i in range(0, len(list0)):
                    cur.execute(
                        "select * from %s where convert(varchar, %s, 120) like '%s'" % (varTable, list0[i], varValue))
                    t4 = cur.fetchall()
                    if len(t4) != 0:
                        print("*" * 100)
                        print("search: " + varValue + " > " + varDB + "." + varTable + "(" ")." + list0[
                            i] + " > [" + str(len(t4)) + " 条记录]" + "\n")
                        for j in range(len(t4)):
                            print(t4[j])
                list0 = []
                list1 = []
        elif "*" not in varTable:
            # 获取列名称、列类别、类注释
            cur.execute("select syscolumns.name,systypes.name from syscolumns,systypes where syscolumns.xusertype=systypes.xusertype and syscolumns.id=object_id('%s')" % (varTable))
            tblFields = cur.fetchall()
            for i in tblFields:
                if len(i[0]) > x: x = len(i[0])
                if len(i[1]) > y: y = len(i[1])
            for j in tblFields:
                if varType in j[1]:
                    list0.append(j[0])
                    list1.append(j[1])
            for i in range(0, len(list0)):
                cur.execute("select * from %s where %s like '%s'" % (varTable, list0[i], varValue))
                t4 = cur.fetchall()
                if len(t4) != 0:
                    print("search: " + varValue + " > " + varDB + "." + varTable + "(" ")." + list0[
                        i] + " > [" + str(len(t4)) + " records]" + "\n" + "-" * 60)
                    for j in range(len(t4)):
                        print(list(t4[j]))
                    print()
            list0 = []
            list1 = []
    conn.close()

dbDesc()    # 或 dbDesc('*')
# dbDesc('QYYH')   # 搜索HrDic开头的表结构
# dbDesc('HrPersonBasicInfo')
# dbDesc('t_outpatient_registration_invoice')   # 搜索HrDicDisease表结构
# dbDesc('HrDicDisease', 'Type,Remark,Code')   # 搜索HrDicDisease表的Type\Remark\Code字段的结构
# dbDesc('HrDic*', 'Type')  # 搜索HrDic开头的表结构中Type字段的结构（通配符*）

# *****************************************************************

# dbRecord('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
# dbRecord('*', 'varchar', '%王静%')  # 模糊搜索所有表中带yoy的char类型。
# dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# dbRecord('*','datetime', '%2019-07-17 11:19:41%')  # 模糊搜索所有表中带2019-01的timestamp类型。

dbRecord('*', 'int', '%310102730812282%')  # 模糊搜索所有表中带yoy的char类型。