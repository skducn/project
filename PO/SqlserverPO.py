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
    def __init__(self, varHost, varUser, varPassword, varDB, varCharset=""):
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

    def execQuery(self, sql):

        """执行sql"""

        # self.conn.commit()

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

        cur = self.__GetConnect()
        self.conn.commit()  # 用于新增后立即查询
        cur.execute(sql, param)

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

    def execProcedure(self, varProcedureName):

        """执行存储过程"""
        # execProcedure(存储过程名)

        cur = self.__GetConnect()
        # sql =[]
        # sql.append("exec procontrol")
        # cur.callproc(varProcedureName)
        cur.execute(varProcedureName)
        self.conn.commit()
        cur.close()  # 关闭游标
        self.conn.close()  # 关闭连接

    def execSqlFile(self, varPathSqlFile):

        """执行sql文件语句"""

        # execQueryBySQL('D:\\51\\python\\project\\instance\\zyjk\\EHR\\controlRule\\mm.sql')
        cur = self.__GetConnect()
        with open(varPathSqlFile) as f:
            sql = f.read()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()

    def execSqlFile2(self, varPathSqlFile):

        """执行sql文件语句2"""

        cur = self.__GetConnect()
        with open(varPathSqlFile) as f:
            sql = f.read()
            cur.execute(sql)
            cur.nextset()
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
            print(l_table_comment)
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
        for t in l_table_comment:
            if t[1] != None:
                d_tableComment[t[0]] = t[1].decode("utf8")
            else:
                d_tableComment[t[0]] = str(t[1])

        for k, v in d_tableComment.items():
            varTable = k
            l_table_field_type_size_isNull_comment = self.execQuery(
                "SELECT A.name, B.name, d.name, B.max_length, B.is_nullable, C.value FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s'"
                % (varTable)
            )
            # print(l_table_field_type_size_isNull_comment)  # [('condition_item', 'id', 'int', 4, False, b'\xe8\x87\xaa\xe5\xa2\x9e\xe4\xb8\xbb\xe9\x94\xae'), ]
            # print(l_table_field_type_size_isNull_comment[0][5].decode('utf8'))
            try:
                # 字段与类型对齐
                a = b = c = d = e = f = 0
                for i in l_table_field_type_size_isNull_comment:
                    # if len(i[0]) > a: a = len(i[0])
                    if len(i[1]) > b:
                        b = len(i[1])
                    if len(i[2]) > c:
                        c = len(i[2])
                    if len(str(i[3])) > d:
                        d = len(str(i[3]))
                    if len(str(i[4])) > e:
                        e = len(str(i[4]))
                    if len(str(i[5])) > f:
                        f = len(str(i[5]))

                if var_l_field != 0:
                    # 可选字段
                    for l in range(len(var_l_field)):
                        for m in range(len(l_table_field_type_size_isNull_comment)):
                            if (
                                var_l_field[l]
                                == l_table_field_type_size_isNull_comment[m][1]
                            ):
                                l_field.append(
                                    str(l_table_field_type_size_isNull_comment[m][1])
                                    + " "
                                    * (
                                        b
                                        - len(
                                            l_table_field_type_size_isNull_comment[m][1]
                                        )
                                        + 1
                                    )
                                )
                                l_type.append(
                                    str(l_table_field_type_size_isNull_comment[m][2])
                                    + " "
                                    * (
                                        c
                                        - len(
                                            l_table_field_type_size_isNull_comment[m][2]
                                        )
                                        + 1
                                    )
                                )
                                l_isKey.append(
                                    str(l_table_field_type_size_isNull_comment[m][3])
                                    + " "
                                    * (
                                        d
                                        - len(
                                            str(
                                                l_table_field_type_size_isNull_comment[
                                                    m
                                                ][3]
                                            )
                                        )
                                        + 1
                                    )
                                )
                                l_isnull.append(
                                    str(l_table_field_type_size_isNull_comment[m][4])
                                    + " "
                                    * (
                                        e
                                        - len(
                                            str(
                                                l_table_field_type_size_isNull_comment[
                                                    m
                                                ][4]
                                            )
                                        )
                                        + 7
                                    )
                                )
                                if l_table_field_type_size_isNull_comment[m][5] == None:
                                    l_comment.append(
                                        str(
                                            l_table_field_type_size_isNull_comment[m][5]
                                        )
                                        + " "
                                        * (
                                            f
                                            - len(
                                                str(
                                                    l_table_field_type_size_isNull_comment[
                                                        m
                                                    ][
                                                        5
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
                                                5
                                            ].decode("utf8")
                                        )
                                        + " "
                                        * (
                                            f
                                            - len(
                                                str(
                                                    l_table_field_type_size_isNull_comment[
                                                        m
                                                    ][
                                                        5
                                                    ]
                                                )
                                            )
                                            + 1
                                        )
                                    )
                else:
                    # 所有字段
                    for i in l_table_field_type_size_isNull_comment:
                        l_field.append(str(i[1]) + " " * (b - len(i[1]) + 1))
                        l_type.append(str(i[2]) + " " * (c - len(i[2]) + 1))
                        l_isKey.append(str(i[3]) + " " * (d - len(str(i[3])) + 1))
                        l_isnull.append(str(i[4]) + " " * (e - len(str(i[4])) + 7))
                        if i[5] == None:
                            l_comment.append(str(i[5]) + " " * (f - len(str(i[5])) + 1))
                        else:
                            l_comment.append(
                                str(i[5].decode("utf8"))
                                + " " * (f - len(str(i[5])) + 1)
                            )

                # 只输出找到字段的表
                if len(l_field) != 0:
                    print("- - " * 50)
                    Color_PO.consoleColor(
                        "31",
                        "36",
                        "["
                        + str(k)
                        + "("
                        + str(d_tableComment[k])
                        + ") - "
                        + str(len(l_table_field_type_size_isNull_comment))
                        + "个字段]",
                        "",
                    )
                    print(
                        "字段名" + " " * (b - 4),
                        "数据类型" + " " * (c - 6),
                        "大小" + " " * (d - 2),
                        "允许空值" + " " * (e),
                        "字段说明",
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
                "\n[已完成], 当前数据库 " + self.varDB + " 共有 " + str(result) + " 张表。 ",
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
        self.cur = self.__GetConnect()

        list0 = []
        list1 = []
        x = y = 0
        if (
            varType
            in "double,timestamp,float,money,int,nchar,nvarchar,datetime,varchar"
        ):
            if "*" in varTable:
                # 遍历所有表
                self.cur.execute("SELECT NAME FROM SYSOBJECTS WHERE TYPE='U'")
                tbl = self.cur.fetchall()
                for b in range(len(tbl)):
                    # 遍历所有的表 的 列名称、列类别、类注释
                    varTable = tbl[b][0]
                    self.cur.execute(
                        "select syscolumns.name,systypes.name from syscolumns,systypes where syscolumns.xusertype=systypes.xusertype and syscolumns.id=object_id('%s')"
                        % (varTable)
                    )
                    tblFields = self.cur.fetchall()
                    for i in tblFields:
                        if len(i[0]) > x:
                            x = len(i[0])
                        if len(i[1]) > y:
                            y = len(i[1])
                    for j in tblFields:
                        if varType in j[1]:
                            list0.append(j[0])
                            list1.append(j[1])
                    # print(varTable + " - " + str(list0))   # 遍历输出所有表与字段名
                    for i in range(0, len(list0)):
                        self.cur.execute(
                            "select * from %s where convert(varchar, %s, 120) like '%s'"
                            % (varTable, list0[i], varValue)
                        )
                        t4 = self.cur.fetchall()
                        if len(t4) != 0:
                            print("*" * 100)
                            print(
                                "搜索: "
                                + varValue
                                + " , "
                                + str(len(t4))
                                + " 条记录 来自 "
                                + self.varDB
                                + "."
                                + varTable
                                + "("
                                ")." + list0[i] + "\n"
                            )
                            for j in range(len(t4)):
                                print(t4[j])
                                # print(str(t4[j]).decode("utf8"))
                                # print(t4[j].encode('latin-1').decode('utf8'))

                    list0 = []
                    list1 = []
            elif "*" not in varTable:
                # 获取列名称、列类别、类注释
                self.cur.execute(
                    "select syscolumns.name,systypes.name from syscolumns,systypes where syscolumns.xusertype=systypes.xusertype and syscolumns.id=object_id('%s')"
                    % (varTable)
                )
                tblFields = self.cur.fetchall()
                for i in tblFields:
                    if len(i[0]) > x:
                        x = len(i[0])
                    if len(i[1]) > y:
                        y = len(i[1])
                for j in tblFields:
                    if varType in j[1]:
                        list0.append(j[0])
                        list1.append(j[1])
                for i in range(0, len(list0)):
                    self.cur.execute(
                        "select * from %s where convert(varchar, %s, 120) like '%s'"
                        % (varTable, list0[i], varValue)
                    )
                    t4 = self.cur.fetchall()
                    if len(t4) != 0:
                        print("*" * 100)
                        print(
                            "搜索: "
                            + varValue
                            + " , "
                            + str(len(t4))
                            + " 条记录 来自 "
                            + self.varDB
                            + "."
                            + varTable
                            + "("
                            ")." + list0[i] + "\n"
                        )
                        # print("search: " + varValue + " > " + self.varDB + "." + varTable + "(" ")." + list0[i] + " > [" + str(len(t4)) + " 条记录]" + "\n")
                        for j in range(len(t4)):
                            print(t4[j])
                            # print(t4[j].encode('latin-1').decode('gbk'))

                list0 = []
                list1 = []
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
