# coding=utf-8
#***************************************************************
# Author     : John
# Revise on : 2019-04-16
# Description: SqlServerPO对象层
# sql server 查询数据库所有的表名 + 字段  https://www.cnblogs.com/TF12138/p/4064752.html
# pymssql 托管在Github上：https://github.com/pymssql
# python连接sql server数据库实现增删改查 https://www.cnblogs.com/malcolmfeng/p/6909293.html
# /usr/local/pip3.7 install pymssql
# 问题：查询后中文正确显示，但在数据库中却显示乱码
# 解决方法：添加 charset='utf8' , 确保 charset 与数据库编码一致，如数据库是gb2312 , 则charset='gb2312'。
# conn = pymssql.Connect(host='localhost', user='root', passwd='root', db='python',charset='utf8')
#***************************************************************

import pymssql,uuid
# print(pymssql.__version__)
from adodbapi import connect

class SqlServerPO():

    def __init__(self, varHost, varUser, varPassword, varDB):
        # 类的构造函数，初始化DBC连接信息
        self.varHost = varHost
        self.varUser = varUser
        self.varPassword = varPassword
        self.varDB = varDB

    def __GetConnect123(self):
        # 得到数据库连接信息，返回conn.cursor()
        if not self.varDB:
            raise (NameError, "没有设置数据库信息")
        # self.conn = connect(server=self.varHost, user=self.varUser, password=self.varPassword, database=self.varDB)
        self.conn = connect('Provider=SQLOLEDB.1;Data Source=%s;Initial Catalog=%s;UserID = %s;Password = %s;'%(self.varHost, self.varDB, self.varUser, self.varPassword))

        cur = self.conn.cursor()  # 创建一个游标对象
        if not cur:
            raise (NameError, "连接数据库失败")  # 将DBC信息赋值给cur
        else:
            return cur

    def __GetConnect(self):
        # 得到数据库连接信息，返回conn.cursor()
        if not self.varDB:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymssql.connect(server=self.varHost, user=self.varUser, password=self.varPassword, database=self.varDB)
        cur = self.conn.cursor()  # 创建一个游标对象
        if not cur:
            raise (NameError, "连接数据库失败")  # 将DBC信息赋值给cur
        else:
            return cur

    def ExecQuery(self, sql):
        '''
        执行查询语句
        返回一个包含tuple的list，list是元素的记录行，tuple记录每行的字段数值
        '''

        cur = self.__GetConnect()
        self.conn.commit()  # 新增后需要马上查询的话，则先commit一下。
        cur.execute(sql)  # 执行查询语句

        try:
            result = cur.fetchall()  # fetchall()获取查询结果
        except:
            self.conn.commit()
            cur.close()  # 关闭游标
            self.conn.close()  # 关闭连接
            return
        self.conn.commit()
        cur.close()  # 关闭游标
        self.conn.close()  # 关闭连接
        return result

    def ExecProcedure(self, varProcedureName):
        '''
        执行存储过程
        '''

        cur = self.__GetConnect()
        # sql =[]
        # sql.append("exec procontrol")
        # cur.callproc(varProcedureName)

        cur.execute(varProcedureName)
        # result = cur.fetchall()
        # for rec in result:
        #     print(rec)
        self.conn.commit()
        cur.close()  # 关闭游标
        self.conn.close()  # 关闭连接



    def ExecQueryBySQL(self, varPathSqlFile):

        '''执行sql文件语句'''

        cur = self.__GetConnect()
        with open(varPathSqlFile) as f:
        # with open('D:\\51\\python\\project\\instance\\zyjk\\EHR\\controlRule\\mm.sql') as f:
            sql = f.read()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()

    def ExecQueryBySQL1(self, varPathSqlFile):

        '''执行sql文件语句'''

        cur = self.__GetConnect()
        with open(varPathSqlFile) as f:
            sql = f.read()
            cur.execute(sql)
            cur.nextset()
            # cur.callproc(sql,(1,2))
            # self.conn.commit()
            self.conn.close()


    def dbDesc(self, *args):
        ''' 搜索表结构，表名区分大小写 '''
        # Sqlserver_PO.dbDesc()   # 查看所有表结构
        # Sqlserver_PO.dbDesc('myclass')   # 查看 myclass 表结构
        # Sqlserver_PO.dbDesc('b*')  # 查看所有b开头的表结构（通配符*） ???
        # Sqlserver_PO.dbDesc('book', 'id,page')   # 查看book表id,page字段的结构
        # Sqlserver_PO.dbDesc('b*', 'id,page')  # 查看所有b开头的表中id字段的结构（通配符*）
        self.cur = self.__GetConnect()

        dict1 ={}
        tblComment = "SELECT DISTINCT d.name,f.value FROM syscolumns a LEFT JOIN systypes b ON a.xusertype= b.xusertype INNER JOIN sysobjects d ON a.id= d.id AND d.xtype= 'U' AND d.name<> 'dtproperties' LEFT JOIN syscomments e ON a.cdefault= e.id LEFT JOIN sys.extended_properties g ON a.id= G.major_id AND a.colid= g.minor_id LEFT JOIN sys.extended_properties f ON d.id= f.major_id AND f.minor_id= 0"
        self.cur.execute(tblComment)
        tblComment = self.cur.fetchall()
        for t in tblComment:
            if t[1] != None:
                dict1[t[0]] = t[1].decode('utf8')
            else:
                dict1[t[0]] = t[1]
        # print(dict1)

        if len(args) == 0:
            # 查看所有表结构，获取数据库下有多少张表
            allTable = "select * from sysobjects where xtype = 'u' and name != 'sysdiagrams'"
            self.cur.execute(allTable)
            allTable = self.cur.fetchall()
            varInfo = "数据库<" + self.varDB + ">共有<" + str(len(allTable)) + ">张表\n"
            print(varInfo)
            for tbl in allTable:
                # 遍历表
                varTable = tbl[0]
                sql = "SELECT A.name, B.name, d.name, B.max_length, B.is_nullable, C.value FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'" % (varTable)
                try:
                    self.cur.execute(sql)
                    results = self.cur.fetchall()
                    tblName = results[0][0]
                    x = y = z = 0
                    for i in results:
                        if len(i[1]) > x: x = len(i[1])
                        if len(i[2]) > y: y = len(i[2])
                        if len(str(i[3])) > z: z = len(str(i[3]))
                    varComment = dict1.get(tblName, "error,没有找到!")
                    print("*" * 100 + "\n" + str(
                        tblName + "(" + str(varComment) + ") - " + str(len(results)) + "个字段") + "\n字段" + " " * (
                                  x - 3), "类型" + " " * (y - 3), "大小" + " " * (z + 2), "可空" + " " * 7, "注释")
                    # print("*" * 100 + "\n" + str(tblName + " - " + str(len(results)) + "个字段") + "\n字段" + " " * (x - 3),"类型" + " " * (y - 3), "大小" + " " * (z+2), "可空" + " " * 6, "注释")
                    for row in results:
                        # 遍历字段、类型、大小、可空、注释
                        if row[5] != None:
                            if row[4] == True:
                                print(row[1] + " " * (x - len(row[1]) + 1), row[2] + " " * (y - len(row[2]) + 1), str(row[3]) + " " * (z - len(str(row[3])) + 6), str(row[4]) + " " * (6),str(row[5], 'utf-8'))
                            else:
                                print(row[1] + " " * (x - len(row[1]) + 1), row[2] + " " * (y - len(row[2]) + 1), str(row[3]) + " " * (z - len(str(row[3])) + 6), str(row[4]) + " " * (5),str(row[5], 'utf-8'))
                        else:
                            if row[4] == True:
                                print(row[1] + " " * (x - len(row[1]) + 1), row[2] + " " * (y - len(row[2]) + 1), str(row[3]) + " " * (z - len(str(row[3])) + 6), str(row[4]) + " " * (6), str(row[5]))
                            else:
                                print(row[1] + " " * (x - len(row[1]) + 1), row[2] + " " * (y - len(row[2]) + 1), str(row[3]) + " " * (z - len(str(row[3])) + 6), str(row[4]) + " " * (5), str(row[5]))
                except Exception as e:
                    raise e
                finally:
                    print("\n")
        elif len(args) == 1:
            varTable = args[0]
            if "*" in varTable:
                # 模糊匹配多个表格的所有表结构，搜索表明中带xxx的表结构（如：upmxxxtest）
                tblHead = varTable.split("*")[0]
                # 查看所有表结构，获取数据库下有多少张表
                allTable = "select * from sysobjects where xtype = 'u' and name != 'sysdiagrams'"
                self.cur.execute(allTable)
                allTable = self.cur.fetchall()
                tblCount = 0
                for tbl in allTable:
                    if tblHead in tbl[0]:
                        tblCount += 1
                varInfo = "数据库<" + self.varDB + ">中表名带有<" + tblHead + ">字符的共有<" + str(tblCount) + ">张表\n"
                print(varInfo)
                allTable = "select * from sysobjects where xtype = 'u' and name != 'sysdiagrams'"
                self.cur.execute(allTable)
                allTable = self.cur.fetchall()
                for tbl in allTable:
                    # 遍历表
                    if tblHead in tbl[0]:
                        varTable = tbl[0]
                        sql = "SELECT A.name, B.name, d.name, B.max_length, B.is_nullable, C.value FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'" % (
                            varTable)
                        try:
                            self.cur.execute(sql)
                            results = self.cur.fetchall()
                            tblName = results[0][0]
                            x = y = z = 0
                            for i in results:
                                if len(i[1]) > x: x = len(i[1])
                                if len(i[2]) > y: y = len(i[2])
                                if len(str(i[3])) > z: z = len(str(i[3]))
                            varComment = dict1.get(tblName, "error,没有找到!")
                            print("*" * 100 + "\n" + str(tblName + "(" + str(varComment) + ") - " + str(len(results)) + "个字段") + "\n字段" + " " * (
                                        x - 3), "类型" + " " * (y - 3), "大小" + " " * (z + 2), "可空" + " " * 6, "注释")
                            for row in results:
                                # 遍历字段、类型、大小、可空、注释
                                if row[5] != None:
                                    if row[4] == True:
                                        print(row[1] + " " * (x - len(row[1]) + 1),
                                              row[2] + " " * (y - len(row[2]) + 1),
                                              str(row[3]) + " " * (z - len(str(row[3])) + 6), str(row[4]) + " " * (6),
                                              str(row[5], 'utf-8'))
                                    else:
                                        print(row[1] + " " * (x - len(row[1]) + 1),
                                              row[2] + " " * (y - len(row[2]) + 1),
                                              str(row[3]) + " " * (z - len(str(row[3])) + 6), str(row[4]) + " " * (5),
                                              str(row[5], 'utf-8'))
                                else:
                                    if row[4] == True:
                                        print(row[1] + " " * (x - len(row[1]) + 1),
                                              row[2] + " " * (y - len(row[2]) + 1),
                                              str(row[3]) + " " * (z - len(str(row[3])) + 6), str(row[4]) + " " * (6),
                                              str(row[5]))
                                    else:
                                        print(row[1] + " " * (x - len(row[1]) + 1),
                                              row[2] + " " * (y - len(row[2]) + 1),
                                              str(row[3]) + " " * (z - len(str(row[3])) + 6), str(row[4]) + " " * (5),
                                              str(row[5]))
                        except Exception as e:
                            raise e
                        finally:
                            print("\n")
            elif "*" not in varTable:
                # 单个表格的所有表结构
                sql = "SELECT A.name, B.name, d.name, B.max_length, B.is_nullable, C.value FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'" % (
                    varTable)
                try:
                    self.cur.execute(sql)
                    results = self.cur.fetchall()
                    tblName = results[0][0]
                    x = y = z = 0
                    for i in results:
                        if len(i[1]) > x: x = len(i[1])
                        if len(i[2]) > y: y = len(i[2])
                        if len(str(i[3])) > z: z = len(str(i[3]))

                    varComment = dict1.get(tblName, "error,没有找到!")
                    print("*" * 100 + "\n" + str(
                        tblName + "(" + str(varComment) + ") - " + str(len(results)) + "个字段") + "\n字段" + " " * (
                                  x - 3), "类型" + " " * (y - 3), "大小" + " " * (z + 2), "可空" + " " * 7, "注释")
                    for row in results:
                        # 遍历字段、类型、大小、可空、注释
                        if row[5] != None:
                            if row[4] == True:
                                print(row[1] + " " * (x - len(row[1]) + 1), row[2] + " " * (y - len(row[2]) + 1),
                                      str(row[3]) + " " * (z - len(str(row[3])) + 6), str(row[4]) + " " * (6),
                                      str(row[5], 'utf-8'))
                            else:
                                print(row[1] + " " * (x - len(row[1]) + 1), row[2] + " " * (y - len(row[2]) + 1),
                                      str(row[3]) + " " * (z - len(str(row[3])) + 6), str(row[4]) + " " * (5),
                                      str(row[5], 'utf-8'))
                        else:
                            if row[4] == True:
                                print(row[1] + " " * (x - len(row[1]) + 1), row[2] + " " * (y - len(row[2]) + 1),
                                      str(row[3]) + " " * (z - len(str(row[3])) + 6), str(row[4]) + " " * (6),
                                      str(row[5]))
                            else:
                                print(row[1] + " " * (x - len(row[1]) + 1), row[2] + " " * (y - len(row[2]) + 1),
                                      str(row[3]) + " " * (z - len(str(row[3])) + 6), str(row[4]) + " " * (5),
                                      str(row[5]))
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
                self.cur.execute(allTable)
                allTable = self.cur.fetchall()
                tblCount = 0
                for tbl in allTable:
                    if tblHead in tbl[0]:
                        tblCount += 1
                if tblCount == 0 :
                    print("数据库<" + self.varDB + ">中没有发现表名中带有<" + tblHead + ">字符的表\n")
                else:
                    varInfo = "数据库<" + self.varDB + ">中符合<" + varTable + ">表共有<" + str(tblCount) + ">张，其中包含<" + varFields + ">字段的表如下：\n"
                    print(varInfo)
                allTable = "select * from sysobjects where xtype = 'u' and name != 'sysdiagrams'"
                self.cur.execute(allTable)
                allTable = self.cur.fetchall()
                for tbl in allTable:
                    # 遍历表
                    if tblHead in tbl[0]:
                        varTable = tbl[0]
                        sql = "SELECT A.name, B.name, d.name, B.max_length, B.is_nullable, C.value FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'" % (
                            varTable)
                        try:
                            self.cur.execute(sql)
                            results = self.cur.fetchall()
                            tblName = results[0][0]
                            x = y = z = 0
                            for i in results:
                                if len(i[1]) > x: x = len(i[1])
                                if len(i[2]) > y: y = len(i[2])
                                if len(str(i[3])) > z: z = len(str(i[3]))
                            for row in results:
                                if row[1] in varFields:
                                    varComment = dict1.get(tblName, "error,没有找到!")
                                    print("*" * 100 + "\n" + str(tblName + "(" + str(varComment) + ") - " + str(
                                        len(results)) + "个字段") + "\n字段" + " " * (
                                                  x - 3), "类型" + " " * (y - 3), "大小" + " " * (z + 2), "可空" + " " * 6,
                                          "注释")
                                    # print("*" * 100 + "\n" + str(
                                    #     tblName + " - " + str(len(results)) + "个字段") + "\n字段" + " " * (
                                    #               x - 3),
                                    #       "类型" + " " * (y - 3), "大小" + " " * (z + 2), "可空" + " " * 6, "注释")
                            for row in results:
                                # 遍历字段、类型、大小、可空、注释
                                if row[1] in varFields:
                                    if row[5] != None:
                                        if row[4] == True:
                                            print(row[1] + " " * (x - len(row[1]) + 1),
                                                  row[2] + " " * (y - len(row[2]) + 1),
                                                  str(row[3]) + " " * (z - len(str(row[3])) + 6), str(row[4]) + " " * (6),
                                                  str(row[5], 'utf-8'))
                                        else:
                                            print(row[1] + " " * (x - len(row[1]) + 1),
                                                  row[2] + " " * (y - len(row[2]) + 1),
                                                  str(row[3]) + " " * (z - len(str(row[3])) + 6), str(row[4]) + " " * (5),
                                                  str(row[5], 'utf-8'))
                                    else:
                                        if row[4] == True:
                                            print(row[1] + " " * (x - len(row[1]) + 1),
                                                  row[2] + " " * (y - len(row[2]) + 1),
                                                  str(row[3]) + " " * (z - len(str(row[3])) + 6), str(row[4]) + " " * (6),
                                                  str(row[5]))
                                        else:
                                            print(row[1] + " " * (x - len(row[1]) + 1),
                                                  row[2] + " " * (y - len(row[2]) + 1),
                                                  str(row[3]) + " " * (z - len(str(row[3])) + 6), str(row[4]) + " " * (5),
                                                  str(row[5]))
                        except Exception as e:
                            raise e
                        finally:
                            print("\n")
            elif "*" not in varTable:
                # 单个表格可选字段表结构
                sql = "SELECT A.name, B.name, d.name, B.max_length, B.is_nullable, C.value FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'" % (
                    varTable)
                try:
                    self.cur.execute(sql)
                    results = self.cur.fetchall()
                    tblName = results[0][0]
                    x = y = z = 0
                    for i in results:
                        if len(i[1]) > x: x = len(i[1])
                        if len(i[2]) > y: y = len(i[2])
                        if len(str(i[3])) > z: z = len(str(i[3]))

                    varComment = dict1.get(tblName, "error,没有找到!")
                    print("*" * 100 + "\n" + str(
                        tblName + "(" + str(varComment) + ") - " + str(len(results)) + "个字段") + "\n字段" + " " * (
                                  x - 3), "类型" + " " * (y - 3), "大小" + " " * (z + 2), "可空" + " " * 6, "注释")

                    # print("*" * 100 + "\n" + str(
                    #     tblName + " - " + str(len(results)) + "个字段") + "\n字段" + " " * (
                    #               x - 3),
                    #       "类型" + " " * (y - 3), "大小" + " " * (z + 2), "可空" + " " * 6, "注释")
                    for row in results:
                        # 遍历字段、类型、大小、可空、注释
                        if row[1] in varFields:
                            if row[5] != None:
                                if row[4] == True:
                                    print(row[1] + " " * (x - len(row[1]) + 1),
                                          row[2] + " " * (y - len(row[2]) + 1),
                                          str(row[3]) + " " * (z - len(str(row[3])) + 6), str(row[4]) + " " * (6),
                                          str(row[5], 'utf-8'))
                                else:
                                    print(row[1] + " " * (x - len(row[1]) + 1),
                                          row[2] + " " * (y - len(row[2]) + 1),
                                          str(row[3]) + " " * (z - len(str(row[3])) + 6), str(row[4]) + " " * (5),
                                          str(row[5], 'utf-8'))
                            else:
                                if row[4] == True:
                                    print(row[1] + " " * (x - len(row[1]) + 1),
                                          row[2] + " " * (y - len(row[2]) + 1),
                                          str(row[3]) + " " * (z - len(str(row[3])) + 6), str(row[4]) + " " * (6),
                                          str(row[5]))
                                else:
                                    print(row[1] + " " * (x - len(row[1]) + 1),
                                          row[2] + " " * (y - len(row[2]) + 1),
                                          str(row[3]) + " " * (z - len(str(row[3])) + 6), str(row[4]) + " " * (5),
                                          str(row[5]))
                except Exception as e:
                    print(e, ",很抱歉，您搜索的表<" + varTable + ">不存在！")
                finally:
                    print("\n")
        self.conn.close()

    def dbRecord(self, varTable, varType, varValue):
        '''
        # 模糊搜索关键字,显示记录
        # 参数1：varTable = 表名（*表示所有的表）
        # 参数2：varType = 数据类型(char,int,double,timestamp)
        # 参数3：varValue = 值 (支持%模糊查询，如 %yy%)
        '''
        # Sqlserver_PO.dbRecord('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
        # Sqlserver_PO.dbRecord('*', 'varchar', '%海鹰居委会%')
        # Sqlserver_PO.dbRecord('*', 'money', '%34.5%')
        # Sqlserver_PO.dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
        # Sqlserver_PO.dbRecord('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。
        self.cur = self.__GetConnect()

        list0 = []
        list1 = []
        x = y = 0
        if varType in "double,timestamp,float,money,int,nchar,nvarchar,datetime,varchar":
            if "*" in varTable:
                # 遍历所有表
                self.cur.execute("SELECT NAME FROM SYSOBJECTS WHERE TYPE='U'")
                tbl = self.cur.fetchall()
                for b in range(len(tbl)):
                    # 遍历所有的表 的 列名称、列类别、类注释
                    varTable = tbl[b][0]
                    self.cur.execute(
                        "select syscolumns.name,systypes.name from syscolumns,systypes where syscolumns.xusertype=systypes.xusertype and syscolumns.id=object_id('%s')" % (
                            varTable))
                    tblFields = self.cur.fetchall()
                    for i in tblFields:
                        if len(i[0]) > x: x = len(i[0])
                        if len(i[1]) > y: y = len(i[1])
                    for j in tblFields:
                        if varType in j[1]:
                            list0.append(j[0])
                            list1.append(j[1])
                    # print(varTable + " - " + str(list0))   # 遍历输出所有表与字段名
                    for i in range(0, len(list0)):
                        self.cur.execute("select * from %s where convert(varchar, %s, 120) like '%s'" % (varTable, list0[i], varValue))
                        t4 = self.cur.fetchall()
                        if len(t4) != 0:
                            print("*" * 100)
                            print("搜索: " + varValue + " , " + str(len(t4)) + " 条记录 来自 " + self.varDB + "." + varTable + "(" ")." + list0[i] + "\n")
                            for j in range(len(t4)):
                                print(t4[j])
                    list0 = []
                    list1 = []
            elif "*" not in varTable:
                # 获取列名称、列类别、类注释
                self.cur.execute(
                    "select syscolumns.name,systypes.name from syscolumns,systypes where syscolumns.xusertype=systypes.xusertype and syscolumns.id=object_id('%s')" % (
                        varTable))
                tblFields = self.cur.fetchall()
                for i in tblFields:
                    if len(i[0]) > x: x = len(i[0])
                    if len(i[1]) > y: y = len(i[1])
                for j in tblFields:
                    if varType in j[1]:
                        list0.append(j[0])
                        list1.append(j[1])
                for i in range(0, len(list0)):
                    self.cur.execute("select * from %s where convert(varchar, %s, 120) like '%s'" % (varTable, list0[i], varValue))
                    t4 = self.cur.fetchall()
                    if len(t4) != 0:
                        print("*" * 100)
                        print("搜索: " + varValue + " , " + str(len(t4)) + " 条记录 来自 " + self.varDB + "." + varTable + "(" ")." + list0[i] + "\n")
                        # print("search: " + varValue + " > " + self.varDB + "." + varTable + "(" ")." + list0[i] + " > [" + str(len(t4)) + " 条记录]" + "\n")
                        for j in range(len(t4)):
                            print(t4[j])
                list0 = []
                list1 = []
        else:
            print("\n" + varType + "类型不存在，如：float,money,int,nchar,nvarchar,datetime,timestamp")
        self.conn.close()

    def dbDesc1(self, *args):
        ''' 查看数据库表结构（字段、类型、DDL）
        第1个参数：表名或表头*（通配符*）
        第2个参数：字段名（区分大小写），指定查看的字段名，多个字段名用逗号分隔，不支持通配符*
        '''
        # Mysql_PO.dbDesc()  # 搜索所有表结构
        # Mysql_PO.dbDesc('fact*')  # 搜索fact开头的表结构（通配符*）
        # Mysql_PO.dbDesc('fact_visit')   # 搜索app_info表结构
        # Mysql_PO.dbDesc('fact*', 'Id', "IsAccept")  # 搜索fact开头的表结构.并只显示Id，page字段
        # Mysql_PO.dbDesc('app_info', "id", "mid", "icon")   # 搜索app_info表结构，并只显示id，mid,icon字段
        l_name = []
        l_type = []
        l_isnull = []
        l_comment = []
        x = y = z = 0
        self.cur = self.__GetConnect()

        if len(args) == 0:
            # 查看所有表结构
            self.cur.execute('select TABLE_NAME,TABLE_COMMENT from information_schema.`TABLES` where table_schema="%s" ' % self.varDB)
            tblName = self.cur.fetchall()
            for k in range(len(tblName)):
                self.cur.execute('select column_name,column_type,is_nullable,column_comment from information_schema.`COLUMNS` where table_schema="%s" and table_name="%s" ' % (self.varDB, tblName[k][0]))
                tblFields = self.cur.fetchall()
                # print(u"\033[1;34;40m", 'printGreen', "\n" + "*" * 50 + " " + tblName[k][0] + "(" + tblName[k][1] + " ) > " + str(len(tblFields)) + "个字段 " + "*" * 50 )
                for i in tblFields:
                    # 字段与类型对齐
                    if len(i[0]) > x: x = len(i[0])
                    if len(i[1]) > y: y = len(i[1])
                    if len(i[2]) > z: z = len(i[2])
                print("*" * 100 + "\n" + tblName[k][0] + "(" + tblName[k][1] + " ) - " + str(len(tblFields)) + "个字段 " + "\n字段" + " " * (x - 3),"类型" + " " * (y - 3),  "可空" + " " * 4, "注释")
                for i in tblFields:
                    l_name.append(i[0] + " " * (x - len(i[0]) + 1))
                    l_type.append(i[1] + " " * (y - len(i[1]) + 1))
                    l_isnull.append(i[2] + " " * (z - len(i[2]) + 5))
                    l_comment.append(i[3].replace("\r\n", ",").replace("  ", ""))
                for i in range(len(tblFields)):
                    print(l_name[i], l_type[i], l_isnull[i], l_comment[i])
                l_name = []
                l_type = []
                l_isnull = []
                l_comment = []
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
                    print("[errorrrrrrr , 数据库(" + self.varDB + ")中没有找到 " + varTable.split("*")[0] + " 前缀的表!]")
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
                    print("[errorrrrrrr , 数据库(" + self.varDB + ")中没有找到 " + varTable + "表!]")
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
                        print("*" * 100 + "\n" + varTable + "(" + tblDDL[0] + ") - " + str(
                            len(tblFields)) + "个字段 " + "\n字段" + " " * (x - 3), "类型" + " " * (y - 3), "可空" + " " * 4,
                              "注释")
                        for i in tblFields:
                            l_name.append(i[0] + " " * (x - len(i[0]) + 1))
                            l_type.append(i[1] + " " * (y - len(i[1]) + 1))
                            l_isnull.append(i[2] + " " * (z - len(i[2]) + 6))
                            l_comment.append(i[3].replace("\r\n", ",").replace("  ", ""))

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

if __name__ == '__main__':

    # Sqlserver_PO = SqlServerPO("192.168.0.195", "DBuser", "qwer#@!", "bmlpimpro")  # PIM 测试环境
    # l_result = Sqlserver_PO.ExecQuery('select receiptNo from t_ph_outin_info where receiptType=%s ' % (15))
    # print(len(l_result))
    # print(l_result)
    # print(l_result[1])
    # for (Value) in l_result:
    #     print(Value)


    Sqlserver_PO = SqlServerPO("192.168.0.35", "test", "123456", "healthcontrol_test")  # EHR质控 测试环境

    # Sqlserver_PO.dbDesc()  # 所有表结构
    Sqlserver_PO.dbDesc('CommonDictionary')   # 某个表结构
    # Sqlserver_PO.dbDesc('Upms*')  # 查看所有b开头的表结构（通配符*） ??? 错误函数
    # Sqlserver_PO.dbDesc('HrPersonBasicInfo', 'personid,Id,Name')   # 某表的部分字段
    # Sqlserver_PO.dbDesc('b*', 'id,page')  # 查看所有b开头的表中id字段的结构（通配符*）

    # Sqlserver_PO.dbRecord('CommonDictionary', 'varchar', '%录音%')  # 搜索指定表符合条件的记录.
    # Sqlserver_PO.dbRecord('*', 'varchar', '%居委会%')  # 搜索所有表符合条件的记录.
    # Sqlserver_PO.dbRecord('*', 'money', '%34.5%')
    # Sqlserver_PO.dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
    # Sqlserver_PO.dbRecord('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。




