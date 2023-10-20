# -- coding: utf-8 --
# ***************************************************************
# Author     : John
# Data       : 2019-04-16
# Description: SqlServerPO 对象层
# sql server 查询数据库所有的表名 + 字段  https://www.cnblogs.com/TF12138/p/4064752.html
# pymssql 托管在Github上：https://github.com/pymssql
# python连接sql server数据库实现增删改查 https://www.cnblogs.com/malcolmfeng/p/6909293.html
# /usr/local/pip3.7 install pymssql

# 问题：查询后中文正确显示，但在数据库中却显示乱码
# 解决方法：添加 charset='utf8' , 确保 charset 与数据库编码一致，如数据库是gb2312 , 则charset='gb2312'。
# conn = pymssql.Connect(host='localhost', user='root', passwd='root', db='python',charset='utf8')

# https://www.cnblogs.com/kerrycode/p/11391832.html  pymssql默认关闭自动模式开启事务行为浅析
# https://docs.microsoft.com/zh-cn/previous-versions/sql/sql-server-2008-r2/ms179296(v=sql.105)?redirectedfrom=MSDN   微软官网transact-SQL使用TRy...catch

# 关于Python获取SQLSERVER数据库中文显示乱码问题
# 原因是由于数据库中的字段的类型问题导致,varchar乱码 而 ncarchar正常
# 解决方案：在select语句中直接通过convert(nvarchar(20), remark) 转换即可

# sqlserver 报错：Cannot insert explicit value for identity column in table 't' when identity_insert is set to OFF
# 分析：当 identity insert 设置为 off 时，无法为表中的标识列插入显式值，就是 自增设置了off后，不能手动在唯一索引上添加值。
# 解决：
# set identity_insert[tableName] on
# inset ...
# set identity_insert[tableName] off

# ***************************************************************


"""
1.1 执行sql execute(self, varTable, sql)
1.2 查询sql execQuery(self, sql)
1.3 查询带参数sql execQueryParam(self, sql, param)
1.4 执行存储过程 execProcedure(self, varProcedureName)
1.5.1 执行sql文件 execSqlFile(self, varPathSqlFile)
1.5.2 执行sql文件2 execSqlFile2(self, varPathSqlFile)
1.6 close

2.1.1 获取所有表  getTables(self)
2.1.2 获取所有表和表注释 getTableAndComment(self)
2.1.3 获取表的结构信息 getTableInfor(self, varTable[all])
2.2.1 获取字段  getFields(self, varTable)
2.2.2 获取字段和字段注释 getFieldInfor(self, varTable)
2.3 获取记录数 getRecordQty(self, varTable)
2.4.1 获取所有字段和类型 getFieldAndType(self, varTable)
2.4.2 获取N个字段和类型 getOneFieldAndType(self, varTable, varField)
2.4.3 获取所有必填项字段和类型 getNotNullFieldAndType（self, varTable）
2.5 获取自增主键 getIdentityPrimaryKey(self, varTable)
2.6 获取主键  getPrimaryKey（self, varTable）
2.7 获取主键最大值 getPrimaryKeyMaxValue（self, varTable）

3.1 创建表 crtTable(self, varTable, sql)
3.2.1 生成类型值 _genTypeValue(self, varTable)
3.2.2 生成必填项类型值 _genNotNullTypeValue(self, varTable)
3.2.3 自动生成第一条数据 genFirstRecord(self, varTable)
3.2.3(2)所有表自动生成第一条数据 genFirstRecordByAll()
3.2.4 自动生成数据 genRecord(self, varTable)
3.2.5 自动生成必填项数据 genRecordByNotNull(self, varTable)
3.2.6 执行insert _execInsert(self, varTable, d_init,{})

4.1 判断表是否存在 isTable(self, varTable)
4.1 判断字段是否存在 isField(self, varTable, varField)
4.2 判断是否有自增主键 isIdentity(self, varTable)

5 excel导入数据库

应用
1 查看数据库表结构（字段、类型、大小、可空、注释），注意，表名区分大小写  dbDesc()
2 查找记录  dbRecord('*', 'money', '%34.5%')

"""

import sys
from collections.abc import Iterable, Iterator
# from collections.abc import pymssql
import pymssql
from time import sleep
# print(pymssql.__version__)
# from adodbapi import connect
from sqlalchemy import create_engine
from PO.ColorPO import *
Color_PO = ColorPO()
from PO.TimePO import *
Time_PO = TimePO()

class SqlServerPO:

    def __init__(self, varHost, varUser, varPassword, varDB, varCharset="utf-8"):
        self.host = varHost
        self.user = varUser
        self.password = varPassword
        self.db = varDB
        # self.port = int(varPort)
        self.varCharset = varCharset
        self.conn = pymssql.connect(
            server=varHost,
            user=varUser,
            password=varPassword,
            database=varDB,
            charset=varCharset,
            as_dict=True,
            tds_version="7.3",
            autocommit=True,
        )
        # self.conn = pymssql.connect(server=varHost, user=varUser, password=varPassword, port=varPort, charset=varCharset, autocommit=True)
        # self.conn = pymssql.connect(server=self.varHost, user=self.varUser, password=self.varPassword, database=self.varDB, charset='utf-8', autocommit=True)
        # self.conn = pymssql.connect(server=self.varHost, user=self.varUser, password=self.varPassword, database=self.varDB, charset='GBK', autocommit=True)
        # self.conn = pymssql.connect(server=self.varHost, user=self.varUser, password=self.varPassword, database=self.varDB, charset='CP936', autocommit=True, login_timeout=10)
        # self.conn = connect('Provider=SQLOLEDB.1;Data Source=%s;Initial Catalog=%s;UserID = %s;Password = %s;'%(self.varHost, self.varDB, self.varUser, self.varPassword))

        self.cur = self.conn.cursor()
        if not self.cur:
            raise (NameError, "error，创建游标失败！")


    def getEngine_pyodbc(self):
        # pyodbc 引擎
        return create_engine("mssql+pyodbc://" + self.user + ":" + self.password + "@mydsn")

    def getEngine_pymssql(self):
        # pymssql 引擎
        # return create_engine("mssql+pymssql://" + self.user + ":" + self.password + "@" + self.host + ":" + str(self.port) + "/" + self.db)
        return create_engine("mssql+pymssql://" + self.user + ":" + self.password + "@" + self.host + "/" + self.db)


    def xlsx2db(self, varPathFile, varSheetName, varDbTableName):

        '''
        5，xlsx导入数据库
        :param varExcelFile:
        :param varTable:
        :return:
        xlsx2db('./data/2.xlsx',"sheet3", "jh123")
        excel表格第一行数据对应db表中字段，建议用英文
        '''

        try:
            df = pd.read_excel(varPathFile, sheet_name=varSheetName)
            engine = self.getEngine_pymssql()
            df.to_sql(varDbTableName, con=engine, if_exists="replace", index=False)
        except Exception as e:
            print(e)


    # 1.1 执行sql
    def execute(self, sql):

        '''
        执行sql （insert，update）
        :param sql:
        :return:
        '''

        try:
            # 判断表是否存在
            # if self.isTable(varTable) == True:
            self.conn.commit()
            self.cur.execute(sql)
            self.conn.commit()
            return "ok"
        except Exception as e:
            # print(e.args)  # ('table hh already exists',)
            # print(str(e))  # table hh already exists
            # print(NameError(e))  # table hh already exists
            # print(repr(e))  # OperationalError('table hh already exists')
            return str(e)

    # 1.2 查询sql
    def execQuery(self, sql):

        '''
        查询sql
        :param sql:
        :return:
        '''

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

    # 1.3 查询带参数sql
    def execQueryParam(self, sql, param):

        '''
        查询带参数sql， 返回一个包含tuple的list，list是元素的记录行，tuple记录每行的字段数值
        :param sql:
        :param param:
        :return:
        '''

        # cur = self.__GetConnect()
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





    # 2.1.1 获取所有表
    def getTables(self):

        '''
        获取所有表
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

    # 2.1.2 获取所有表和表注释
    def getTableAndComment(self):

        '''
        获取所有表和表注释
        :return:
        '''

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
            print(e, ",[error], SqlserverPO.getTableAndComment()异常!")
            self.conn.close()

    # 2.1.3 获取表的结构信息
    def getTableInfor(self, varTable="allTables"):

        '''
        获取表的结构信息 (查询表的列名称、说明、备注、类型等)
        :param varTable: 如果有表名就获取一个表的信息，否则所有表的信息
        :return:
        其他用法：将如下查询内容，在navicate中执行，并导出excel文档。
        '''

        if varTable == "allTables":

            r = self.execQuery('''
            SELECT 表名 = case when a.colorder = 1 then d.name else '' end,
              表说明 = case when a.colorder = 1 then isnull(f.value, '') else '' end,
              字段序号 = a.colorder,
              字段名 = a.name,
              标识 = case when COLUMNPROPERTY(a.id, a.name, 'IsIdentity')= 1 then '√' else '' end,
              主键 = case when exists(SELECT 1 FROM sysobjects where xtype = 'PK' and parent_obj = a.id and name in (SELECT name FROM sysindexes WHERE indid in(SELECT indid FROM sysindexkeys WHERE id = a.id AND colid = a.colid))) then '√' else '' end,
              类型 = b.name,
              占用字节数 = a.length,
              长度 = COLUMNPROPERTY(a.id, a.name, 'PRECISION'),
              小数位数 = isnull(COLUMNPROPERTY(a.id, a.name, 'Scale'),0),
              允许空 = case when a.isnullable = 1 then '√' else '' end,
              默认值 = isnull(e.text, ''),
              字段说明 = isnull(g.[value], '')
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
            r = self.execQuery('''
            SELECT 表名 = case when a.colorder = 1 then d.name else '' end,
              表说明 = case when a.colorder = 1 then isnull(f.value, '') else '' end,
              字段序号 = a.colorder,
              字段名 = a.name,
              标识 = case when COLUMNPROPERTY(a.id, a.name, 'IsIdentity')= 1 then '√' else '' end,
              主键 = case when exists(SELECT 1 FROM sysobjects where xtype = 'PK' and parent_obj = a.id and name in (SELECT name FROM sysindexes WHERE indid in(SELECT indid FROM sysindexkeys WHERE id = a.id AND colid = a.colid))) then '√' else '' end,
              类型 = b.name,
              占用字节数 = a.length,
              长度 = COLUMNPROPERTY(a.id, a.name, 'PRECISION'),
              小数位数 = isnull(COLUMNPROPERTY(a.id, a.name, 'Scale'),0),
              允许空 = case when a.isnullable = 1 then '√' else '' end,
              默认值 = isnull(e.text, ''),
              字段说明 = isnull(g.[value], '')
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

        return r

    # 2.2.1 获取字段
    def getFields(self, varTable):

        '''
        获取字段
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

    # 2.2.2 获取字段和字段注释
    def getFieldAndComment(self, varTable):

        '''
        获取字段和字段注释
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


    # 2.3 获取记录数
    def getRecordQty(self, varTable):

        '''
        获取记录数（特别适合大数据）
        :param varTable:
        :return:
        '''

        qty = self.execQuery(
            "SELECT rows FROM sysindexes WHERE id = OBJECT_ID('" + varTable + "') AND indid < 2")
        return qty[0]['rows']

    # 2.4.1 获取所有字段和类型
    def getFieldAndType(self, varTable):

        '''
        获取字段和类型
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

    # 2.4.2 获取N个字段和类型
    def getMoreFieldAndType(self, varTable, l_field):

        '''
        获取单个字段和类型
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

    # 2.4.3 获取所有必填项字段和类型
    def getNotNullFieldAndType(self, varTable):

        '''
        获取必填项字段和类型
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

    # 2.5 获取自增主键
    def getIdentityPrimaryKey(self, varTable):

        '''
        获取自增主键
        :param varTable:
        :return:
        '''

        l_field = self.execQuery("select * from sys.identity_columns where [object_id]= OBJECT_ID('" + varTable + "')")
        # print(l_field)
        if l_field != []:
            return (l_field[0]['name'])  # id
        else:
            return None

    # 2.6 获取主键
    def getPrimaryKey(self, varTable):

        '''
        获取主键
        :param varTable:
        :return:
        '''

        l_primaryKey = self.execQuery("SELECT COLUMN_NAME FROM information_schema.key_column_usage where table_name='" + varTable + "'")
        # print(l_primaryKey)  # [{'COLUMN_NAME': 'ADDRESS'}, {'COLUMN_NAME': 'ID'}]
        if l_primaryKey == [] :
            return None
        else:
            return l_primaryKey

    # 2.7 获取主键最大值
    def getPrimaryKeyMaxValue(self, varTable):

        '''
        获取表主键最大值
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



    # 3.1 创建表
    def crtTable(self, varTable, sql):

        '''
        创建表
        :param sql: 
        :return: 
        '''

        # 判断表是否存在
        if self.isTable(varTable) == False:
            try:
                c_cur = self.conn.cursor()
                c_cur.execute(sql)
                print("[ok], 表<" + varTable + "> 创建成功")
            except Exception as e:
                print("表创建失败")
                # print(f"表创建失败，失败信息为:{e}")
        else:
            print("[warning], 创建<" + str(varTable) + ">表失败，表已存在！")

    # 3.2.1 生成类型值
    def _genTypeValue(self, varTable):

        '''
        初始化对应类型的值
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

    # 3.2.2 生成必填项类型值
    def _genNotNullTypeValue(self, varTable):

        '''
        生成必填项类型值
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


    # 3.2.3 单表自动生成第一条数据
    def genFirstRecord(self, varTable):

        '''
        自动生成第一条数据
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

    # 3.2.3(2)所有表自动生成第一条数据
    def genFirstRecordByAll(self):

        '''
        所有表自动生成第一条数据
        :return:
        '''
        r = self.getTables()
        # print(r)
        for i in range(len(r)):
            self.genFirstRecord(r[i])


    # 3.2.4 自动生成数据
    def genRecord(self, varTable, d_field={}):

        '''
        自动生成数据
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

    # 3.2.5 自动生成必填项数据
    def genRecordByNotNull(self, varTable):

        '''
        自动生成必填项数据（非必填项忽略）
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

    # 3.2.6 执行insert
    def _execInsert(self, varTable, d_init, d_field):

        '''
        执行insert
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



    # 4.1 判断表是否存在
    def isTable(self, varTable):

        '''
        判断表是否存在
        :param varTable:
        :return: 返回True或False
        '''

        r = self.execQuery("SELECT COUNT(*) c FROM SYSOBJECTS WHERE XTYPE = 'U' AND NAME='%s'" % (varTable))
        # print(r)  # [{'c': 1}]
        if r[0]['c'] == 1:
            return True
        else:
            return False

    # 4.2 判断字段是否存在
    def isField(self, varTable, varField):

        '''
        判断字段是否存在
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

    # 4.3 判断是否有自增主键
    def isIdentity(self, varTable):

        '''
        判断是否有自增主键, 如果有则返回1，无则返回0
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
                "\n[Result] => " + self.db + "数据库合计" + str(result) + "张表。",
                "",
            )
        elif len(args) == 1:
            # 2，单表结构 和 3，带通配符表结构 （ok）
            self._dbDesc_search(args[0])
        elif len(args) == 2:
            # 4，单表结构的可选字段 、 5，带通配符表结构的可选字段、6，所有表结构的可选字段
            self._dbDesc_search(args[0], args[1])

    # 2 查找记录
    def dbRecord(self, varTable, varType, varValue):

        """查找记录
        # 参数1：varTable = 表名（*表示所有的表）
        # 参数2：varType = 数据类型(char,int,double,timestamp)
        # 参数3：varValue = 值 (支持%模糊查询，如 %yy%)
        """
        # Sqlserver_PO.dbRecord('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
        # Sqlserver_PO.dbRecord('*', 'varchar', '%海鹰居委会%')
        # Sqlserver_PO.dbRecord('*', 'money', '%34.5%')
        # Sqlserver_PO.dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
        # Sqlserver_PO.dbRecord('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。
        # self.cur = self.__GetConnect()
        # self.cur = self.cur

        l_tbl_Name = []
        l_tbl_Type = []
        x = y = 0
        if (
                varType
                in "double,timestamp,float,money,int,nchar,nvarchar,datetime,varchar"
        ):
            if "*" in varTable:
                # 遍历所有表
                tbl = self.execQuery("SELECT NAME FROM SYSOBJECTS WHERE TYPE='U'")
                # print(tbl)
                # print(len(tbl))

                for b in range(len(tbl)):
                    # 遍历所有的表 的 列名称、列类别、类注释
                    varTable = tbl[b]['NAME']
                    # print(varTable)
                    l_tbl_NameType = self.execQuery(
                        "select syscolumns.name as Name,systypes.name as Type from syscolumns,systypes where syscolumns.xusertype=systypes.xusertype and syscolumns.id=object_id('%s')"
                        % (varTable)
                    )
                    # print(l_tbl_NameType)
                    for i in l_tbl_NameType:
                        if len(i['Name']) > x:
                            x = len(i['Name'])
                        if len(i['Type']) > y:
                            y = len(i['Type'])
                    for j in l_tbl_NameType:
                        if varType in j['Type']:
                            l_tbl_Name.append(j['Name'])
                            l_tbl_Type.append(j['Type'])
                    # print(varTable + " - " + str(list0))   # 遍历输出所有表与字段名
                    for i in range(0, len(l_tbl_Name)):
                        t4 = self.execQuery(
                            "select * from %s where convert(varchar, %s, 120) like '%s'"
                            % (varTable, l_tbl_Name[i], varValue)
                        )
                        if len(t4) != 0:
                            print("- - " * 20)

                            # print(
                            #     "搜索: "
                            #     + varValue
                            #     + " , "
                            #     + str(len(t4))
                            #     + " 条记录 来自 "
                            #     + self.db
                            #     + "."
                            #     + varTable
                            #     + "("
                            #     ")." + list0[i] + "\n"
                            # )
                            Color_PO.consoleColor(
                                "31",
                                "36",
                                "[Search] => "
                                + varValue
                                + " , [Result] => "
                                + varTable
                                + "." + l_tbl_Name[i] + " 疑似 " + str(len(t4)) + " 条。 " + "\n",
                                "",
                            )
                            for j in range(len(t4)):
                                print(t4[j])
                                # print(str(t4[j]).decode("utf8"))
                                # print(t4[j].encode('latin-1').decode('utf8'))

                    list0 = []
                    list1 = []

            elif "*" not in varTable:
                # 搜索指定表（单表）符合条件的记录.  ，获取列名称、列类别、类注释

                # 获取表的Name和Type
                l_tbl_NameType = self.execQuery(
                    "select syscolumns.name as Name,systypes.name as Type from syscolumns,systypes where syscolumns.xusertype=systypes.xusertype and syscolumns.id=object_id('%s')"
                    % (varTable)
                )
                # print(l_tbl_NameType)  # [{'Name': 'ID', 'Type': 'int'}, {'Name': 'ARCHIVENUM', 'Type': 'varchar'}]

                # 输出Name
                l_tbl_name = []
                for i in range(len(l_tbl_NameType)):
                    l_tbl_name.append(l_tbl_NameType[i]['Name'])

                # for i in l_tbl_NameType:
                #     if len(i['Name']) > x:
                #         x = len(i['Name'])
                #     if len(i['Type']) > y:
                #         y = len(i['Type'])

                # 筛选符合条件（包含指定Type）的Name
                l_tbl_Name_filter = []
                for j in l_tbl_NameType:
                    if varType in j['Type']:
                        l_tbl_Name_filter.append(j['Name'])
                        # l_tbl_Type.append(j['Type'])
                # print(l_tbl_Name)  # ['ARCHIVENUM', 'EHRNUM', 'NAME', 'PRESENTADDRESS']

                for i in range(len(l_tbl_Name_filter)):
                    result = self.execQuery(
                        "select * from %s where convert(varchar, %s, 120) like '%s'"
                        % (varTable, l_tbl_Name_filter[i], varValue)
                    )

                    if len(result) != 0:
                        print("- - " * 20)
                        # print(
                        #     "[Search] => "
                        #     + varValue
                        #     + ",[Result] => "
                        #     + str(len(t4))
                        #     + " 条记录, 来自 "
                        #     + self.db
                        #     + "."
                        #     + varTable
                        #     + "("
                        #     ")." + list0[i] + "\n"
                        # )
                        Color_PO.consoleColor(
                            "31",
                            "36",
                            "[search = " + varValue + "] , [result = " + varTable
                            + "." + l_tbl_Name_filter[i] + " => " + str(len(result)) + "条]" + "\n",
                            "",
                        )

                        # 输出Name
                        print(l_tbl_name)  # ['ID', 'ARCHIVENUM', 'EHRNUM', 'NAME', 'PRESENTADDRESS']

                        # 获取所有Name的大小
                        l_nameSize = []
                        for i in l_tbl_name:
                            l_nameSize.append(len(i))
                        # print(l_nameSize)  # [2, 10, 6, 4, 14, 16, 5]

                        for j in range(len(result)):
                            l_value = [value for value in result[j].values()]
                            print(l_value)  # [1, '410522200004110812', 'K22402612', '刘斌龙', '河北省 ]

                        #     # 获取所有值的大小
                        #     l_valueSize = []
                        #     for i in l_value:
                        #         l_valueSize.append(len(str(i)))
                        #     # print(l_valueSize)  # [1, 18, 9, 3, 23, 4, 11, 4, 4, 4, 4, 4, 4]
                        #
                        #     # 格式化Name
                        #     for i in range(len(l_valueSize)):
                        #         if l_valueSize[i] > l_nameSize[i]:
                        #             x = l_valueSize[i] - l_nameSize[i]
                        #             l_tbl_name[i] = l_tbl_name[i] + " " * x
                        #         else:
                        #             l_tbl_name[i] = l_tbl_name[i] + " "
                        #             l_value[i] = str(l_value[i]) + " " * (l_nameSize[i] - l_valueSize[i]) + " "
                        #
                        # print(l_tbl_name)  # ['ID ', 'ARCHIVENUM        ', 'EHRNUM   ', 'NAME ', 'PRESENTADDRESS         ']
                        # print(l_value)

                        # # 将所有Name合并成字符串
                        # str_name = str_value = ""
                        # for i in l_tbl_name:
                        #     str_name = str_name + i
                        # print(str_name)  # ID ARCHIVENUM        EHRNUM   NAME PRESENTADDRESS
                        #
                        # for i in l_value:
                        #     str_value = str_value + str(i)
                        # print(str_value)

                        # # 将所有value合并成字符串
                        # for j in range(len(result)):
                        #     l_value = [value for value in result[j].values()]

                        # for i in my_list:
                        #     list4.append(len(str(i)))
                        # print(list4)

                        # print(t4[j].encode('latin-1').decode('gbk'))

                l_tbl_Name = []
                l_tbl_Type = []
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


    print("5 excel导入数据库".center(100, "-"))
    Sqlserver_PO.xlsx2db('./data/2.xlsx', "Sheet3", "jh123")


    # print("1.1 查询sql".center(100, "-"))
    # a = Sqlserver_PO.execQuery("select * from aaa")
    # print(a)

    # print("1.2 执行sql".center(100, "-"))
    # Sqlserver_PO.execute("aaa", "UPDATE aaa set AGE=20 where ID=4")  # 更新数据
    # Sqlserver_PO.execute("aaa", "drop table aaa")  # 删除表
    # Sqlserver_PO.execute("aaa", "truncate table aaa")  # 删除数据



    # print("2.1.1 获取所有表".center(100, "-"))
    # print(Sqlserver_PO.getTables())  # ['condition_item', 'patient_demographics', 'patient_diagnosis']

    # print("2.1.2 获取所有表和表注释".center(100, "-"))
    # print(Sqlserver_PO.getTableAndComment())  # {'aaa': None, 'bbb': None, 'EMR_ADMISSION_ASSESSMENT': '入院评估记录',...}

    # print("2.1.3 获取所有表结构信息".center(100, "-"))
    # print(Sqlserver_PO.getTableInfor('aaa'))
    # print(Sqlserver_PO.getTableInfor())



    # print("2.2.1 获取字段".center(100, "-"))
    # print(Sqlserver_PO.getFields('aaa'))  # ['ID', 'ADDRESS', 'SALARY', 'NAME', 'AGE', 'time']

    # print("2.2.2 获取字段和字段注释".center(100, "-"))
    # print(Sqlserver_PO.getFieldAndComment('TB_HIS_MZ_Reg'))

    # getFieldAndComment

    # print("2.3 获取记录数 ".center(100, "-"))
    # print(Sqlserver_PO.getQty('aaa'))  # 0

    # print("2.4.1 获取所有字段和类型 ".center(100, "-"))
    # print(Sqlserver_PO.getFieldAndType("aaa"))  # {'ID': 'int', 'NAME': 'text', 'AGE': 'int', 'ADDRESS': 'char', 'SALARY': 'float'}
    #
    # print("2.4.2 获取N个字段和类型 ".center(100, "-"))
    # print(Sqlserver_PO.getMoreFieldAndType("aaa", ["ID"]))  # {'ID': 'int'}
    # print(Sqlserver_PO.getMoreFieldAndType("aaa", ["ID", 'AGE']))  # {'ID': 'int', 'AGE': 'int'}
    #
    # print("2.4.3 获取必填项字段和类型".center(100, "-"))
    # print(Sqlserver_PO.getNotNullFieldAndType('aaa'))  # {'ID': 'int', 'NAME': 'text', 'AGE': 'int', 'ADDRESS': 'char'}
    #
    # print("2.5 获取自增主键".center(100, "-"))
    # print(Sqlserver_PO.getIdentityPrimaryKey('aaa'))  # None // 没有自增主键
    # print(Sqlserver_PO.getIdentityPrimaryKey('bbb'))  # id
    #
    # print("2.6 获取表主键".center(100, "-"))
    # print(Sqlserver_PO.getPrimaryKey('aaa'))  # [{'COLUMN_NAME': 'ADDRESS'}, {'COLUMN_NAME': 'ID'}]
    # print(Sqlserver_PO.getPrimaryKey('bbb'))  # [{'COLUMN_NAME': 'id'}]

    # print("2.7 获取表主键最大值 ".center(100, "-"))
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

    # print("3.2.1 生成类型值".center(100, "-"))
    # print(Sqlserver_PO._genTypeValue("aaa"))  # {'ID': 1, 'NAME': 'a', 'AGE': 1, 'ADDRESS': 'a', 'SALARY': 1.0, 'time': '08:12:23'}

    # print("3.2.2 生成必填项类型值".center(100, "-"))
    # print(Sqlserver_PO._genNotNullTypeValue("aaa"))

    # print("3.2.3 自动生成第一条数据".center(100, "-"))
    # Sqlserver_PO.genFirstRecord('bbb')
    # print("3.2.3(2) 所有表自动生成第一条数据".center(100, "-"))
    # Sqlserver_PO.genFirstRecordByAll()

    # print("3.2.4 自动生成数据".center(100, "-"))
    # Sqlserver_PO.genRecord('aaa')

    # print("3.2.5 自动生成必填项数据".center(100, "-"))
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
    # Sqlserver_PO.dbRecord('*', 'varchar', '%高血压%')  # 搜索所有表符合条件的记录.
    # Sqlserver_PO.dbRecord('*', 'money', '%34.5%')l
    # Sqlserver_PO.dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
    # Sqlserver_PO.dbRecord('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。


