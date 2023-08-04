# -- coding: utf-8 --
# ***************************************************************
# Author     : John
# Data       : 2019-04-16
# Description: SqlServerPO对象层
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

# ***************************************************************


"""

1 查看数据库表结构（字段、类型、大小、可空、注释），注意，表名区分大小写  dbDesc()
2 查找记录  dbRecord('*', 'money', '%34.5%')
3 判断字段是否存在 isField(self, varTable, varField)
4 获取字段的类型  getFieldType(self, varTable, varField)
5 获取单个表的所有字段  getTableField(self, varTable)
6 获取所有表名  getAllTable(self)

"""
import sys
from collections.abc import Iterable, Iterator

# from collections.abc import pymssql
import pymssql

# print(pymssql.__version__)
# from adodbapi import connect
from sqlalchemy import create_engine
from PO.ColorPO import *

Color_PO = ColorPO()


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

<<<<<<< HEAD


    def execute(self, sql):

        """insert or update sql"""
        try:
            self.cur.execute(sql)
        except Exception as e:
            # print(e.args)  # ('table hh already exists',)
            # print(str(e))  # table hh already exists
            # print(NameError(e))  # table hh already exists
            print(repr(e))  # OperationalError('table hh already exists')


    def execQuery(self, sql):

        """执行sql"""

        # self.conn.commit()

=======
    def execQuery(self, sql):

        """执行sql"""

        # self.conn.commit()

>>>>>>> origin/master
        try:
            self.cur.execute(sql)
            result = self.cur.fetchall()
            self.conn.commit()
            return result
        except Exception as e:
            # print(e.args)  # ('table hh already exists',)
            # print(str(e))  # table hh already exists
            # print(NameError(e))  # table hh already exists
            print(repr(e))  # OperationalError('table hh already exists')

    def close(self):
        self.cur.close()
        self.conn.close()

    def getEngine_pyodbc(self):
        # pyodbc 引擎
        return create_engine(
            "mssql+pyodbc://" + self.user + ":" + self.password + "@mydsn"
        )

    def getEngine_pymssql(self):
        # pymssql 引擎
        return create_engine(
            "mssql+pymssql://"
            + self.user
            + ":"
            + self.password
            + "@"
            + self.host
            + ":"
            + str(self.port)
            + "/"
            + self.db
        )

    def execQueryParam(self, sql, param):

        """执行查询语句 (参数)
        返回一个包含tuple的list，list是元素的记录行，tuple记录每行的字段数值
        """

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

    def execProcedure(self, varProcedureName):

        """执行存储过程"""
        # execProcedure(存储过程名)

        # cur = self.__GetConnect()
        # sql =[]
        # sql.append("exec procontrol")
        # cur.callproc(varProcedureName)
        self.cur.execute(varProcedureName)
        self.conn.commit()
        self.cur.close()  # 关闭游标
        self.conn.close()  # 关闭连接

    def execSqlFile(self, varPathSqlFile):

        """执行sql文件语句"""

        # execQueryBySQL('D:\\51\\python\\project\\instance\\zyjk\\EHR\\controlRule\\mm.sql')
        # cur = self.__GetConnect()
        with open(varPathSqlFile) as f:
            sql = f.read()
            self.cur.execute(sql)
            self.conn.commit()
            self.conn.close()

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
                        l_isKey.append(str(i['Size']) + " " * (tblSize - len(str(i['Size']))+5))
                        l_isnull.append(str(i['NotNull']) + " " * (tblNotNull - len(str(i['NotNull']))+3))
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
                        "Name" + " " * (tblName - len("Name")+1) +
                        "Type" + " " * (tblType - len("Type")+1) +
                        "Size" + " " * (tblSize - len("Size")+6) +
                        "isNull" + " " * (tblNotNull - len("isNull")+4) +
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

    # 3 判断字段是否存在
    def isField(self, varTable, varField):

        """判断字段是否存在，返回True或False"""
        # isField("tb_dc_htn_visit", "name")

        r = self.execQuery(
            "SELECT B.name as FieldName FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'"
            % (varTable)
        )
        for i in range(len(r)):
            if r[i][0] == varField:
                return True
        return False

    # 4 获取字段的类型
    def getFieldType(self, varTable, varField):

        """获取字段的类型"""
        # Sqlserver_PO.getFieldType("tb_dc_htn_visit", "visitDate")

        r = self.execQuery(
            "SELECT B.name as FieldName, d.name as FieldType FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'"
            % (varTable)
        )
        for i in range(len(r)):
            if r[i][0] == varField:
                return r[i][1]
        return None

    # 5 获取单个表的所有字段
    def getTableField(self, varTable):

        """获取单个表的所有字段"""
        # Sqlserver_PO.getTableField('HrCover')

        try:
            r = self.execQuery(
                "SELECT B.name as FieldName FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'"
                % (varTable)
            )
            l_field = []
            for i in range(len(r)):
                l_field.append(r[i][0])
            return l_field

        except Exception as e:
            print(e, ",很抱歉，出现异常您搜索的<" + varTable + ">不存在！")

    # 6 获取所有表名
    def getAllTable(self):

        """获取所有表名"""
        try:
            r = self.execQuery(
                "SELECT DISTINCT d.name,f.value FROM syscolumns a LEFT JOIN systypes b ON a.xusertype= b.xusertype INNER JOIN sysobjects d ON a.id= d.id AND d.xtype= 'U' AND d.name<> 'dtproperties' LEFT JOIN syscomments e ON a.cdefault= e.id LEFT JOIN sys.extended_properties g ON a.id= G.major_id AND a.colid= g.minor_id LEFT JOIN sys.extended_properties f ON d.id= f.major_id AND f.minor_id= 0"
            )
            list1 = []
            for i in range(len(r)):
                list1.append(r[i][0])
            return list1
        except Exception as e:
            print(e, ",很抱歉，出现异常！")
            self.conn.close()


if __name__ == "__main__":

    # 234 ehr ————————————————————————————————————————————————————————————————————————————————————————————————————————————
    Sqlserver_PO = SqlServerPO(
        "192.168.0.234", "sa", "Zy_123456789", "EHR_CDRINFO", "GBK"
    )  # 测试环境
    # Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "EHR_CDRINFO", "utf8")  # 测试环境
    # Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "EHR_CDRINFO")  # 测试环境
    # Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy@123456", "EHR_CDRINFO", 1433, "GBK")  # 测试环境
    # Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy@123456", "EHR_CDRINFO", 1433, "")  # 测试环境

    # r = Sqlserver_PO.execQuery('select * from tb_org where id=%s ' % ('1'))
    # print(r)

    # tmpList = Sqlserver_PO.execQuery("SELECT convert(nvarchar(255), Categories)  FROM HrRule where RuleId='00081d1c0cce49fd88ac68b7627d6e1c' ")  # 数据库数据自造
    # l_result = Sqlserver_PO.execQuery('select top 1 (select sum(live_people_num) from (select live_people_num,org_name from report_qyyh group by org_code,org_name,live_people_num) a)  livePeopleNum from report_qyyh')
    # print(l_result)

    # l_result = Sqlserver_PO.execQuery('select convert(nvarchar(20), Name) from HrCover where id=%s ' % (1))  # 中文乱码使用 convert(nvarchar(20), 字段)
    # l_result = Sqlserver_PO.execQuery('select Name from HrCover where id=%s ' % (1))  # 中文乱码使用 convert(nvarchar(20), 字段)
    # print(l_result)

    print("1 查看数据库表结构（字段、类型、大小、可空、注释）".center(100, "-"))
    # Sqlserver_PO.dbDesc()  # 1，所有表结构
    Sqlserver_PO.dbDesc("tb_org")  # 2，单表结构
    # Sqlserver_PO.dbDesc('s%')  # 3，带通配符表结构
    # Sqlserver_PO.dbDesc('tb_org', ['id', 'org_name'])  # 4,单表结构的可选字段
    # Sqlserver_PO.dbDesc('s%', ['id', 'kaId'])  # 5，带通配符表结构的可选字段(只输出找到字段的表)
    # Sqlserver_PO.dbDesc(0, ['id', 'kaId', 'org_name'])  # 6，所有表结构的可选字段(只输出找到字段的表)

    # print("2 查找记录".center(100, "-"))
    # Sqlserver_PO.dbRecord('CommonDictionary', 'varchar', '%录音%')  # 搜索指定表符合条件的记录.
    # Sqlserver_PO.dbRecord('*', 'varchar', '%高血压%')  # 搜索所有表符合条件的记录.
    # Sqlserver_PO.dbRecord('*', 'money', '%34.5%')l
    # Sqlserver_PO.dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
    # Sqlserver_PO.dbRecord('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。

    # print("3 判断字段是否存在".center(100, "-"))
    # print(Sqlserver_PO.isField("condition_item", "name"))  # False
    # print(Sqlserver_PO.isField("condition_item", "id"))  # True

    # print("4 获取字段的类型".center(100, "-"))
    # print(Sqlserver_PO.getFieldType(Sqlserver_PO.getAllTable()[0], "id"))  # int
    # print(Sqlserver_PO.getFieldType("condition_item", "id"))

    # print("4 获取单个表的所有字段".center(100, "-"))
    # print(Sqlserver_PO.getTableField(Sqlserver_PO.getAllTable()[0]))  # ['id', 'sd_id', 'category', 'item', 'itemValue', 'sign', 'logic', 'isAccurate', 'type']
    # print(Sqlserver_PO.getTableField('condition_item'))

    # print("6 获取所有表名".center(100, "-"))
    # print(Sqlserver_PO.getAllTable())  # ['condition_item', 'patient_demographics', 'patient_diagnosis']
