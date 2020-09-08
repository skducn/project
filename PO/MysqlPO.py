# -*- coding: utf-8 -*-
#***************************************************************
# Author     : John
# Revise on : 2019-04-16
# Description: MysqlPO对象层，定义mysql数据库封装对象
# 查询后中文正确显示，但在数据库中却显示乱码 ， 解决方法如下 ，添加 charset='utf8 ，  charset是要跟你数据库的编码一样，如果是数据库是gb2312 ,则写charset='gb2312'。
# conn = pymssql.Connect(host='localhost', user='root', passwd='root', db='python',charset='utf8')
# pip3.7 install mysqlclient
# None是一个对象，而NULL是一个类型。
# Python中没有NULL，只有None，None有自己的特殊类型NoneType。
# None不等于0、任何空字符串、False等。
# 在Python中，None、False、0、""(空字符串)、[](空列表)、()(空元组)、{}(空字典)都相当于False。
#***************************************************************

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from PO.ExcelPO.ExcelPO import *
Excel_PO = ExcelPO()

class MysqlPO():

    def __init__(self, varHost, varUser, varPassword, varDB, varPort=3336):

        self.varDB = varDB
        self.conn = MySQLdb.connect(host=varHost, user=varUser, passwd=varPassword, db=varDB, port=int(varPort), use_unicode=True)
        self.cur = self.conn.cursor()
        self.cur.execute('SET NAMES utf8;')
        # self.conn.set_character_set('utf8')
        self.cur.execute('show tables')

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

                print("*" * 100 + "\n" + tblName[k][0] + " ( " + tblName[k][1] + " ) - " + str(len(tblFields)) + "个字段 " +
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
                            print("*" * 100 + "\n" + varTable + "(" + tblDDL[0] + ") - " + str(
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
                    print("*" * 100 + "\n" + varTable + "(" + tblDDL[0] + ") - " + str(
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
                            print("*" * 100 + "\n" + varTable + "(" + tblDDL[0] + ") - " + str(
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
                    print("*" * 100 + "\n" + varTable + "(" + tblDDL[0] + ") - " + str(
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
        ''' 查表的创建时间及区间
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

    def dbDesc2excel(self, varFileName, varSheetName):
        ''' 将数据库表结构（字段、类型、DDL）导出到excel'''

        l_name = []
        l_dataType = []
        l_isNull = []
        l_isKey = []
        l_default = []
        l_comment = []

        listSub = []
        listMain = []
        sum = 1

        self.cur.execute('select TABLE_NAME,TABLE_COMMENT from information_schema.`TABLES` where table_schema="%s" ' % self.varDB)
        tblName = self.cur.fetchall()
        for k in range(len(tblName)):
            self.cur.execute('select column_name,column_type,is_nullable,column_key,column_default,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (self.varDB, tblName[k][0]))
            tblFields = self.cur.fetchall()
            listSub.append(1)
            listSub.append("表名")
            listSub.append("表说明")
            listSub.append("名称")
            listSub.append("数据类型(长度)")
            listSub.append("允许空值")
            listSub.append("主键")
            listSub.append("默认值")
            listSub.append("说明")
            listMain.append(listSub)
            listSub = []
            for i in tblFields:
                l_name.append(i[0])
                l_dataType.append(i[1])
                l_isNull.append(i[2])
                l_isKey.append(i[3])
                if i[4] == None:
                    l_default.append("")
                else:
                    l_default.append(i[4])
                l_comment.append(i[5])
            x = 0
            for i in range(len(tblFields)):
                listSub.append(sum+1)
                if x != 1:
                    listSub.append(tblName[k][0])
                    listSub.append(tblName[k][1])
                else:
                    listSub.append("")
                    listSub.append("")
                listSub.append(l_name[i])
                listSub.append(l_dataType[i])
                listSub.append(l_isNull[i])
                listSub.append(l_isKey[i])
                listSub.append(l_default[i])
                listSub.append(l_comment[i])
                listMain.append(listSub)
                listSub = []
                sum = sum + 1
                x = 1
            l_name = []
            l_dataType = []
            l_isNull = []
            l_isKey = []
            l_default = []
            l_comment = []

        Excel_PO.writeXlsxByMore(varFileName, varSheetName, listMain)

    def dbDesc2excelbak(self, varFileName, varSheetName):
        ''' 将数据库表结构（字段、类型、DDL）导出到excel'''

        l_name = []
        l_type = []
        l_isnull = []
        l_comment = []
        l_isKey = []
        listSub = []
        listMain = []
        sum = 1

        self.cur.execute('select TABLE_NAME,TABLE_COMMENT from information_schema.`TABLES` where table_schema="%s" ' % self.varDB)
        tblName = self.cur.fetchall()
        for k in range(len(tblName)):
            self.cur.execute('select column_name,column_type,is_nullable,column_comment,column_key from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (self.varDB, tblName[k][0]))
            tblFields = self.cur.fetchall()
            listSub.append(1)
            listSub.append("表名")
            listSub.append("表说明")
            listSub.append("字段名")
            listSub.append("字段说明")
            listSub.append("字段类型")
            listSub.append("主键")
            listSub.append("是否为空")
            listMain.append(listSub)
            listSub = []
            for i in tblFields:
                l_name.append(i[0])
                l_type.append(i[1])
                l_isnull.append(i[2])
                l_comment.append(i[3])
                l_isKey.append(i[4])
            for i in range(len(tblFields)):
                listSub.append(sum+1)
                listSub.append(tblName[k][0])
                listSub.append(tblName[k][1])
                listSub.append(l_name[i])
                listSub.append(l_comment[i])
                listSub.append(l_type[i])
                listSub.append(l_isKey[i])
                listSub.append(l_isnull[i])
                listMain.append(listSub)
                listSub = []
                sum = sum + 1
            l_name = []
            l_comment = []
            l_type = []
            l_isKey = []
            l_isnull = []

        Excel_PO.writeXlsxByMore(varFileName, varSheetName, listMain)

if __name__ == '__main__':

    # pass
    Mysql_PO = MysqlPO("192.168.0.195", "root", "Zy123456", "saasuserdev", 3306)  # 测试环境
    Mysql_PO.cur.execute('select id from sys_org where orgName="%s"' % ("陈一机构"))
    tmpTuple = Mysql_PO.cur.fetchall()
    print(tmpTuple[0][0])

    Mysql_PO.cur.execute('select id from sys_dept where localName="%s" and orgId="%s"' % ("阿里巴巴999",279))
    id = Mysql_PO.cur.fetchall()
    print(id)


    # Mysql_PO.dbDesc2excel("d:\\saasuserdev.xlsx", "mySheet1")  # 将所有表结构导出到excel
    # Mysql_PO.cur.execute('select id from sys_org where orgName="%s"' % 123)


    # # # crm小程序清空账号权限
    # mysql_PO = MysqlPO("192.168.0.39", "ceshi", "123456", "TD_OA", 3336)
    # mysql_PO.cur.execute("update user SET VX_MARK='', IMEI='', MODEL='',PLATFORM='', NOT_LOGIN=0, LIMIT_LOGIN=0 ")
    # mysql_PO.conn.commit()

    # tmpTuple = Mysql_PO.cur.fetchall()
    # 患者360 开发环境
    # mysql_PO = MysqlPO("192.168.0.195", "root", "Zy123456", "upvdev", 3306)
    # mysql_PO.dbRecord('*', 'char', u'%郑和成%')
    # mysql_PO.dbRecord('*', 'float', u'%295.54%')
    # mysql_PO.dbDesc()   # 打印所有表结构
    # mysql_PO.dbDesc2excel("d:\\test5.xlsx", "mySheet1")  # 将所有表结构导出到excel


    # BI 测试环境
    # Mysql_PO = MysqlPO("192.168.0.195", "root", "Zy123456", "bitest", 3306)
    # varUpdateDate = '2020-03-22'
    #
    # # Mysql_PO.conn.cursor(MySQLdb.cursors.DictCursor)
    # # Mysql_PO.cur.execute('SELECT ifnull(round((SELECT inPAccount/10000 FROM `bi_inpatient_yard` where statisticsDate = "%s"),2),0)' % varUpdateDate)
    # # Mysql_PO.cur.execute('SELECT ifnull(round((SELECT inPAccount/10000 FROM `bi_inpatient_yard` where statisticsDate = "%s"),2),0)' % varUpdateDate)
    # Mysql_PO.cur.execute('SELECT deptname,round(outPAccount,2) from bi_outpatient_dept where statisticsDate ="%s" GROUP BY deptname ORDER BY outpaccount DESC LIMIT 10' % varUpdateDate)
    # tmpTuple = Mysql_PO.cur.fetchall()
    # print(tmpTuple)
    # print(tmpTuple[0][1])
    #
    # # desc = Mysql_PO.cur.description     # 获取单表的字段名信息
    # # print(desc)
    # # print(Mysql_PO.cur.rowcount)   # 获取结果集的条数/
    # # print(tmpTuple[0][0])


    # Mysql_PO.cur.execute('select id,anaesthesiaId from bi_anaesthesia_dept where deptIdName="%s" ' % ("骨科"))
    # tmpTuple = Mysql_PO.cur.fetchall()
    # print(tmpTuple)
    # for i in tmpTuple:
    #     print(str(i[0]) + " , " + str(i[1]))

    # Mysql_PO = MysqlPO("192.168.0.39", "ceshi", "123456", "TD_OA", 3336)  # 盛蕴CRM小程序 测试环境
    #
    # Mysql_PO.cur.execute('select USER_NAME from user where USER_PRIV_NO=%s ' % (999))
    # l_result = Mysql_PO.cur.fetchall()
    # print(len(l_result))
    # print(l_result)
    # print(l_result[0][0])
    # for (Value) in l_result:
    #     print(Value)

    # Mysql_PO.dbDesc()  # 所有表结构
    # Mysql_PO.dbDesc('user')   # 指定表结构
    # Mysql_PO.dbDesc('u*')  # u开头的表结构（通配符*）
    # Mysql_PO.dbDesc('use*', 'USER_NAME', 'KEY_SN', "BYNAME")  # 搜索符合条件字段的u开头的表结构
    # Mysql_PO.dbDesc('user', 'USER_NAME', 'KEY_SN', "BYNAME")  # 搜索符合条件字段的user开头的表结构

    # Mysql_PO.dbRecord('user', 'char', '%金丽娜%')  # 搜索user表中内容包含金丽娜的char类型记录。
    # Mysql_PO.dbRecord('*', 'varchar', u'%金丽娜%')   # 搜索所有表中带金丽娜的char类型记录。
    # Mysql_PO.dbRecord('*', 'datetime', u'%2019-10-10%')  # 模糊搜索所有表中日期类型为datetime的2019-04-12 15:13:23记录。

    # Mysql_PO.dbCreateDate()   # 查看所有表的创建时间
    # Mysql_PO.dbCreateDate('app_code')   # 查看book表创建时间
    # Mysql_PO.dbCreateDate('fact*')   # 查看所有b开头表的创建时间，通配符*
    # Mysql_PO.dbCreateDate('after', '2019-02-18')  # 查看所有在2019-02-18之后创建的表
    # Mysql_PO.dbCreateDate('>', '2019-02-18')  # 查看所有在2019-02-18之后创建的表
    # Mysql_PO.dbCreateDate('before', "2019-04-10")  # 显示所有在2019-12-08之前创建的表
    # Mysql_PO.dbCreateDate('<', "2019-02-18")  # 显示所有在2019-12-08之前创建的表
