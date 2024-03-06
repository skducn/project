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

# Errors 1000 - 1999 https://learn.microsoft.com/en-us/previous-versions/sql/sql-server-2008/cc645860(v=sql.100)
# 关于 1753 Column '%.*ls.%.*ls' is not the same length or scale as referencing column '%.*ls.%.*ls' in foreign key '%.*ls'. Columns participating in a foreign key relationship must be defined with the same length and scale.
# 发生在外键关联失败，请检查表结构，是否在关联的字段类型与尺寸一致。


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

# https://blog.51cto.com/u_16213439/7729728
# sys.foreign_keys视图：该视图包含了数据库中所有的外键的信息，包括外键名称、关联表、主表等。

# 获取日期时间为：年-月-日 时：分：秒， 如：2024-01-30 14:50：12
# select CONVERT(nvarchar(20), getdate(),120) as Sdatetime from a_student;
# 获取日期时间为：年-月-日 时：分， 如：2024-01-30 14:50
# select substring(convert(varchar,getdate(),120),1,16) as Sdatetime from a_student;
# 获取日期时间为：年-月-日 时， 如：2024-01-30 14
# select substring(convert(varchar,getdate(),120),1,13) as Sdatetime from a_student;
# ***************************************************************

"""

5.1.1 csv2dbByType()  csv2db自定义字段类型
5.1.2 csv2dbByAutoType()  csv2db自动生成字段类型
5.2 exls2db  excel导入数据库
5.3 dict2db
5.4 list2db
5.5 db2csv
5.6 db2xlsx
5.7 db2dict


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


from PO.TimePO import *
Time_PO = TimePO()



class SqlServer:

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
        ''' pyodbc 引擎 '''
        return create_engine("mssql+pyodbc://" + self.user + ":" + self.password + "@mydsn")

    def getEngine_pymssql(self):
        ''' pymssql 引擎 '''
        # return create_engine("mssql+pymssql://" + self.user + ":" + self.password + "@" + self.server + ":" + str(self.port) + "/" + self.database)
        return create_engine("mssql+pymssql://" + self.user + ":" + self.password + "@" + self.server + "/" + self.database)



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




if __name__ == "__main__":


    # todo 公卫
    Sqlserver_PO = SqlServer("192.168.0.234", "sa", "Zy_123456789", "PHUSERS", "GBK")

    engine = Sqlserver_PO.getEngine_pymssql()
    df = pd.read_sql(text("select * from a_test"), con=engine.connect())
    # df = pd.read_sql("select * from a_test", con=engine.connect())
    print(df)

    # 从库里获取数据

    # 从csv中获取数据