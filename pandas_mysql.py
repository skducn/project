# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-4-8
# Description: pandas 操作mysql数据库
# pandas dataframe.to_sql() 用法  , https://www.jianshu.com/p/d615699ff254
# *****************************************************************

import pandas as pd
from sqlalchemy import create_engine

# 使用pymysql模块初始化数据库连接
engine = create_engine('mysql+pymysql://ceshi:123456@192.168.0.233:3336/TD_OA')

# 读表
sql_cmd = "select * from user_jh where user_name='金浩'"
df = pd.read_sql(sql=sql_cmd, con=engine)
print(df.head())
print(df["USER_NAME"][0])
# 写表方法1，原表是数据库表，将DATAFRAME to_sql成新表。（会有以下几个问题）
# 问题1：目标表的数据类型变为数字型和字符型。
# 问题2：没有了primarykey
# 因为 pandas 定位是数据分析工具，数据源可以来自 CSV 这种文本型文件，本身是没有严格数据类型的。而且，pandas 数据 to_excel() 或者to_sql() 只是方便数据存放到不同的目的地，本身也不是一个数据库升迁工具。
# df.to_sql("user_jh",engine)

# 写表方法2，数据源来自csv
# import sqlalchemy
#
# print(pd.io.sql.get_schema(df, 'emp_backup', keys='EMP_ID',
#    dtype={'EMP_ID': sqlalchemy.types.BigInteger(),
#        'GENDER': sqlalchemy.types.String(length=20),
#        'AGE': sqlalchemy.types.BigInteger(),
#        'EMAIL':  sqlalchemy.types.String(length=50),
#        'PHONE_NR':  sqlalchemy.types.String(length=50),
#        'EDUCATION':  sqlalchemy.types.String(length=50),
#        'MARITAL_STAT':  sqlalchemy.types.String(length=50),
#        'NR_OF_CHILDREN': sqlalchemy.types.BigInteger()
#        }, con=engine))

# 其中 get_schema方法就是如下语句
# CREATE TABLE emp_backup (
#         `EMP_ID` BIGINT NOT NULL AUTO_INCREMENT,
#         `GENDER` VARCHAR(20),
#         `AGE` BIGINT,
#         `EMAIL` VARCHAR(50),
#         `PHONE_NR` VARCHAR(50),
#         `EDUCATION` VARCHAR(50),
#         `MARITAL_STAT` VARCHAR(50),
#         `NR_OF_CHILDREN` BIGINT,
#         CONSTRAINT emp_pk PRIMARY KEY (`EMP_ID`)
# )
#
# # 写表方法3，原表是数据库表，将DATAFRAME to_sql成新表。（多了一个index字段，或通过index=False不创建索引）
# Copy table structure
with engine.connect() as con:
    con.execute('DROP TABLE if exists user_jh')
    con.execute('CREATE TABLE user_jh LIKE user;')  # 复制新表 user_jh

# # print(df.shape)
# # print(df.info())
# # print(df.columns)
# # print(df.columns.values)
# # print(df.columns.values[3])
# # df.columns = [x.strip() for x in df.columns.values]   # 将列表名中前后空格去掉了。
#
# print(df.duplicated().sum())
#
# print(df.describe().T)
#
# print(df[df.ONLINE < 5000])
# print(df[df.ONLINE < 5000].count()["UID"])
#
# print(df.isnull().sum())
#
# print(df[df.IMEI.isnull()].head())
#
# print(df.loc[df.IMEI.isnull(), "USER_NAME"])
# # df.USER_NAME = df.USER_NAME + "NULL"
# # str(df.USER_NAME).replace("NULL", "")
#
# x = df.loc[df.IMEI.isnull(), "USER_NAME"]
# df.loc[df.IMEI.isnull(), "USER_NAME"] = [i + "NULL" for i in x]
#
#
# # # # 将新建的DataFrame储存为MySQL中的数据表，储存index列
# df.to_sql('user_jh', engine, index=False, if_exists='append')
#
#
#
#
#
# # sql = ''' select * from user_test; '''
# # # read_sql_query的两个参数: sql语句， 数据库连接
# # df = pd.read_sql_query(sql, engine)
# #
# # # 输出表的查询结果
# # print(df['USER_NAME'])
# #
# # # # 新建pandas中的DataFrame, 只有id,num两列
# # df = pd.DataFrame({'id': [1, 2, 3, 4], 'name': ['zhangsan', 'lisi', 'wangwu', 'zhuliu']})
# # print(df)
# #
#
# # df.to_sql('user_copy', engine, index=True) # mydf表名，engine：存到相应的数据库下面
# # # print('Read from and write to Mysql table successfully!')