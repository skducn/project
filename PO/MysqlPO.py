# -*- coding: utf-8 -*-
#***************************************************************
# Author     : John
# Revise on : 2019-04-16
# Description: MysqlPO对象层
# pip3 install mysqlclient  (MySQLdb)
# pip3 install pymysql
# 问1：数据库中乱码显示问题，查询后却显示中文？
# 解答1：设置 charset 编码，如 self.conn = MySQLdb.connect(host=self.varHost, user=self.varUser, passwd=self.varPassword, db=self.varDB, port=self.varPort, use_unicode=True, charset='utf8') ，注意：charset 应该与数据库编码一致，如数据库是gb2312 ,则 charset='gb2312'。
# None是一个对象，而NULL是一个类型。
# Python中没有NULL，只有None，None有自己的特殊类型NoneType
# None不等于0、任何空字符串、False等。
# 在Python中，None、False、0、""(空字符串)、[](空列表)、()(空元组)、{}(空字典)都相当于False
#***************************************************************

'''
pandas引擎（pymysql）  getPymysqlEngine()
pandas引擎（mysqldb）  getMysqldbEngine()

1，查看数据库表结构（字段、类型、大小、可空、注释），注意，表名区分大小写 dbDesc()
2，搜索表记录 dbRecord('*', 'money', '%34.5%')
3，查询创建时间 dbCreateDate()

4.1，数据库表导出excel db2xlsx()
4.2，数据库表导出html db2html()
4.3，数据库表导出csv db2csv()
4.4 excel导入数据库表 xlsx2db()

5 将所有表结构导出到excel(覆盖)  dbDesc2xlsx（）

'''

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from PO.ExcelPO import *
import pandas as pd
from sqlalchemy import create_engine
from PO.OpenpyxlPO import *
from PO.NewexcelPO import *


class MysqlPO():

    # def __init__(self, varHost, varUser, varPassword, varDB, varPort=3336):
    #
    #
    #     self.conn = MySQLdb.connect(host=varHost, user=varUser, passwd=varPassword, db=varDB, port=int(varPort), use_unicode=True)
    #     self.cur = self.conn.cursor()
    #     self.cur.execute('SET NAMES utf8;')
    #     # self.conn.set_character_set('utf8')
    #     self.cur.execute('show tables')


    def __init__(self, varHost, varUser, varPassword, varDB, varPort=3336):
        self.varHost = varHost
        self.varUser = varUser
        self.varPassword = varPassword
        self.varDB = varDB
        self.varPort = int(varPort)

    def __GetConnect(self):
        # 得到数据库连接信息，返回conn.cursor()
        if not self.varDB:
            raise (NameError, "没有设置数据库信息")
        self.conn = MySQLdb.connect(host=self.varHost, user=self.varUser, passwd=self.varPassword, db=self.varDB, port=int(self.varPort), use_unicode=True)
        self.cur = self.conn.cursor()  # 创建一个游标对象
        if not self.cur:
            raise (NameError, "连接数据库失败")  # 将DBC信息赋值给cur
        else:
            return self.cur

    def execQuery(self, sql):

        ''' 执行查询语句
        返回一个包含tuple的list，list是元素的记录行，tuple记录每行的字段数值
        '''

        cur = self.__GetConnect()
        self.conn.commit()  # 新增后需要马上查询的话，则先commit一下。
        cur.execute(sql)

        try:
            result = cur.fetchall()
        except:
            self.conn.commit()
            cur.close()
            self.conn.close()
            return
        self.conn.commit()
        cur.close()
        self.conn.close()
        return result


    def getPymysqlEngine(self):
        # pandas引擎（pymysql）
        return create_engine('mysql+pymysql://' + self.varUser + ":" + self.varPassword + "@" + self.varHost + ":" + str(self.varPort) + "/" + self.varDB)

    def getMysqldbEngine(self):
        # pandas引擎（mysqldb）
        return create_engine('mysql+mysqldb://' + self.varUser + ":" + self.varPassword + "@" + self.varHost + ":" + str(self.varPort) + "/" + self.varDB)


    def dbDesc(self, *args):
        ''' 查看数据库表结构（字段、类型、DDL）
        第1个参数：表名或表头*（通配符*）
        第2个参数：字段名（区分大小写），指定查看的字段名，多个字段名用逗号分隔，不支持通配符*
        '''

        l_name = []
        l_type = []
        l_isnull = []
        l_comment = []
        l_isKey = []
        l_extra = []
        a=b=c=d=e= 0
        x = y = z = 0
        if len(args) == 0:
            # 查看所有表结构
            self.cur.execute('select TABLE_NAME,TABLE_COMMENT from information_schema.`TABLES` where table_schema="%s" ' % self.varDB)
            tblName = self.cur.fetchall()
            for k in range(len(tblName)):
                self.cur.execute('select column_name,column_comment,column_type,column_key,is_nullable from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (self.varDB, tblName[k][0]))

                # self.cur.execute('select column_name,column_type,is_nullable,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (self.varDB, tblName[k][0]))
                tblFields = self.cur.fetchall()
                # print(u"\033[1;34;40m", 'printGreen', "\n" + "*" * 50 + " " + tblName[k][0] + "(" + tblName[k][1] + " ) > " + str(len(tblFields)) + "个字段 " + "*" * 50 )
                a = b = c = d = e = 0
                for i in tblFields:
                    # 字段与类型对齐
                    if len(i[0]) > a: a = len(i[0])

                    if len(i[2]) > c: c = len(i[2])
                    if len(i[3]) > d: d = len(i[3])
                    if len(i[4]) > e: e = len(i[4])
                    if len(i[1].replace("\r\n", ",").replace("  ", "")) > b: b = len(i[1])

                print("-" * 100 + "\n" + tblName[k][0] + " ( " + tblName[k][1] + " ) - " + str(len(tblFields)) + "个字段 " +
                      "\n字段名" + " " * (a - 5),
                      "类型" + " " * (c-3),
                      "主键" + " " * (d-3),
                      "是否为空"+ " " * (e),
                      "字段说明")
                for i in tblFields:
                    l_name.append(i[0] + " " * (a - len(i[0]) + 1))
                    l_type.append(i[2] + " " * (c - len(i[2]) + 1))
                    l_isKey.append(i[3] + " " * (d - len(i[3]) + 1))
                    l_isnull.append(i[4] + " " * (e - len(i[4]) + 8))
                    l_comment.append(i[1] + " " * (b - len(i[1])))

                for i in range(len(tblFields)):
                    print(l_name[i], l_type[i], l_isKey[i], l_isnull[i], l_comment[i])
                l_name = []
                l_comment = []
                l_type = []
                l_isKey = []
                l_isnull = []



        elif len(args) == 1:
            # 查看单表或多表的所有表结构
            varTable = args[0]
            if "*" in varTable:
                # 多个表格的所有表结构
                varTable2 = varTable.split("*")[0] + "%"  # t_store_%
                self.cur.execute(
                    'select table_name from information_schema.`TABLES` where table_schema="%s" and table_name like "%s"' % (
                    self.varDB, varTable2))
                tblCount = self.cur.fetchall()
                if len(tblCount) != 0:
                    for p in range(len(tblCount)):
                        # 遍历N张表
                        varTable = tblCount[p][0]
                        n = self.cur.execute(
                            'select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (
                            self.varDB, varTable))
                        if n == 1:
                            tblDDL = self.cur.fetchone()
                            self.cur.execute('select column_name,column_type,is_nullable,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (self.varDB, varTable))
                            tblFields = self.cur.fetchall()

                            for i in tblFields:
                                # 字段与类型对齐
                                if len(i[0]) > x: x = len(i[0])
                                if len(i[1]) > y: y = len(i[1])
                                if len(i[2]) > z: z = len(i[2])
                            print("-" * 100 + "\n" + varTable + "(" + tblDDL[0] + ") - " + str(
                                len(tblFields)) + "个字段 " + "\n字段" + " " * (x - 3), "类型" + " " * (y - 3), "可空" + " " * 4,
                                  "注释")
                            for i in tblFields:
                                l_name.append(i[0] + " " * (x - len(i[0]) + 1))
                                l_type.append(i[1] + " " * (y - len(i[1]) + 1))
                                l_isnull.append(i[2] + " " * (z - len(i[2]) + 5))
                                l_comment.append(i[3].replace("\r\n", ",").replace("  ", ""))
                            for i in range(len(tblFields)):
                                print(l_name[i], l_type[i], l_isnull[i], l_comment[i])
                        l_name = []
                        l_type = []
                        l_comment = []
                        l_isnull = []
                else:
                    print("[errorrrrrrr , 数据库" + self.varDB + " 中没有找到 " + varTable.split("*")[0] + " 前缀的表!]")
            elif "*" not in varTable:
                # 单个表格的所有表结构
                n = self.cur.execute(
                    'select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (
                    self.varDB, varTable))
                if n == 1:
                    tblDDL = self.cur.fetchone()
                    self.cur.execute('select column_name,column_type,is_nullable,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (self.varDB, varTable))
                    tblFields = self.cur.fetchall()
                    for i in tblFields:
                        # 字段与类型对齐
                        if len(i[0]) > x: x = len(i[0])
                        if len(i[1]) > y: y = len(i[1])
                        if len(i[2]) > z: z = len(i[2])
                    print("-" * 100 + "\n" + varTable + "(" + tblDDL[0] + ") - " + str(
                        len(tblFields)) + "个字段 " + "\n字段" + " " * (x - 3), "类型" + " " * (y - 3), "可空" + " " * 4,
                          "注释")
                    for i in tblFields:
                        l_name.append(i[0] + " " * (x - len(i[0]) + 1))
                        l_type.append(i[1] + " " * (y - len(i[1]) + 1))
                        l_isnull.append(i[2] + " " * (z - len(i[2]) + 5))
                        l_comment.append(i[3].replace("\r\n", ",").replace("  ", ""))
                    for i in range(len(tblFields)):
                        print(l_name[i], l_type[i], l_isnull[i], l_comment[i])

                else:
                    print("[errorrrrrrr , 数据库" + self.varDB + " 中没有找到 " + varTable + " 表!]")
        elif len(args) > 1:
            # 查看单表或多表的可选字段表结构
            varTable = args[0]
            varFields = args[1]
            if "*" in varTable:
                # 多个表格可选字段表结构
                varTable2 = varTable.split("*")[0] + "%"  # t_store_%
                self.cur.execute(
                    'select table_name from information_schema.`TABLES` where table_schema="%s" and table_name like "%s"' % (
                    self.varDB, varTable2))
                tblCount = self.cur.fetchall()
                for p in range(len(tblCount)):
                    #  遍历N张表
                    varTable = tblCount[p][0]
                    n = self.cur.execute(
                        'select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (
                        self.varDB, varTable))
                    if n != 0:
                        tblDDL = self.cur.fetchone()
                        self.cur.execute(
                            'select column_name,column_type,is_nullable,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (
                            self.varDB, varTable))
                        tblFields = self.cur.fetchall()

                        for i in tblFields:
                            # 字段与类型对齐
                            if len(i[0]) > x: x = len(i[0])
                            if len(i[1]) > y: y = len(i[1])
                            if len(i[2]) > z: z = len(i[2])
                        # print("*" * 100 + "\n" + varTable + "(" + tblDDL[0] + ") - " + str(
                        #     len(tblFields)) + "个字段 " + "\n字段" + " " * (x - 3), "类型" + " " * (y - 3), "可空" + " " * 4,
                        #       "注释")
                        for i in tblFields:
                            l_name.append(i[0] + " " * (x - len(i[0]) + 1))
                            l_type.append(i[1] + " " * (y - len(i[1]) + 1))
                            l_isnull.append(i[2] + " " * (z - len(i[2]) + 6))
                            l_comment.append(i[3].replace("\r\n", ","))

                        varTmp = 0
                        for i in range(len(args) - 1):
                                for j in range(len(l_name)):
                                    if str(l_name[j]).strip() == args[i + 1]:
                                        varTmp = 1
                        if varTmp == 1:
                            print("-" * 100 + "\n" + varTable + "(" + tblDDL[0] + ") - " + str(
                                len(tblFields)) + "个字段 " + "\n字段" + " " * (x - 3), "类型" + " " * (y - 3), "可空" + " " * 5, "注释")
                        for i in range(len(args) - 1):
                            try:
                                for j in range(len(l_name)):
                                    if str(l_name[j]).strip() == args[i + 1]:
                                        print(l_name[j], l_type[j], l_isnull[j], l_comment[j])
                            except:
                                print("[errorrrrrrr , (" + varFields + ")中部分字段不存在!]")
                        l_name = []
                        l_type = []
                        l_comment = []
                        l_isnull = []
                    else:
                        print("[errorrrrrrr , 数据库(" + self.varDB + ")中没有找到 " + varTable.split("*")[0] + " 前缀的表!]")
            elif "*" not in varTable:
                # 单个表格可选字段表结构
                n = self.cur.execute(
                    'select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (
                    self.varDB, varTable))
                if n == 1:
                    tblDDL = self.cur.fetchone()
                    self.cur.execute(
                        'select column_name,column_type,is_nullable,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (
                        self.varDB, varTable))

                    tblFields = self.cur.fetchall()
                    for i in tblFields:
                        # 字段与类型对齐
                        if len(i[0]) > x: x = len(i[0])
                        if len(i[1]) > y: y = len(i[1])
                        if len(i[2]) > z: z = len(i[2])
                    print("-" * 100 + "\n" + varTable + "(" + tblDDL[0] + ") - " + str(
                        len(tblFields)) + "个字段 " + "\n字段" + " " * (x - 3), "类型" + " " * (y - 3), "可空" + " " * 4,
                          "注释")
                    for i in tblFields:
                        l_name.append(i[0] + " " * (x - len(i[0]) + 1))
                        l_type.append(i[1] + " " * (y - len(i[1]) + 1))
                        l_isnull.append(i[2] + " " * (z - len(i[2]) + 5))
                        l_comment.append(i[3].replace("\r\n", ",").replace("  ", ""))
                    for i in range(len(args)-1):
                        try:
                            for j in range(len(l_name)):
                                if str(l_name[j]).strip() == args[i+1]:
                                    print(l_name[j], l_type[j], l_isnull[j], l_comment[j])
                        except:
                            print("[errorrrrrrr , (" + varFields + ")中部分字段不存在!]")
                else:
                    print("[errorrrrrrr , 数据库(" + self.varDB + ")中没有找到 " + varTable + "表!]")

    def dbRecord(self, varTable, varType, varValue):
        '''
        # 搜索表记录
        # 参数1：varTable = 表名（*表示所有的表）
        # 参数2：varType = 数据类型(char,int,double,timestamp)
        # 参数3：varValue = 值 (支持%模糊查询，如 %yy%)
        '''
        # dbRecord('myclass','char', 'yoyo')  # 报错？
        # dbRecord('*','char', u'%yoy%')  # 模糊搜索所有表中带yoy的char类型。
        # dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
        # dbRecord('*','timestamp', u'%2019-01%')  # 模糊搜索所有表中带2019-01的timestamp类型。
        list0 = []
        list1 = []
        x = y = 0
        if varType in "float,money,int,nchar,nvarchar,datetime,timestamp":
            if "*" in varTable:
                # 遍历所有表
                tblCount = self.cur.execute(
                    'select table_name from information_schema.`TABLES` where table_schema="%s" ' % (self.varDB))
                if tblCount != 0:
                    tbl = self.cur.fetchall()
                    for b in range(tblCount):
                        # 遍历所有的表 de 列名称、列类别、类注释
                        varTable = tbl[b][0]
                        # 获取表的注释
                        self.cur.execute(
                            'select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (
                            self.varDB, varTable))
                        tblDDL = self.cur.fetchone()
                        # 获取列名称、列类别、类注释
                        self.cur.execute(
                            'select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (
                            self.varDB, varTable))
                        tblFields = self.cur.fetchall()
                        for i in tblFields:
                            if len(i[0]) > x: x = len(i[0])
                            if len(i[1]) > y: y = len(i[1])
                        for j in tblFields:
                            if varType in j[1]:
                                list0.append(j[0])
                                list1.append(j[1])
                        for i in range(0, len(list0)):
                            # print(list0[i]) 过滤系统关键字
                            if list0[i] not in 'desc,limit,key,group,usage':
                                self.cur.execute('select * from `%s` where %s LIKE "%s" ' % (varTable, list0[i], str(varValue)))
                                t4 = self.cur.fetchall()
                                if len(t4) != 0:
                                    print("- -" * 50)
                                    print("[search = " + varValue + "] , [result = " + str(len(t4)) + "] , [location = " + self.varDB + "." + varTable + "(" + str(tblDDL[0]) + ")." + list0[i] + "]\n")
                                    for j in range(len(t4)):
                                        print(list(t4[j]))
                                    print()
                        list0 = [];
                        list1 = []
                else:
                    print("[errorrrrrrr , 数据库(" + self.varDB + ")中没有找到 " + varTable.split("*")[0] + " 前缀的表!]")
            elif "*" not in varTable:
                self.cur.execute(
                    'select table_comment from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (
                    self.varDB, varTable))
                tblDDL = self.cur.fetchone()
                # 获取列名称、列类别、类注释
                self.cur.execute(
                    'select column_name,column_type,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (
                    self.varDB, varTable))
                tblFields = self.cur.fetchall()
                for i in tblFields:
                    if len(i[0]) > x: x = len(i[0])
                    if len(i[1]) > y: y = len(i[1])
                for j in tblFields:
                    if varType in j[1]:
                        list0.append(j[0])
                        list1.append(j[1])
                for i in range(0, len(list0)):
                    if list0[i] not in 'desc,limit,key':
                        self.cur.execute('select * from %s where %s LIKE "%s"' % (varTable, list0[i], varValue))
                        t4 = self.cur.fetchall()
                        if len(t4) != 0:
                            print("- -" * 50)
                            print("[search = " + varValue + "] , [result = " + str(len(t4)) + "] , [location = " + self.varDB + "." + varTable + "(" + str(tblDDL[0]) + ")." + list0[i] + "]\n")
                            for j in range(len(t4)):
                                print(list(t4[j]))
                list0 = []
                list1 = []

    def dbCreateDate(self, *args):

        '''
        查表的创建时间及区间
        无参：查看所有表的创建时间
        一个参数：表名
        二个参数：第一个是时间前后，如 before指定日期之前创建、after指定日期之后创建，第二个是日期
        '''
        # Mysql_PO.dbCreateDate()   # 查看所有表的创建时间
        # Mysql_PO.dbCreateDate('app_code')   # 查看book表创建时间
        # Mysql_PO.dbCreateDate('fact*')   # 查看所有b开头表的创建时间，通配符*
        # Mysql_PO.dbCreateDate('after', '2019-02-18')  # 查看所有在2019-02-18之后创建的表
        # Mysql_PO.dbCreateDate('>', '2019-02-18')  # 查看所有在2019-02-18之后创建的表
        # Mysql_PO.dbCreateDate('before', "2019-04-10")  # 显示所有在2019-12-08之前创建的表
        # Mysql_PO.dbCreateDate('<', "2019-02-18")  # 显示所有在2019-12-08之前创建的表
        if len(args) == 0:
            try:
                self.cur.execute(
                    'select table_name,create_time from information_schema.`TABLES` where table_schema="%s"' % (self.varDB))
                tbl = self.cur.fetchall()
                print("\n" + self.varDB + "下 " + str(len(tbl)) + " 张表的创建时间" + "\n" + "-" * 60)
                for r in range(len(tbl)):
                    print(str(tbl[r][1]) + " => " + tbl[r][0])
            except:
                print("[warning , 数据库为空!]")
        elif len(args) == 1:
            if "*" in args[0]:
                varTable = args[0].split("*")[0] + "%"  # t_store_%
                self.cur.execute(
                    'select table_name,create_time from information_schema.`TABLES` where table_schema="%s" and table_name like "%s" ' % (
                    self.varDB, varTable))
                tbl = self.cur.fetchall()
                print("\n" + self.varDB + "." + args[0] + " 表的创建时间" + "\n" + "-" * 60)
                for r in range(len(tbl)):
                    print(str(tbl[r][1]) + " => " + tbl[r][0])
            else:
                try:
                    self.cur.execute(
                        'select create_time from information_schema.`TABLES` where table_schema="%s" and table_name="%s" ' % (
                        self.varDB, args[0]))
                    tbl = self.cur.fetchone()
                    print("\n" + self.varDB + "." + args[0] + " 表的创建时间" + "\n" + "-" * 60)
                    print(str(tbl[0]) + " => " + args[0])
                except:
                    print("[errorrrrrrr , " + args[0] + "表不存在!]")
        elif len(args) == 2:
            if args[0] == "after" or args[0] == ">":
                self.cur.execute(
                    'select table_name,create_time from information_schema.`TABLES` where table_schema="%s" and create_time>"%s"' % (
                    self.varDB, args[1]))
                tbl = self.cur.fetchall()
                print("\n" + self.varDB + "下 " + str(len(tbl)) + " 张表在 " + str(args[1]) + " 之后被创建" + "\n" + "-" * 60)
                for r in range(len(tbl)):
                    print(str(tbl[r][1]) + " => " + tbl[r][0])
            elif args[0] == "before" or args[0] == "<":
                self.cur.execute(
                    'select table_name,create_time from information_schema.`TABLES` where table_schema="%s" and create_time<"%s"' % (
                    self.varDB, args[1]))
                tbl = self.cur.fetchall()
                print("\n" + self.varDB + "下 " + str(len(tbl)) + " 张表在 " + str(args[1]) + " 之前被创建" + "\n" + "-" * 60)
                for r in range(len(tbl)):
                    print(str(tbl[r][1]) + " => " + (tbl[r][0]))
            else:
                print("[errorrrrrrr , 参数1必须是 after 或 before ]")
        else:
            print("[errorrrrrrr , 参数溢出！]")



    def db2xlsx(self, sql, xlsxFile):
        '''
        4.1 使用pandas将数据库表导出excel
        :param sql:
        :param xlsxFile:
        :return:
                # Mysql_PO.db2xlsx("select * from sys_menu", "d:\\111.xlsx")
        '''
        try:
            df = pd.read_sql(sql=sql, con=self.getPymysqlEngine())
            df.to_excel(xlsxFile)
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) +" row" )

    def db2html(self, sql, htmlFile):
        '''
        4.2 使用pandas将数据库表导出html
        :param sql:
        :param toHtml:
        :return:
                # Mysql_PO.db2xlsx("select * from sys_menu", "d:\\index1.html")
                参考：https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_html.html
                css加载，https://blog.csdn.net/qq_38316655/article/details/104663077
                颜色，https://www.jianshu.com/p/946481cd288a
                https://www.jianshu.com/p/946481cd288a
        '''

        try:
            df = pd.read_sql(sql=sql, con=self.getPymysqlEngine())
            df.to_html(htmlFile,col_space=100,na_rep="0")
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def xlsx2db(self, varExcelFile, varTable, usecols=None, nrows=None, skiprows=None, dtype=None, parse_dates=None, date_parser=None, converters=None, sheet_name=None):
        '''
        4.4 excel导入数据库表(覆盖)
        :return:

        参数参考：https://zhuanlan.zhihu.com/p/96203752
        '''

        try:
            df = pd.read_excel(varExcelFile, usecols=usecols, nrows=nrows, skiprows=skiprows, dtype=dtype, parse_dates=parse_dates, date_parser=date_parser, converters=converters, sheet_name=sheet_name)
            df.to_sql(varTable, con=self.getMysqldbEngine(), if_exists='replace', index=False)
        except Exception as e:
            print(e)

    def dbDesc2xlsx(self, varFileName):
        '''
        5 将所有表结构导出到excel(覆盖)
        :param varFileName:
        :return:
        '''

        listSub = []
        listMain = []
        dict1 = {}

        try:
            self.cur.execute('select TABLE_NAME,TABLE_COMMENT from information_schema.`TABLES` where table_schema="%s" ' % self.varDB)
            tblName = self.cur.fetchall()
            listSub.append("表名")
            listSub.append("表说明")
            listSub.append("名称")
            listSub.append("数据类型(长度)")
            listSub.append("允许空值")
            listSub.append("主键")
            listSub.append("默认值")
            listSub.append("说明")
            dict1[1] = listSub
            for k in range(len(tblName)):
                self.cur.execute('select column_name,column_type,is_nullable,column_key,column_default,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (self.varDB, tblName[k][0]))
                tblFields = self.cur.fetchall()
                for i in range(len(tblFields)):
                    list3 = list(tblName[k]) + list(tblFields[i])
                    listMain.append(list3)
            for i in range(len(listMain)):
                dict1[i+2] = listMain[i]
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

        NewexcelPO(varFileName)
        Openpyxl_PO = OpenpyxlPO(varFileName)
        Openpyxl_PO.setRowValue(dict1)
        Openpyxl_PO.save()


if __name__ == '__main__':


    # 195_saas_test >>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Mysql_PO = MysqlPO("192.168.0.195", "root", "Zy123456", "saasuserdev", 3306)
    # Mysql_PO.cur.execute('select id from sys_org where orgName="%s"' % ("陈一机构"))
    # tmpTuple = Mysql_PO.cur.fetchall()
    # print(tmpTuple[0][0])
    # Mysql_PO.cur.execute('select id from sys_dept where localName="%s" and orgId="%s"' % ("阿里巴巴999",279))
    # id = Mysql_PO.cur.fetchall()
    # print(id)

    # 195_患者360_test   (开发环境)
    # mysql_PO = MysqlPO("192.168.0.195", "root", "Zy123456", "upvdev", 3306)
    # mysql_PO.dbRecord('*', 'char', u'%郑和成%')
    # mysql_PO.dbRecord('*', 'float', u'%295.54%')
    # mysql_PO.dbDesc()   # 打印所有表结构
    # mysql_PO.dbDesc2excel("d:\\test5.xlsx", "mySheet1")  # 将所有表结构导出到excel

    # 195_Bi_test   (测试环境）
    # Mysql_PO = MysqlPO("192.168.0.195", "root", "Zy123456", "bitest", 3306)
    # varUpdateDate = '2020-03-22'
    # # Mysql_PO.conn.cursor(MySQLdb.cursors.DictCursor)
    # # Mysql_PO.cur.execute('SELECT ifnull(round((SELECT inPAccount/10000 FROM `bi_inpatient_yard` where statisticsDate = "%s"),2),0)' % varUpdateDate)
    # # Mysql_PO.cur.execute('SELECT ifnull(round((SELECT inPAccount/10000 FROM `bi_inpatient_yard` where statisticsDate = "%s"),2),0)' % varUpdateDate)
    # Mysql_PO.cur.execute('SELECT deptname,round(outPAccount,2) from bi_outpatient_dept where statisticsDate ="%s" GROUP BY deptname ORDER BY outpaccount DESC LIMIT 10' % varUpdateDate)
    # tmpTuple = Mysql_PO.cur.fetchall()
    # print(tmpTuple)
    # print(tmpTuple[0][1])
    # # desc = Mysql_PO.cur.description     # 获取单表的字段名信息
    # # print(desc)
    # # print(Mysql_PO.cur.rowcount)   # 获取结果集的条数/
    # # print(tmpTuple[0][0])
    # Mysql_PO.cur.execute('select id,anaesthesiaId from bi_anaesthesia_dept where deptIdName="%s" ' % ("骨科"))
    # tmpTuple = Mysql_PO.cur.fetchall()
    # print(tmpTuple)
    # for i in tmpTuple:
    #     print(str(i[0]) + " , " + str(i[1]))


    # 39_crm_test >>>>>>>>>>>>>>>>>>>>>>>>>>>
    # mysql_PO = MysqlPO("192.168.0.39", "ceshi", "123456", "TD_OA", 3336)
    # crm小程序清空账号权限
    # mysql_PO.cur.execute("update user SET VX_MARK='', IMEI='', MODEL='',PLATFORM='', NOT_LOGIN=0, LIMIT_LOGIN=0 ")
    # mysql_PO.conn.commit()
    # tmpTuple = Mysql_PO.cur.fetchall()

    # Mysql_PO.cur.execute('select USER_NAME from user where USER_PRIV_NO=%s ' % (999))
    # l_result = Mysql_PO.cur.fetchall()
    # print(len(l_result))
    # print(l_result)
    # print(l_result[0][0])
    # for (Value) in l_result:
    #     print(Value)


    # 35_ehr_test - - - - - - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -
    # mysql_PO = MysqlPO("192.168.0.234", "sa", "Zy@123456", "healthrecord_test", 3336)  # 测试环境
    # mysql_PO = MysqlPO("192.168.0.35", "test", "123456", "healthrecord", 3336)  # 开发环境


    # 201_禅道 - - - - - - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -- - - -
    # mysql_PO = MysqlPO("192.168.0.201", "root1", "123456", "zentao", 3306) # 测试

    # 招远防疫 >>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Mysql_PO = MysqlPO("192.168.0.231", "root", "Zy123456", "epidemic_center", 3306)  # 开发
    Mysql_PO = MysqlPO("192.168.0.234", "root", "123456", "epd", 3306)   # 测试

    # Mysql_PO.cur.execute('select * from test1')
    # l_result = Mysql_PO.cur.fetchall()
    # print(l_result)
    # print("1 查看数据库表结构（字段、类型、大小、可空、注释）".center(100, "-"))
    # Mysql_PO.dbDesc()  # 所有表结构
    # Mysql_PO.dbDesc('sys_menu')   # 指定表结构
    # Mysql_PO.dbDesc('test*')  # u开头的表结构（通配符*）
    # Mysql_PO.dbDesc('test*', 'id', 'name', 'url')  # 搜索符合条件字段的u开头的表结构
    # Mysql_PO.dbDesc('test_menu', 'id', 'name')  # 搜索符合条件字段的user开头的表结构

    # print("2 查找记录".center(100, "-"))
    # Mysql_PO.dbRecord('sys_user', 'char', '%金%')  # 搜索user表中内容包含金丽娜的char类型记录。
    # Mysql_PO.dbRecord('*', 'varchar', u'%招远疫情防控公告123456%')   # 搜索所有表中带金丽娜的char类型记录。
    # Mysql_PO.dbRecord('*', 'datetime', u'%2021-11-17%')  # 模糊搜索所有表中日期类型为datetime的2019-04-12 15:13:23记录。

    # print("3 查找创建时间".center(100, "-"))
    # Mysql_PO.dbCreateDate()   # 查看所有表的创建时间
    # Mysql_PO.dbCreateDate('test1')   # 查看book表创建时间
    # Mysql_PO.dbCreateDate('test*')   # 查看所有b开头表的创建时间，通配符*
    # Mysql_PO.dbCreateDate('after', '2021-11-14')  # 查看所有在2019-02-18之后创建的表
    # Mysql_PO.dbCreateDate('>', '2021-11-14')  # 查看所有在2019-02-18之后创建的表
    # Mysql_PO.dbCreateDate('before', "2021-11-14")  # 显示所有在2019-12-08之前创建的表
    # Mysql_PO.dbCreateDate('<', "2021-11-14")  # 显示所有在2019-12-08之前创建的表


    # print("4.1，数据库表导出excel".center(100, "-"))
    # Mysql_PO.db2xlsx("select * from ba_area", "data/ba_area.xlsx")

    # print("4.2，数据库表导出html".center(100, "-"))
    # Mysql_PO.db2html("select * from ep_zj_center", "d:\\index1.html")

    print("4.4 excel导入数据库表".center(100, "-"))
    Mysql_PO.xlsx2db("data/testcase2.xlsx", "testcase2", sheet_name="case")
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", usecols=eval("range(4)"), nrows=6, dtype={'No.': str, '金额': float},parse_dates=['isRun'], date_parser=lambda x: pd.to_datetime(x, format='%Y%m'))  # 读取表格中前3列、前6行数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", usecols=eval("range(4)"), nrows=6, converters={'isRun': lambda x: pd.to_datetime(x, format='%Y%m')})  # 读取表格中前3列、前6行数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", eval("range(3)"), 6, skiprows=range(1, 100, 2), sheet_name="case")  # 读取表格中前3列、前6行数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", eval("range(3)"), 6, range(1, 100, 2))  # 读取表格中前3列、前6行数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", "A,C,E", None)  # 读取表格中A,C,E3列数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", "A:F", None)  # 读取表格中A-F 列数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", [0,3,4,5], None)  # 读取表格中4列数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", ['interURL','一级属性'], None)  # 读取表格中['interURL','一级属性']列数据写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", lambda x: x in ['班级', 'interURL', '语文'], None)  # 读取表格中符合（存在）['班级', 'interURL', '语文']列数据，并写入数据库表
    # Openpyxl_PO.xlsx2db("data/testcase2.xlsx", "testcase2", lambda x: x in ['班级', 'interURL', '语文'], None, sheet_name="case")  # 读取表格中符合（存在）['班级', 'interURL', '语文']列数据，并写入数据库表



    # print("5 将所有表结构导出到excel(覆盖)".center(100, "-"))
    # Mysql_PO.dbDesc2xlsx("d:\\test.xlsx")  # 将所有表结构导出到excel

