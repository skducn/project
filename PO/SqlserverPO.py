# -- coding: utf-8 --
# ***************************************************************
# Author     : John
# Data       : 2019-04-16
# Description: SqlServerPO 对象层
# /usr/local/pip3.7 install pymssql
# sql server 查询数据库所有的表名 + 字段  https://www.cnblogs.com/TF12138/p/4064752.html

# todo pymssql
# pymssql官网：http://www.pymssql.org/en/stable/index.html
# 官方API：http://www.pymssql.org/en/stable/ref/pymssql.html
# pymssql是基于_mssql模块做的封装，是为了遵守python的DBAPI规范接口
# python连接sql server数据库实现增删改查 https://www.cnblogs.com/malcolmfeng/p/6909293.html
# pymssql 托管在Github上：https://github.com/pymssql

# todo 乱码
# Q1，dbeaver工具中数据库表中的中文在pymssql查询输出却是乱码。
# 分析：默认情况下SqlServer使用ISO字符集（latin1字符集），而pymssql模块默认utf编码方式解码，数据库中的中文被python以二进制方式读取后以utf8方式解码显示为乱码，其二进制数据未改变。
# 解决：str.encode('latin1').decode('GB2312')
# 注意：windows系统上有此问题，而mac上无此问题。

# Q2：数据库中中文显示乱码，但查询后中文正确显示。
# 解决：在pymssql.Connect中添加 charset='utf8' ,确保 charset 与数据库编码一致，如数据库是gb2312 , 则charset='gb2312'。
# conn = pymssql.Connect(host='localhost', user='root', passwd='root', db='python',charset='utf8')

# Q3：数据库排序规则是Chinese_PRC_CI_AS, 可以使用GB18030读取得到中文。
# 分析：至于为什么不用GB2312呢，因为包含的字符个数：GB2312 < GBK < GB18030，如果用GB2312，在可能报错：“UnicodeDecodeError: 'gb2312' codec can't decode byte 0xa9 in position 0: illegal multibyte sequence”
# create_engine("mssql+pymssql://" + self.user + ":" + self.password + "@" + self.server + "/" + self.database + "?charset=GB18030")

# Q4：读取SQLSERVER数据库中文显示乱码问题。
# 分析：由数据库中的字段的类型问题导致, 如：varchar显示乱码而 ncarchar正常
# 解决：在select语句中直接通过 convert(nvarchar(20), remark) 转换。

# todo 报错
# Q5：Cannot insert explicit value for identity column in table 't' when identity_insert is set to OFF
# 分析：当 identity insert 设置为 off 时，无法为表中的标识列插入显式值，就是自增设置了off后，不能手动在唯一索引上添加值。
# 解决：
# set identity_insert[tableName] on
# inset ...
# set identity_insert[tableName] off

# todo 数据库中的NULL
# SQLserver中，NULL表示缺失或未知的数据
# python中，没有NULL，只有None，None的类型为NoneType ，None是一个对象。
# None不等于0、""(空字符串)、False等。
# 在Python中，None、0、""(空字符串)、[](空列表)、()(空元组)、{}(空字典)都是 False

# Sqlserver中判断NULL值
# select * from table where name IS NOT NULL   //判断name列不为空的值
# select * from table where name IS NULL

# coalesce函数，简化对多个列或表达式进行判断的过程。
# select * from 健康干预 where coalesce(hitQty,'1') = 2  //条件是hitQty=2的值

# todo sqlalchemy中create_engine用法 (https://blog.csdn.net/xc_zhou/article/details/118829588)
# engine = create_engine('数据库类型+驱动://用户名:密码@服务器IP:端口/数据库?charset=utf8')
# pymssql:
# engine = create_engine('mssql+pymssql://scott:tiger@hostname:port/dbname')
# Microsoft SQL Server:
# engine = create_engine('mssql+pyodbc://scott:tiger@mydsn')
# SQLite:
# engine = create_engine('sqlite:///foo.db')
# engine = create_engine('sqlite:absolute/path/to/foo.db')

# sqlalchemy+pandas：错误 'OptionEngine' object has no attribute 'execute'，'str' object has no attribute '_execute_on_connection'
# https://www.cnblogs.com/bruce-he/p/17113269.html

#SqlServer判断表、列不存在则创建 &&ExecuteNonQuery 要求命令拥有事务
# https://blog.csdn.net/Andrewniu/article/details/78028207
# ***************************************************************

"""
1.1 查询sql语句 execQuery(self, sql)
1.2 查询带参数sql execQueryParam(self, sql, param)
1.3 执行sql语句 execute(self, varTable, sql)
1.4 执行存储过程 execProcedure(self, varProcedureName)
1.5.1 执行sql文件 execSqlFile(self, varPathSqlFile)
1.5.2 执行sql文件2 execSqlFile2(self, varPathSqlFile)
1.6 close

2.1 获取所有表  getTables(self)
2.2 获取所有表和表注释 getTableAndComment(self)
2.3 获取表的结构信息 getStructure(self, varTable[all])
2.4 获取字段  getFields(self, varTable)
2.5 获取字段和字段注释 getFieldInfor(self, varTable)
2.6 获取记录数 getRecordQty(self, varTable)
2.7 获取所有字段和类型 getFieldAndType(self, varTable)
2.8 获取N个字段和类型 getOneFieldAndType(self, varTable, varField)
2.9 获取所有必填项字段和类型 getNotNullFieldAndType（self, varTable）
2.10 获取自增主键 getIdentityPrimaryKey(self, varTable)
2.11 获取主键  getPrimaryKey（self, varTable）
2.12 获取主键最大值 getPrimaryKeyMaxValue（self, varTable

3.1 创建表 crtTable(self, varTable, sql)
3.2 生成类型值 _genTypeValue(self, varTable)
3.3 生成必填项类型值 _genNotNullTypeValue(self, varTable)
3.4 单表自动生成第一条数据 genFirstRecord(self, varTable)
3.5 所有表自动生成第一条数据 genFirstRecordByAll()
3.6 自动生成数据 genRecord(self, varTable)
3.7 自动生成必填项数据 genRecordByNotNull(self, varTable)
3.8 执行insert _execInsert(self, varTable, d_init,{})

4.1 判断表是否存在 isTable(self, varTable)
4.2 判断字段是否存在 isField(self, varTable, varField)
4.3 判断是否有自增主键 isIdentity(self, varTable)

5.1.1 csv2dbByType()  csv2db自定义字段类型
5.1.2 csv2dbByAutoType()  csv2db自动生成字段类型
5.2 exls2db  excel导入数据库
5.3 dict2db
5.4 list2db
5.5 db2csv
5.6 db2xlsx
5.7 db2dict


应用
1 查看数据库表结构（字段、类型、大小、可空、注释），注意，表名区分大小写  dbDesc()
2 查找记录  dbRecord('*', 'money', '%34.5%')

"""
import pandas as pd
import petl as etl
import sys
from collections.abc import Iterable, Iterator
# from collections.abc import pymssql
import pymssql
from time import sleep
# print(pymssql.__version__)
# from adodbapi import connect
from sqlalchemy import create_engine, text

from PO.ColorPO import *
Color_PO = ColorPO()

from PO.TimePO import *
Time_PO = TimePO()


class SqlServerPO:

    def __init__(self, server, user, password, database, charset="utf8"):

        self.server = server
        self.user = user
        self.password = password
        self.database = database
        self.conn = pymssql.connect(
            server=server, user=user, password=password, database=database, charset=charset,
            as_dict=True, tds_version="7.3", autocommit=True,
        )
        # 注意：autocommit=True
        # pymssql默认关闭自动模式开启事务行为浅析 https://www.cnblogs.com/kerrycode/p/11391832.html
        # self.conn = pymssql.connect(server=server, user=user, password=password, database=database, charset='GB2312', autocommit=True)
        # self.conn = pymssql.connect(server=server, user=user, password=password, database=database, charset='GB18030', autocommit=True)
        # self.conn = pymssql.connect(server=server, user=user, password=password, database=database, charset='GBK', autocommit=True)
        # self.conn = pymssql.connect(server=server, user=user, password=password, database=database, charset='CP936', autocommit=True, login_timeout=10)
        # self.conn = connect('Provider=SQLOLEDB.1;Data Source=%s;Initial Catalog=%s;UserID = %s;Password = %s;'%(server, database, user, password))

        self.cur = self.conn.cursor()
        if not self.cur:
            raise (NameError, "error，创建游标失败！")

    def getEngine_pyodbc(self):
        # pyodbc 引擎
        return create_engine("mssql+pyodbc://" + self.user + ":" + self.password + "@mydsn")

    def getEngine_pymssql(self):
        # pymssql 引擎
        # return create_engine("mssql+pymssql://" + self.user + ":" + self.password + "@" + self.server + ":" + str(self.port) + "/" + self.database)
        return create_engine("mssql+pymssql://" + self.user + ":" + self.password + "@" + self.server + "/" + self.database)


    def execQuery(self, sql):

        '''1.1 查询sql'''

        try:
            self.conn.commit()
            self.cur.execute(sql)
            self.conn.commit()
            result = self.cur.fetchall()
            # print("[ok], " + sql)
            return result
        except Exception as e:
            # print(e.args)  # ('table hh already exists',)
            # print(str(e))  # table hh already exists
            # print(NameError(e))  # table hh already exists
            print(repr(e))  # OperationalError('table hh already exists')

    def execQueryParam(self, sql, param):

        '''
        1.2 带参查询sql， 返回一个包含tuple的list，list是元素的记录行，tuple记录每行的字段数值
        :param sql:
        :param param:
        :return:
        '''

        self.conn.commit()  # 用于新增后立即查询
        self.cur.execute(sql, param)
        try:
            result = self.cur.fetchall()
        except:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            return
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        return result

    def execute(self, sql):

        '''
        1.3 执行sql （insert，update）
        :param sql:
        :return:
        '''

        try:
            self.cur.execute(sql)
            self.conn.commit()
            return "ok"
        except Exception as e:
            # print(e.args)  # ('table hh already exists',)
            # print(str(e))  # table hh already exists
            # print(NameError(e))  # table hh already exists
            # print(repr(e))  # OperationalError('table hh already exists')
            return str(e)

    # 1.4 执行存储过程
    def execProcedure(self, varProcedureName):

        '''
        执行存储过程
        :param varProcedureName:
        :return:
        '''

        # execProcedure(存储过程名)

        # cur = self.__GetConnect()
        # sql =[]
        # sql.append("exec procontrol")
        # cur.callproc(varProcedureName)
        self.cur.execute(varProcedureName)
        self.conn.commit()
        self.cur.close()  # 关闭游标
        self.conn.close()  # 关闭连接

    # 1.5.1 执行sql文件
    def execSqlFile(self, varPathSqlFile):

        '''
        执行sql文件
        :param varPathSqlFile:
        :return:
        '''

        # execSqlFile('D:\\51\\python\\project\\instance\\zyjk\\EHR\\controlRule\\mm.sql')
        # cur = self.__GetConnect()
        with open(varPathSqlFile) as f:
            sql = f.read()
            self.cur.execute(sql)
            self.conn.commit()
            self.conn.close()

    # 1.5.2 执行sql文件2
    def execSqlFile2(self, varPathSqlFile):

        """执行sql文件语句2"""

        # cur = self.__GetConnect()
        with open(varPathSqlFile) as f:
            sql = f.read()
            self.cur.execute(sql)
            self.cur.nextset()
            # cur.callproc(sql,(1,2))
            # self.conn.commit()
            self.conn.close()

    # 1.6 关闭
    def close(self):
        self.cur.close()
        self.conn.close()



    def getTables(self):

        '''
        2.1 获取所有表
        :return:
        '''

        try:
            r = self.execQuery("SELECT DISTINCT d.name FROM syscolumns a LEFT JOIN systypes b ON a.xusertype= b.xusertype INNER JOIN sysobjects d ON a.id= d.id AND d.xtype= 'U' AND d.name<> 'dtproperties' LEFT JOIN syscomments e ON a.cdefault= e.id LEFT JOIN sys.extended_properties g ON a.id= G.major_id AND a.colid= g.minor_id LEFT JOIN sys.extended_properties f ON d.id= f.major_id AND f.minor_id= 0")
            # print(r)  # [{'name': 'EMR_ADMISSION_ASSESSMENT'}, {'name': 'EMR_ADMISSION_DEAD_RECORD_TF'},...]
            l_tables = []
            for i in range(len(r)):
                l_tables.append(r[i]['name'])
            return l_tables
        except Exception as e:
            print(e, ",[error], SqlserverPO.getTables()异常!")
            self.conn.close()


    def getTableComment(self, varTable="allTables"):

        '''
        2.2 获取所有表和表注释
        :return: 字典格式 ，如{'ASSESS_DIAGNOSIS': '门诊数据', 'ASSESS_MEDICATION': '评估用药情况表'}
        '''
        if varTable == "allTables":
            try:    
                r = self.execQuery("SELECT DISTINCT d.name,f.value FROM syscolumns a LEFT JOIN systypes b ON a.xusertype= b.xusertype INNER JOIN sysobjects d ON a.id= d.id AND d.xtype= 'U' AND d.name<> 'dtproperties' LEFT JOIN syscomments e ON a.cdefault= e.id LEFT JOIN sys.extended_properties g ON a.id= G.major_id AND a.colid= g.minor_id LEFT JOIN sys.extended_properties f ON d.id= f.major_id AND f.minor_id= 0")
                # print(r)  # [{'name': 'aaa', 'value': None}, {'name': 'bbb', 'value': None}...]
                l_table = []
                l_comment = []
                d = {}
                for i in range(len(r)):
                    l_table.append(r[i]['name'])
                    if r[i]['value'] == None:
                        l_comment.append(r[i]['value'])
                    else:
                        l_comment.append(r[i]['value'].decode(encoding="utf-8", errors="strict"))
                d = dict(zip(l_table, l_comment))
                # print(d)
                return d
            except Exception as e:
                print(e, ",[error], SqlserverPO.getTableComment()异常!")
                self.conn.close()
        else:
            try:
                r = self.execQuery("SELECT DISTINCT d.name,f.value FROM syscolumns a LEFT JOIN systypes b ON a.xusertype= b.xusertype INNER JOIN sysobjects d ON a.id= d.id AND d.xtype= 'U' AND d.name<> 'dtproperties' LEFT JOIN syscomments e ON a.cdefault= e.id LEFT JOIN sys.extended_properties g ON a.id= G.major_id AND a.colid= g.minor_id LEFT JOIN sys.extended_properties f ON d.id= f.major_id AND f.minor_id= 0")
                # print(r)  # [{'name': 'aaa', 'value': None}, {'name': 'bbb', 'value': None}...]
                l_table = []
                l_comment = []
                d = {}
                for i in range(len(r)):
                    if r[i]['name'] == varTable:
                        l_table.append(r[i]['name'])
                        if r[i]['value'] == None:
                            l_comment.append(r[i]['value'])
                        else:
                            l_comment.append(r[i]['value'].decode(encoding="utf-8", errors="strict"))
                d = dict(zip(l_table, l_comment))
                # print(d)
                return d
            except Exception as e:
                print(e, ",[error], SqlserverPO.getTableComment()异常!")
                self.conn.close()


    def getStructure(self, varTable="allTables"):

        '''
        2.3 获取表的结构信息
        :param varTable: 所有表或单表
        :return: [{表：'','表注释:'', '字段序号':'', '字段':'', '': '', '主键': '√', '类型': 'int', '占用字节数': 4, '长度': 10, '小数位数': 0, '允许空': '', '默认值': '', '字段注释': b''},{}...]
        其他用法：将如下查询内容，在navicate中执行，并导出excel文档。
        '''

        if varTable == "allTables":
            list1 = self.execQuery('''
            SELECT 表 = d.name,
              表注释 = isnull(f.value, ''),
              字段序号 = a.colorder,
              字段 = a.name,
              标识 = case when COLUMNPROPERTY(a.id, a.name, 'IsIdentity')= 1 then '√' else '' end,
              主键 = case when exists(SELECT 1 FROM sysobjects where xtype = 'PK' and parent_obj = a.id and name in (SELECT name FROM sysindexes WHERE indid in(SELECT indid FROM sysindexkeys WHERE id = a.id AND colid = a.colid))) then '√' else '' end,
              类型 = b.name,
              占用字节数 = a.length,
              长度 = COLUMNPROPERTY(a.id, a.name, 'PRECISION'),
              小数位数 = isnull(COLUMNPROPERTY(a.id, a.name, 'Scale'),0),
              允许空 = case when a.isnullable = 1 then '√' else '' end,
              默认值 = isnull(e.text, ''),
              字段注释 = isnull(g.[value], '')
            FROM
              syscolumns a
              left join systypes b on a.xusertype = b.xusertype
              inner join sysobjects d on a.id = d.id
              and d.xtype = 'U'
              and d.name<>'dtproperties'
              left join syscomments e on a.cdefault = e.id
              left join sys.extended_properties g on a.id = G.major_id
              and a.colid = g.minor_id
              left join sys.extended_properties f on d.id = f.major_id
              and f.minor_id = 0
            order by
              a.id,
              a.colorder
            ''')
        else:
            list1 = self.execQuery('''
            SELECT 表 = d.name ,
              表注释 =  isnull(f.value, '') ,
              字段序号 = a.colorder,
              字段 = a.name,
              标识 = case when COLUMNPROPERTY(a.id, a.name, 'IsIdentity')= 1 then '√' else '' end,
              主键 = case when exists(SELECT 1 FROM sysobjects where xtype = 'PK' and parent_obj = a.id and name in (SELECT name FROM sysindexes WHERE indid in(SELECT indid FROM sysindexkeys WHERE id = a.id AND colid = a.colid))) then '√' else '' end,
              类型 = b.name,
              占用字节数 = a.length,
              长度 = COLUMNPROPERTY(a.id, a.name, 'PRECISION'),
              小数位数 = isnull(COLUMNPROPERTY(a.id, a.name, 'Scale'),0),
              允许空 = case when a.isnullable = 1 then '√' else '' end,
              默认值 = isnull(e.text, ''),
              字段注释 = isnull(g.value, '')
            FROM
              syscolumns a
              left join systypes b on a.xusertype = b.xusertype
              inner join sysobjects d on a.id = d.id
              and d.xtype = 'U'
              and d.name<>'dtproperties'
              left join syscomments e on a.cdefault = e.id
              left join sys.extended_properties g on a.id = G.major_id
              and a.colid = g.minor_id
              left join sys.extended_properties f on d.id = f.major_id
              and f.minor_id = 0
            where
                d.name = \'''' + varTable + '''\'
            order by
              a.id,
              a.colorder
            ''')

        for index, i in enumerate(list1):
            for k, v in i.items():
                if isinstance(v, bytes):
                    list1[index][k] = v.decode(encoding="utf-8", errors="strict")

        return list1



    def getFields(self, varTable):

        '''
        2.4 获取字段
        :param varTable:
        :return:
        '''

        try:
            r = self.execQuery(
                "SELECT B.name as name FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'"
                % (varTable)
            )
            # print(r)  # [{'name': 'CF_XM'}, {'name': 'CF_FMKS'},...]
            l_fields = []
            for i in range(len(r)):
                l_fields.append(r[i]['name'])
            return l_fields
        except Exception as e:
            print(e, ",[error], SqlserverPO.getFields()异常!")
            self.conn.close()


    def getFieldComment(self, varTable):

        '''
        2.5 获取字段和字段注释
        :param varTable:
        :return:
        '''

        try:
            r = self.execQuery(
                "SELECT B.name as name, C.value as comment FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'"
                % (varTable)
            )
            # print(r)  # [{'name': 'GHRQ', 'comment': b'\xe6\x8c\x8...]
            l_field = []
            l_comment = []
            d = {}
            for i in range(len(r)):
                l_field.append(r[i]['name'])
                if r[i]['comment'] == None:
                    l_comment.append(r[i]['comment'])
                else:
                    l_comment.append(r[i]['comment'].decode(encoding="utf-8", errors="strict"))
            d = dict(zip(l_field, l_comment))
            return d
        except Exception as e:
            print(e, ",[error], SqlserverPO.getFields()异常!")
            self.conn.close()



    def getRecordQty(self, varTable):

        '''
        2.6 获取记录数（特别适合大数据）
        :param varTable:
        :return:
        '''

        qty = self.execQuery(
            "SELECT rows FROM sysindexes WHERE id = OBJECT_ID('" + varTable + "') AND indid < 2")
        return qty[0]['rows']


    def getFieldAndType(self, varTable):

        '''
        2.6 获取字段和类型
        :param varTable:
        :return:
        '''

        d_fields = {}
        result = self.execQuery(
            "SELECT A.name as tableName, B.name as Name, d.name as Type, B.max_length as Size, B.is_nullable as NotNull, C.value as Comment FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s' order by B.column_id asc"
            % (varTable)
        )
        # print(result) # [{'tableName': 'aaa', 'Name': 'ID', 'Type': 'int', 'Size': 4, 'NotNull': False, 'Comment': None},...]
        try:
            for i in result:
                 d_fields[str(i['Name'])] = str(i['Type'])
        except Exception as e:
            raise e
        return d_fields


    def getMoreFieldAndType(self, varTable, l_field):

        '''
        2.8 获取N个字段和类型
        :param varTable:
        :param varField:
        :return:
        '''

        d_result = self.getFieldAndType(varTable)
        # print(d_result) # {'ID': 'int', 'NAME': 'text', 'AGE': 'int', 'ADDRESS': 'char', 'SALARY': 'float'}

        list1 = []
        d = {}
        for k, v in d_result.items():
            for j in range(len(l_field)):
                if k == l_field[j]:
                    d[k] = v
        return d  # [{'field': 'ID', 'type': 'int'}, {'field': 'AGE', 'type': 'int'}]


    def getNotNullFieldAndType(self, varTable):

        '''
        2.9 获取必填项字段和类型
        :param varTable:
        :return:
        '''

        d_fields = {}
        result = self.execQuery(
            "SELECT A.name as tableName, B.name as Name, d.name as Type, B.max_length as Size, B.is_nullable as NotNull, C.value as Comment FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s' order by B.column_id asc"
            % (varTable)
        )
        try:
            for i in result:
                if i['NotNull'] == False :
                    d_fields[str(i['Name'])] = str(i['Type'])
        except Exception as e:
            raise e
        return d_fields  # {'ID': 'int', 'NAME': 'text', 'AGE': 'int', 'ADDRESS': 'char'}


    def getIdentityPrimaryKey(self, varTable):

        '''
        2.10 获取自增主键
        :param varTable:
        :return:
        '''

        l_field = self.execQuery("select * from sys.identity_columns where [object_id]= OBJECT_ID('" + varTable + "')")
        # print(l_field)
        if l_field != []:
            return (l_field[0]['name'])  # id
        else:
            return None


    def getPrimaryKey(self, varTable):

        '''
        2.11 获取主键
        :param varTable:
        :return:
        '''

        l_primaryKey = self.execQuery("SELECT COLUMN_NAME FROM information_schema.key_column_usage where table_name='" + varTable + "'")
        # print(l_primaryKey)  # [{'COLUMN_NAME': 'ADDRESS'}, {'COLUMN_NAME': 'ID'}]
        if l_primaryKey == [] :
            return None
        else:
            return l_primaryKey


    def getPrimaryKeyMaxValue(self, varTable):

        '''
        2.12 获取表主键最大值
        :param varTable:
        :return:
        '''

        # 判断表中是否有记录
        varQty = self.getRecordQty(varTable)
        if varQty != 0 :
            # 判断是否有主键
            l_primaryKey = self.getPrimaryKey(varTable)
            if l_primaryKey != None:
                # 当有一个主键时，
                # print(l_primaryKey)  # [{'COLUMN_NAME': 'id'}]
                if len(l_primaryKey) == 1 :
                    d = {}
                    # print(l_primaryKey[0]['COLUMN_NAME'])  # id
                    maxValue = self.execQuery("select max(" + str(l_primaryKey[0]['COLUMN_NAME']) + ") as name from " + varTable)
                    d[l_primaryKey[0]['COLUMN_NAME']] = maxValue[0]['name']
                    return (d)  # {'ID': 1}
                else:
                    # 多个主键
                    pass
                    # print(l_primaryKey)  # [{'name': 'ID'}, {'name': 'ADDRESS'}]  //1个主键




    def crtTable(self, varTable, sql):

        '''
        3.1 创建表
        :param varTable : test99
        :param sql: id INTEGER PRIMARY KEY, name TEXT, age INTEGER
        :return:
        '''

        # Sqlserver_PO.execute('''if not exists (select * from sysobjects where id = object_id('test99') and OBJECTPROPERTY(id, 'IsUserTable') = 1)create table test99(id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

        sql = "if not exists (select * from sysobjects where id = object_id('" + varTable + "') and OBJECTPROPERTY(id, 'IsUserTable') = 1)create table " + varTable + "(" + sql + ")"
        print(sql)
        self.execute(sql)


    def _genTypeValue(self, varTable):

        '''
        3.2 生成类型值
        :param varTable:
        :return:
        '''

        # 获取所有字段和类型
        d = self.getFieldAndType(varTable)
        # print(d)  # {'id': 'int', 'name': 'varchar', 'age': 'int'}

        # 初始化对应类型的值
        d_init = {}
        for k, v in d.items():
            if v == 'tinyint' or v == 'smallint' or v == 'int' or v == 'bigint':
                d_init[k] = 1
            elif v == 'float' or v == 'real':
                d_init[k] = 1.00
            elif v == 'numeric' or v == 'decimal':
                d_init[k] = 1
            elif v == 'money' or v == 'smallmoney':
                d_init[k] = 1
            elif v == 'char' or v == 'varchar' or v == 'nchar' or v == 'nvarchar' or v == 'text':
                d_init[k] = 'a'
            elif v == 'datetime' or v == 'smalldatetime' or v == 'datetime2':
                d_init[k] = Time_PO.getDateTimeByPeriod(0)
            elif v == 'time':
                d_init[k] = '08:12:23'
            elif v == 'date':
                d_init[k] = Time_PO.getDateByMinus()
        # print(d1)  # {'id': 1, 'name': 'a', 'age': 1}
        return d_init

    def _genNotNullTypeValue(self, varTable):

        '''
        3.3 生成必填项类型值
        :param varTable:
        :return:
        '''
        # 获取所有字段和类型
        d = self.getNotNullFieldAndType(varTable)
        # print(d)  # {'id': 'int', 'name': 'varchar', 'age': 'int'}

        # 初始化对应类型的值
        d_init = {}
        for k, v in d.items():
            if v == 'tinyint' or v == 'smallint' or v == 'int' or v == 'bigint':
                d_init[k] = 1
            elif v == 'float' or v == 'real':
                d_init[k] = 1.00
            elif v == 'numeric' or v == 'decimal':
                d_init[k] = 1
            elif v == 'money' or v == 'smallmoney':
                d_init[k] = 1
            elif v == 'char' or v == 'varchar' or v == 'nchar' or v == 'nvarchar' or v == 'text':
                d_init[k] = 'a'
            elif v == 'datetime' or v == 'smalldatetime' or v == 'datetime2':
                d_init[k] = '2020-12-12 09:12:23'
            elif v == 'time':
                d_init[k] = '08:12:23'
            elif v == 'date':
                d_init[k] = '2019-11-27'
        # print(d1)  # {'id': 1, 'name': 'a', 'age': 1}
        return d_init

    def genFirstRecord(self, varTable):

        '''
        3.4 单表自动生成第一条数据
        :param varTable:
        :return:
        '''

        # 判断表是否存在
        if self.isTable(varTable) == True:
            # 判断是否有记录
            qty = self.getRecordQty(varTable)
            if qty == 0:

                print(varTable)

                # 获取生成类型值
                d_init = self._genTypeValue(varTable)
                # print(d_init)
                # 执行insert
                self._execInsert(varTable, d_init,{})



                return True
            else:
                return False

    def genFirstRecordByAll(self):

        '''
        3。5 所有表自动生成第一条数据
        :return:
        '''
        r = self.getTables()
        # print(r)
        for i in range(len(r)):
            self.genFirstRecord(r[i])

    def genRecord(self, varTable, d_field={}):

        '''
        3.6 自动生成数据
        :param varTbl:
        :param d_field: 可以设置字段的值，如："ID = 123" ， 但不能设置主键
        Sqlserver_PO.genRecord("TB_HIS_MZ_Reg", {"GTHBZ": None, "GHRQ":"777"})  # 自动生成数据
        :return:
        '''

        if self.genFirstRecord(varTable) == False:

            # 判断表是否存在
            if self.isTable(varTable) == True:

                # 获取生成类型值
                d_init = self._genTypeValue(varTable)

                # 获取主键
                l_primaryKey = self.getPrimaryKey(varTable)
                # 没有主键
                if l_primaryKey != None:
                    primaryKey = l_primaryKey[0]['COLUMN_NAME']

                    # 获取主键最大值
                    d_primaryKey = self.getPrimaryKeyMaxValue(varTable)
                    # print(d_primaryKey)  # {'id': 39}
                    # print(d_primaryKey[primaryKey])  # 39
                    # 修改主键最大值+1
                    d_init[primaryKey] = d_primaryKey[primaryKey] + 1
                    # print(d1)  # {'id': 40, 'name': 'a', 'age': 1}


                # 执行insert
                self._execInsert(varTable, d_init, d_field)

    def genRecordByNotNull(self, varTable):

        '''
        3.7 自动生成必填项数据（非必填项忽略）
        :param varTbl:
        :return:
        '''

        if self.genFirstRecord(varTable) == False:

            # 判断表是否存在
            if self.isTable(varTable) == True:

                # 生成必填项类型值
                d_init = self._genNotNullTypeValue(varTable)

                # 获取主键
                l_primaryKey = self.getPrimaryKey(varTable)
                # print(l_primaryKey[0]['COLUMN_NAME'])  # ID
                primaryKey = l_primaryKey[0]['COLUMN_NAME']

                # 获取主键最大值
                d_primaryKey = self.getPrimaryKeyMaxValue(varTable)
                # print(d_primaryKey)  # {'id': 39}
                # print(d_primaryKey[primaryKey])  # 39
                # 修改主键最大值+1
                d_init[primaryKey] = d_primaryKey[primaryKey] + 1
                # print(d_init)  # {'id': 40, 'name': 'a', 'age': 1}

                # 执行insert
                self._execInsert(varTable, d_init,{})

    def _execInsert(self, varTable, d_init, d_field):

        '''
        3.8 执行insert
        :param varTable:
        :param d_init:
        :return:
        '''

        if d_field != {}:
            for k, v in d_field.items():
                for k1, v1 in d_init.items():
                    if k == k1 :
                        d_init[k] = v
            # print(d_init)  # {'GHRQ': 'a', 'GHBM': 'a', 'GTHBZ': 'a', ...}

        # 将d_init转换成insert语句的字段名及值
        s = ""
        u = ""
        for k, v in d_init.items():
            s = s + k + ","
            u = u + "'" + str(v) + "',"
        s = s[:-1]
        u = u[:-1]

        # 判断是否有自增列，如果有则返回1，无则返回0
        qty = self.execQuery("Select OBJECTPROPERTY(OBJECT_ID('" + varTable + "'),'TableHasIdentity') as qty")
        if qty[0]['qty'] == 1:
            self.execute('set identity_insert ' + str(varTable) + ' on')
            sql = "INSERT INTO " + str(varTable) + " (" + s + ") VALUES (" + u + ")"
            self.execute(varTable, sql)
            self.conn.commit()
            print("[ok], " + str(sql))
            self.execute('set identity_insert ' + str(varTable) + ' off')
        else:
            if 'None' in u :
                u = u.replace(",'None',", ",null,")
                sql = "INSERT INTO " + str(varTable) + " (" + s + ") VALUES (" + u + ")"
            else:

                sql = "INSERT INTO " + str(varTable) + " (" + s + ") VALUES (" + u + ")"
            self.execute(varTable, sql)
            self.conn.commit()
            print("[ok], " + str(sql))



    def isTable(self, varTable):

        '''
        4.1 判断表是否存在
        :param varTable:
        :return: 返回True或False
        '''

        r = self.execQuery("SELECT COUNT(*) c FROM SYSOBJECTS WHERE XTYPE = 'U' AND NAME='%s'" % (varTable))
        # print(r)  # [{'c': 1}]
        if r[0]['c'] == 1:
            return True
        else:
            return False

    def isField(self, varTable, varField):

        '''
        4.2 判断字段是否存在
        :param varTable:
        :param varField:
        :return: 返回True或False
        '''

        r = self.execQuery(
            "SELECT B.name as field FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'"
            % (varTable)
        )
        # print(r)  # [{'field': 'name'}, {'field': 'age'}, {'field': 'id'}]
        for i in range(len(r)):
            if r[i]['field'] == varField:
                return True
        return False

    def isIdentity(self, varTable):

        '''
        4.3 判断是否有自增主键, 如果有则返回1，无则返回0
        :param varTable:
        :return:
        '''

        qty = self.execQuery("Select OBJECTPROPERTY(OBJECT_ID('" + varTable + "'),'TableHasIdentity') as qty")
        # print(qty)  # [{'qty': 1}]
        # print(qty[0]['qty'])  # 1
        if qty[0]['qty'] == 1 :
            return True
        else:
            return False


    # todo 迁移

    def csv2dbByType(self, varPathFile, varDbTable, varFieldAndType):

        '''
        5.1.1 csv2db 自定义字段类型
        varPathFile = './data/test.csv'
        varDbTable = 'test000'
        varFieldAndType = 'id INTEGER PRIMARY KEY, name TEXT, age INTEGER'
        csv2dbBy
        '''

        try:
            data = etl.fromcsv(varPathFile)
            self.crtTable(varDbTable, varFieldAndType)  # 创建表
            etl.todb(data, self.conn, varDbTable)
        except Exception as e:
            print(e)

    def csv2dbByAutoType(self, varPathFile, varDbTable):

        '''
        5.1.2 csv2db 自动生成字段类型
        varTable = './data/test.csv'
        varFieldAndType = 'tableName'
        '''

        try:
            df = pd.read_csv(varPathFile, encoding='gbk')
            engine = self.getEngine_pymssql()
            df.to_sql(varDbTable, con=engine, if_exists="replace", index=False)
        except Exception as e:
            print(e)

    def xlsx2db(self, varPathFile, varDbTable, varSheetName=0):

        '''
        5.2，xlsx导入数据库
        :param varExcelFile: './data/test.xlsx'
        :param varTable:
        :return:
        xlsx2db('./data/2.xlsx', "jh123""sheet3",)
        excel表格第一行数据对应db表中字段，建议用英文
        '''

        try:
            df = pd.read_excel(varPathFile, sheet_name=varSheetName)
            engine = self.getEngine_pymssql()
            df.to_sql(varDbTable, con=engine, if_exists="replace", index=False)
            # pd.read
        except Exception as e:
            print(e)


    def dict2db(self, varDict, varDbTable, index="True"):

        """5.3 字典导入数据库"""

        try:
            df = pd.DataFrame(varDict)
            engine = self.getEngine_pymssql()
            if index == "False":
                df.to_sql(name=varDbTable, con=engine, if_exists="replace", index=False)
            else:
                df.to_sql(name=varDbTable, con=engine, if_exists="replace")
        except Exception as e:
            print(e)

    def list2db(self, l_col, l_value, varDbTable, index="True"):

        """5.4 列表导入数据库
        l_col = 列名，如 ['id','name','age']
        l_value= 值,如 [['1','john','44],['2','ti','4']]
        """

        try:

            df = pd.DataFrame(l_value, columns=l_col)
            engine = self.getEngine_pymssql()
            if index == "False":
                df.to_sql(name=varDbTable, con=engine, if_exists="replace", index=False)
            else:
                df.to_sql(name=varDbTable, con=engine, if_exists="replace")
        except Exception as e:
            print(e)


    def db2csv(self, sql, varExcelFile, header=1):

        """5.5 数据库转csv(含字段或不含字段)"""

        try:
            engine = self.getEngine_pymssql()
            df = pd.read_sql(text(sql), con= engine.connect())
            # header=None表示不含列名
            if header == None:
                df.to_csv(varExcelFile, index=None, header=None)
            else:
                df.to_csv(varExcelFile, index=None)
        except Exception as e:
            print(e)

    def db2xlsx(self, sql, varExcelFile, header=1):

        """5.6 数据库转xlsx(含字段或不含字段)"""

        try:
            engine = self.getEngine_pymssql()
            df = pd.read_sql(text(sql), con=engine.connect())
            # header=None表示不含列名
            if header == None:
                df.to_excel(varExcelFile, index=None, header=None)
            else:
                df.to_excel(varExcelFile, index=None)
        except Exception as e:
            print(e)

    def db2dict(self, sql, orient='list'):

        """5.7 db转字典"""

        try:
            engine = self.getEngine_pymssql()
            df = pd.read_sql(text(sql), con=engine.connect())
            return df.to_dict(orient=orient)

        except Exception as e:
            print(e)





    # todo 应用
    def _dbDesc_search(self, varTable=0, var_l_field=0):

        d_tableComment = {}
        l_field = []
        l_type = []
        l_isKey = []
        l_isnull = []
        l_comment = []

        if varTable == 0 and var_l_field == 0:
            # 1，所有表结构（ok）
            l_table_comment = self.execQuery(
                "SELECT DISTINCT d.name,f.value FROM syscolumns a LEFT JOIN systypes b ON a.xusertype= b.xusertype INNER JOIN sysobjects d ON a.id= d.id AND d.xtype= 'U' AND d.name<> 'dtproperties' LEFT JOIN syscomments e ON a.cdefault= e.id LEFT JOIN sys.extended_properties g ON a.id= G.major_id AND a.colid= g.minor_id LEFT JOIN sys.extended_properties f ON d.id= f.major_id AND f.minor_id= 0"
            )
            # print(l_table_comment)

            # print(l_table_comment.decode('gbk')

        elif varTable == 0 and var_l_field != 0:
            # 6，所有表结构的可选字段(只输出找到字段的表) （ok）
            l_table_comment = self.execQuery(
                "SELECT DISTINCT d.name,f.value FROM syscolumns a LEFT JOIN systypes b ON a.xusertype= b.xusertype INNER JOIN sysobjects d ON a.id= d.id AND d.xtype= 'U' AND d.name<> 'dtproperties' LEFT JOIN syscomments e ON a.cdefault= e.id LEFT JOIN sys.extended_properties g ON a.id= G.major_id AND a.colid= g.minor_id LEFT JOIN sys.extended_properties f ON d.id= f.major_id AND f.minor_id= 0"
            )
        else:
            if "%" not in varTable:
                # 2，单表结构（ok）
                # 4，单表结构可选字段（ok）
                l_table_comment = self.execQuery(
                    "SELECT A.name, C.value FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'"
                    % (varTable)
                )
                # print(l_table_comment)

            elif "%" in varTable:
                # 3，带通配符表结构(ok)
                # 5，带通配符表结构可选字段(只输出找到字段的表) （ok）
                l_table_comment = self.execQuery(
                    "SELECT DISTINCT d.name,f.value FROM syscolumns a LEFT JOIN systypes b ON a.xusertype= b.xusertype INNER JOIN sysobjects d ON a.id= d.id AND d.xtype= 'U' AND d.name<> 'dtproperties' LEFT JOIN syscomments e ON a.cdefault= e.id LEFT JOIN sys.extended_properties g ON a.id= G.major_id AND a.colid= g.minor_id LEFT JOIN sys.extended_properties f ON d.id= f.major_id AND f.minor_id= 0 where d.name like '%s'"
                    % (varTable)
                )
        # print(b'\xd6\xf7\xbc\xfc\xd7\xd4\xd4\xf6'.decode('gbk'))
        for t in l_table_comment:

            if t['value'] != None:
                d_tableComment[t['name']] = t['value'].decode("gbk")
            else:
                d_tableComment[t['name']] = str(t['value'])

        # 字典表名 {Name：Comment}
        # print(d_tableComment)  # {'BACKUP_HISTORY': 'None', 'BACKUPINTERFACE': '拉取ITF的临时表', 'BACKUPQUALITYCONTROL': '拉取ITF数据使用的临时表')'

        # 遍历每个表，获取6个信息分别是： 表名，字段名，类型，大小，是否为空，注释
        for k, v in d_tableComment.items():
            varTable = k
            l_table_field_type_size_isNull_comment = self.execQuery(
                # "SELECT A.name, B.name, d.name, B.max_length, B.is_nullable, C.value FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'"
                "SELECT A.name as tableName, B.name as Name, d.name as Type, B.max_length as Size, B.is_nullable as NotNull, C.value as Comment FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s' order by B.column_id asc"
                % (varTable)
            )
            try:
                # 字段与类型对齐
                # print(l_table_field_type_size_isNull_comment)

                tblTableName = tblName = tblType = tblSize = tblNotNull = tblComment = 0
                # tblTableName = tblName = tblType = tblSize = tblNotNull = tblComment = 0
                for i in l_table_field_type_size_isNull_comment:

                    tblTableName = len(i['tableName'])
                    if len(str(i['Name'])) > tblName:
                        tblName = len(i['Name'])
                    if len(str(i['Type'])) > tblType:
                        tblType = len(i['Type'])
                    if len(str(i['Size'])) > tblSize:
                        tblSize = len(str(i['Size']))
                    if len(str(i['NotNull'])) > tblNotNull:
                        tblNotNull = len(str(i['NotNull']))
                    if len(str(i['Comment'])) > tblComment:
                        tblComment = len(str(i['Comment']))

                # print(tblName)

                if var_l_field != 0:
                    # print(var_l_field)
                    # print(l_table_field_type_size_isNull_comment)
                    # 可选字段
                    for l in range(len(var_l_field)):
                        for m in range(len(l_table_field_type_size_isNull_comment)):
                            if (
                                    var_l_field[l]
                                    == l_table_field_type_size_isNull_comment[m]['Name']
                            ):
                                l_field.append(
                                    str(l_table_field_type_size_isNull_comment[m]['Name'])
                                    + " "
                                    * (
                                            tblName
                                            - len(
                                        l_table_field_type_size_isNull_comment[m]['Name']
                                    )
                                            + 1
                                    )
                                )
                                l_type.append(
                                    str(l_table_field_type_size_isNull_comment[m]['Type'])
                                    + " "
                                    * (
                                            tblType
                                            - len(
                                        l_table_field_type_size_isNull_comment[m]['Type']
                                    )
                                            + 1
                                    )
                                )
                                l_isKey.append(
                                    str(l_table_field_type_size_isNull_comment[m]['Size'])
                                    + " "
                                    * (
                                            tblSize
                                            - len(
                                        str(
                                            l_table_field_type_size_isNull_comment[
                                                m
                                            ]['Size']
                                        )
                                    )
                                            + 1
                                    )
                                )
                                l_isnull.append(
                                    str(l_table_field_type_size_isNull_comment[m]['NotNull'])
                                    + " "
                                    * (
                                            tblNotNull
                                            - len(
                                        str(
                                            l_table_field_type_size_isNull_comment[
                                                m
                                            ]['NotNull']
                                        )
                                    )
                                            + 7
                                    )
                                )
                                if l_table_field_type_size_isNull_comment[m]['Comment'] == None:
                                    l_comment.append(
                                        str(
                                            l_table_field_type_size_isNull_comment[m]['Comment']
                                        )
                                        + " "
                                        * (
                                                tblComment
                                                - len(
                                            str(
                                                l_table_field_type_size_isNull_comment[
                                                    m
                                                ][
                                                    'Comment'
                                                ]
                                            )
                                        )
                                                + 1
                                        )
                                    )
                                else:
                                    l_comment.append(
                                        str(
                                            l_table_field_type_size_isNull_comment[m][
                                                'Comment'
                                            ].decode("GBK")
                                        )
                                        + " "
                                        * (
                                                tblComment
                                                - len(
                                            str(
                                                l_table_field_type_size_isNull_comment[
                                                    m
                                                ][
                                                    'Comment'
                                                ]
                                            )
                                        )
                                                + 1
                                        )
                                    )
                else:
                    # 所有字段
                    for i in l_table_field_type_size_isNull_comment:
                        l_field.append(str(i['Name']) + " " * (tblName - len(i['Name'])))
                        l_type.append(str(i['Type']) + " " * (tblType - len(i['Type'])))
                        l_isKey.append(str(i['Size']) + " " * (tblSize - len(str(i['Size'])) + 5))
                        l_isnull.append(str(i['NotNull']) + " " * (tblNotNull - len(str(i['NotNull'])) + 3))
                        if i['Comment'] == None:
                            l_comment.append(str(i['Comment']) + " " * (tblComment - len(str(i['Comment']))))
                        else:
                            l_comment.append(
                                str(i['Comment'].decode("GBK"))
                                + " " * (tblComment - len(str(i['Comment'])))
                            )

                # 只输出找到字段的表
                if len(l_field) != 0:
                    print("- - " * 20)
                    Color_PO.consoleColor(
                        "31",
                        "36",
                        "[Result] => TableName: "
                        + str(k)
                        + " ("
                        + str(d_tableComment[k])
                        + ") , "
                        + str(len(l_table_field_type_size_isNull_comment))
                        + "个字段",
                        "",
                    )

                    # print(
                    #     "Name" + " " * (tblName - len("Name")),
                    #     "Type" + " " * (tblType - len("Type")),
                    #     "Size" + " " * (tblSize - len("Size")+5),
                    #     "isNull" + " " * (tblNotNull - len("isNull")+3),
                    #     "Comment"
                    # )

                    Color_PO.consoleColor(
                        "31",
                        "36",
                        "Name" + " " * (tblName - len("Name") + 1) +
                        "Type" + " " * (tblType - len("Type") + 1) +
                        "Size" + " " * (tblSize - len("Size") + 6) +
                        "isNull" + " " * (tblNotNull - len("isNull") + 4) +
                        "Comment",
                        "",
                    )

                    for i in range(len(l_field)):
                        print(
                            l_field[i], l_type[i], l_isKey[i], l_isnull[i], l_comment[i]
                        )

                l_field = []
                l_type = []
                l_isKey = []
                l_isnull = []
                l_comment = []

            except Exception as e:
                raise e
        return len(d_tableComment)

    # 1, 查看数据库表结构（字段名、数据类型、大小、允许空值、字段说明）
    def dbDesc(self, *args):

        """1, 查看数据库表结构（字段名、数据类型、大小、允许空值、字段说明）"""
        # 注意，表名区分大小写
        # Sqlserver_PO.dbDesc()  # 1，所有表结构
        # Sqlserver_PO.dbDesc('tb_code_value')   # 2，某个表结构
        # Sqlserver_PO.dbDesc('tb_code_value', 'code,id,value')  # 3，某表的部分字段
        # Sqlserver_PO.dbDesc('tb*')  # 4，查看所有tb开头的表结构（通配符*）
        # Sqlserver_PO.dbDesc('tb*', 'id,page')  # 5，查看所有b开头的表中id字段的结构（通配符*）

        if len(args) == 0:
            # 1，所有表结构（ok）
            result = self._dbDesc_search()
            Color_PO.consoleColor(
                "31",
                "31",
                "\n[Result] => " + self.database + "数据库合计" + str(result) + "张表。",
                "",
            )
        elif len(args) == 1:
            # 2，单表结构 和 3，带通配符表结构 （ok）
            self._dbDesc_search(args[0])
        elif len(args) == 2:
            # 4，单表结构的可选字段 、 5，带通配符表结构的可选字段、6，所有表结构的可选字段
            self._dbDesc_search(args[0], args[1])


    def dbRecord(self, varTable, varType, varValue):

        """ 查找记录
        # 参数1：varTable = 表名（*表示所有的表）
        # 参数2：varType = 数据类型(char,int,double,timestamp)
        # 参数3：varValue = 值 (支持%模糊查询，如 %yy%)
        """
        # Sqlserver_PO.dbRecord('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
        # Sqlserver_PO.dbRecord('*', 'varchar', '%海鹰居委会%')
        # Sqlserver_PO.dbRecord('*', 'money', '%34.5%')
        # Sqlserver_PO.dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
        # Sqlserver_PO.dbRecord('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。


        # 支持的类型
        if (varType in "double,timestamp,float,money,int,nchar,nvarchar,datetime,varchar"):
            if "*" in varTable:
                # 遍历所有表
                l_d_tbl = self.execQuery("SELECT NAME FROM SYSOBJECTS WHERE TYPE='U'")
                # print(l_d_tbl)  # [{'NAME': 'TB_RIS_REPORT2'}, {'NAME': 'jh_jkpg'}, {'NAME': 'jh_jkgy'},,...]

                for b in range(len(l_d_tbl)):
                    # 遍历所有表的 列名称、列类别、类注释
                    tbl = l_d_tbl[b]['NAME']
                    l_d_field_type = self.execQuery(
                        "select syscolumns.name as field,systypes.name as type from syscolumns,systypes where syscolumns.xusertype=systypes.xusertype and syscolumns.id=object_id('%s')"
                        % (tbl)
                    )
                    # print(l_d_field_type)  # [{'field': 'GUID', 'type': 'varchar'}, {'field': 'VISITSTRNO', 'type': 'varchar'},...]

                    l_field = []
                    l_type = []
                    for j in l_d_field_type:
                        if varType in j['type']:
                            l_field.append(j['field'])
                            l_type.append(j['type'])

                    # print(l_field)  # ['GUID', 'VISITSTRNO', 'ORGCODE', 'ORGNAME',...]
                    # print(l_type)  # ['varchar', 'varchar', 'varchar', 'varchar' ...]

                    # 遍历所有字段
                    for i in range(len(l_field)):
                        l_result = self.execQuery("select * from %s where [%s] like '%s'" % (tbl, l_field[i], varValue))

                        if len(l_result) != 0:
                            print("--" * 50)
                            Color_PO.consoleColor("31", "36", "[result] => " + str(varValue) + " => " + tbl + " => " + l_field[i] + " => " + str(len(l_result)) + "条 ", "")

                            for j in range(len(l_result)):
                                print(l_result[j])
                                # print(str(l_result[j]).decode("utf8"))
                                # print(l_result[j].encode('latin-1').decode('utf8'))


            elif "*" not in varTable:
                # 搜索指定表（单表）符合条件的记录.  ，获取列名称、列类别、类注释

                # 获取表的Name和Type
                l_d_field_type = self.execQuery(
                    "select syscolumns.name as field,systypes.name as type from syscolumns,systypes where syscolumns.xusertype=systypes.xusertype and syscolumns.id=object_id('%s')"
                    % (varTable)
                )
                # print(l_d_field_type)  # [{'field': 'ID', 'type': 'int'}, {'field': 'ARCHIVENUM', 'type': 'varchar'}...]

                # 筛选符合条件（包含指定type）的field
                l_field = []
                for j in l_d_field_type:
                    if varType in j['type']:
                        l_field.append(j['field'])
                print(l_field)  # ['CZRYBM', 'CZRYXM', 'JMXM', 'SJHM', 'SFZH', 'JJDZ',...]

                # 遍历所有字段
                for i in range(len(l_field)):
                    l_result = self.execQuery("select * from %s where [%s] like '%s'" % (varTable, l_field[i], varValue))

                    if len(l_result) != 0:
                        print("--" * 50)
                        Color_PO.consoleColor("31", "36",
                                              "[result] => " + str(varValue) + " => " + varTable + " => " + l_field[
                                                  i] + " => " + str(len(l_result)) + "条 ", "")

                        for j in range(len(l_result)):
                            l_value = [value for value in l_result[j].values()]
                            # print(l_value)  # ['1015', '李*琳', '常*梅', '17717925118', '132222196702240429',...]
                            print(l_result[j])  # {'CZRYBM': '1015', 'CZRYXM': '李*琳', 'JMXM': '常*梅', 'SJHM': '17717925118', 'SFZH': '132222196702240429'...}

        else:
            print(
                "\n"
                + varType
                + "类型不存在，如：float,money,int,nchar,nvarchar,datetime,timestamp"
            )
        self.conn.close()


if __name__ == "__main__":

    # 区域平台 - 人民医院 ————————————————————————————————————————————————————————————————————————————————————————————————————————————
    Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "utf8")  # 测试环境


    # print("1.1 查询sql".center(100, "-"))
    # a = Sqlserver_PO.execQuery("select * from aaa")
    # print(a)

    # print("1.3 执行sql".center(100, "-"))
    # Sqlserver_PO.execute("aaa", "UPDATE aaa set AGE=20 where ID=4")  # 更新数据
    # Sqlserver_PO.execute("aaa", "drop table aaa")  # 删除表
    # Sqlserver_PO.execute("aaa", "truncate table aaa")  # 删除数据



    # print("2.1 获取所有表".center(100, "-"))
    # print(Sqlserver_PO.getTables())  # ['condition_item', 'patient_demographics', 'patient_diagnosis']

    # print("2.2 获取所有表和表注释".center(100, "-"))
    # print(Sqlserver_PO.getTableComment())  # {'ASSESS_DIAGNOSIS': '门诊数据', 'ASSESS_MEDICATION': '评估用药情况表',...}
    # print(Sqlserver_PO.getTableComment('ASSESS_MEDICATION'))  # {'ASSESS_DIAGNOSIS': '门诊数据', 'ASSESS_MEDICATION': '评估用药情况表',...}

    # print("2.3 获取表结构信息".center(100, "-"))
    # print(Sqlserver_PO.getStructure('test000'))
    # # print(Sqlserver_PO.getStructure())
    #
    # print("2.4 获取字段".center(100, "-"))
    # print(Sqlserver_PO.getFields('test000'))  # ['id', 'name', 'age']
    #
    # print("2.5 获取字段和字段注释".center(100, "-"))
    # print(Sqlserver_PO.getFieldComment('test000'))  # {'id': '编号ID', 'name': '姓名', 'age': '年龄'}
    #
    # print("2.6 获取记录数 ".center(100, "-"))
    # print(Sqlserver_PO.getRecordQty('test000'))  # 3

    # print("2.7 获取所有字段和类型 ".center(100, "-"))
    # print(Sqlserver_PO.getFieldAndType("test000"))  # {'ID': 'int', 'NAME': 'text', 'AGE': 'int', 'ADDRESS': 'char', 'SALARY': 'float'}
    #
    # print("2.8 获取N个字段和类型 ".center(100, "-"))
    # print(Sqlserver_PO.getMoreFieldAndType("test000", ["ID"]))  # {'ID': 'int'}
    # print(Sqlserver_PO.getMoreFieldAndType("test000", ["ID", 'AGE']))  # {'ID': 'int', 'AGE': 'int'}
    # #
    # print("2.9 获取必填项字段和类型".center(100, "-"))
    # print(Sqlserver_PO.getNotNullFieldAndType('test000'))  # {'ID': 'int', 'NAME': 'text', 'AGE': 'int', 'ADDRESS': 'char'}
    #
    # print("2.10 获取自增主键".center(100, "-"))
    # print(Sqlserver_PO.getIdentityPrimaryKey('test000'))  # None // 没有自增主键
    # print(Sqlserver_PO.getIdentityPrimaryKey('test000'))  # id
    # #
    # print("2.10 获取主键".center(100, "-"))
    # print(Sqlserver_PO.getPrimaryKey('test000'))  # [{'COLUMN_NAME': 'ADDRESS'}, {'COLUMN_NAME': 'ID'}]
    # print(Sqlserver_PO.getPrimaryKey('bbb'))  # [{'COLUMN_NAME': 'id'}]

    # print("2.11 获取表主键最大值 ".center(100, "-"))
    # print(Sqlserver_PO.getPrimaryKeyMaxValue('aaa'))  # {'ID': 9}
    # print(Sqlserver_PO.getPrimaryKeyMaxValue('bbb'))  # {'id': 4}



    # print("3.1 创建表（自增id主键）".center(100, "-"))
    # Sqlserver_PO.crtTable('bbb', ''''CREATE TABLE bbb (
    # id INT IDENTITY(1,1) PRIMARY KEY,
    # name VARCHAR(20) NOT NULL,
    # age INT NOT NULL) go''')

    # print("3.1 创建表（ID主键） ".center(100, "-"))
    # Sqlserver_PO.crtTable('aaa', '''CREATE TABLE aaa
    #        (ID INT PRIMARY KEY     NOT NULL,
    #         NAME           TEXT    NOT NULL,
    #         AGE            INT     NOT NULL,
    #         ADDRESS        CHAR(50),
    #         SALARY         REAL);''')

    # print("3.2 生成类型值".center(100, "-"))
    # print(Sqlserver_PO._genTypeValue("aaa"))  # {'ID': 1, 'NAME': 'a', 'AGE': 1, 'ADDRESS': 'a', 'SALARY': 1.0, 'time': '08:12:23'}

    # print("3.3 生成必填项类型值".center(100, "-"))
    # print(Sqlserver_PO._genNotNullTypeValue("aaa"))

    # print("3.4 单表自动生成第一条数据".center(100, "-"))
    # Sqlserver_PO.genFirstRecord('bbb')

    # print("3.5 所有表自动生成第一条数据".center(100, "-"))
    # Sqlserver_PO.genFirstRecordByAll()

    # print("3.6 自动生成数据".center(100, "-"))
    # Sqlserver_PO.genRecord('aaa')

    # print("3.7 自动生成必填项数据".center(100, "-"))
    # Sqlserver_PO.genRecordByNotNull('aaa')



    # # print("4.1 判断表是否存在".center(100, "-"))
    # print(Sqlserver_PO.isTable("aaa"))
    #
    # # print("4.2 判断字段是否存在(字段区分大小写)".center(100, "-"))
    # print(Sqlserver_PO.isField('bbb', 'id'))
    #
    # # print("4.3 判断是否有自增主键".center(100, "-"))
    # print(Sqlserver_PO.isIdentity('bbb'))
    # print(Sqlserver_PO.isIdentity('aaa'))



    # # print("5.1.1 csv2db自定义字段类型".center(100, "-"))
    # Sqlserver_PO.csv2dbByType('./data/test12.csv', "test555")

    # # print("5.1.2 csv2db自动生成字段类型".center(100, "-"))
    # Sqlserver_PO.csv2dbByAutoType('./data/test12.csv', "test555")

    # # print("5.2 excel导入数据库".center(100, "-"))
    # Sqlserver_PO.xlsx2db('./data/area.xlsx', "hello", "test333")

    # print("5.3 字典转数据库".center(100, "-"))
    # Sqlserver_PO.dict2db({'A': [3, 4, 8, 9], 'B': [1.2, 2.4, 4.5, 7.3], 'C': ["aa", "bb", "cc", "dd"]}, "test99")  # 带index
    # Sqlserver_PO.dict2db({'A': [3, 4, 8, 9], 'B': [1.2, 2.4, 4.5, 7.3], 'C': ["aa", "bb", "cc", "dd"]}, "test99", "False")  # 不带index

    # print("5.4 列表转数据库".center(100, "-"))
    # Sqlserver_PO.list2db(['name','age','sex'], [['1','2','3'],['a','b','c']], "test99")  # 生成index
    # Sqlserver_PO.list2db(['name','age','sex'], [['1','2','3'],['a','b','c']], "test99", "False")  # 不生成index

    # print("5.5 数据库转csv(含字段或不含字段)".center(100, "-"))
    # Sqlserver_PO.db2csv("SELECT * FROM test99", './data/test99.csv')
    # Sqlserver_PO.db2csv("SELECT * FROM test99", './data/test99.csv', None)  # 不导出字段名

    # print("5.6 数据库转xlsx(含字段或不含字段)".center(100, "-"))
    # Sqlserver_PO.db2xlsx("SELECT * FROM test99", './data/test99.xlsx')  # 导出字段
    # Sqlserver_PO.db2xlsx("SELECT * FROM test99", './data/test99.xlsx', None)  # 不导出字段

    print("5.7 db转字典".center(100, "-"))
    print(Sqlserver_PO.db2dict("SELECT * FROM test99")) # {'index': [0, 1], 'name': ['1', 'a'], 'age': ['2', 'b'], 'sex': ['3', 'c']}
    print(Sqlserver_PO.db2dict("SELECT * FROM test99", 'series'))
    # {'index': 0    0
    # 1    1
    # Name: index, dtype: int64, 'name': 0    1
    # 1    a
    # Name: name, dtype: object, 'age': 0    2
    # 1    b
    # Name: age, dtype: object, 'sex': 0    3
    # 1    c
    # Name: sex, dtype: object}


    # **********************************************************************************************************************************
    # **********************************************************************************************************************************

    # todo 应用

    # print("1 查看数据库表结构（字段、类型、大小、可空、注释）".center(100, "-"))
    # # Sqlserver_PO.dbDesc()  # 1，所有表结构
    # Sqlserver_PO.dbDesc("aaa")  # 2，单表结构
    # Sqlserver_PO.dbDesc('s%')  # 3，带通配符表结构
    # Sqlserver_PO.dbDesc('tb_org', ['id', 'org_name'])  # 4,单表结构的可选字段
    # Sqlserver_PO.dbDesc('s%', ['id', 'kaId'])  # 5，带通配符表结构的可选字段(只输出找到字段的表)
    # Sqlserver_PO.dbDesc(0, ['id', 'kaId', 'org_name'])  # 6，所有表结构的可选字段(只输出找到字段的表)

    # print("2 查找记录".center(100, "-"))
    # Sqlserver_PO.dbRecord('aaa', 'int', '%2%')  # 搜索指定表符合条件的记录.
    # Sqlserver_PO.dbRecord('*', 'varchar', '310101202308070001')  # 搜索所有表符合条件的记录.
    # Sqlserver_PO.dbRecord('QYYH', 'varchar', '132222196702240429')  # 搜索所有表符合条件的记录.
    # Sqlserver_PO.dbRecord('TB_RIS_REPORT2', 'varchar', '000E434B-48BF-4B58-945B-6FDCD46CDECE')  # 搜索所有表符合条件的记录.
    # Sqlserver_PO.dbRecord('*', 'money', '%34.5%')l
    # Sqlserver_PO.dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
    # Sqlserver_PO.dbRecord('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。


