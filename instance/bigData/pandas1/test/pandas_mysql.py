# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-4-8
# Description: pandas 操作mysql数据库表
# pandas dataframe.to_sql() 用法  , https://www.jianshu.com/p/d615699ff254
# *****************************************************************

import pandas as pd
from sqlalchemy import create_engine

'''
1，将数据库表保存到excel

2.1，数据库中复制表格(与原表类型一致)，如将sys_menu 复制成 test_menu
2.2，数据库中复制表格(与原表类型不一致)，varchar变为text，int变为bigint，取消主键

3，将 DataFrame 写入数据库表

4，用 DataFrame 形式读取数据库表
'''

# 加载mysql数据库连接
engine = create_engine('mysql+pymysql://root:123456@192.168.0.234:3306/epd')


# 1，将数据库表保存到excel
sql = "select * from sys_menu "
df = pd.read_sql(sql=sql, con=engine)
# print(df.head())
# print(df["id"][0])
df.to_excel("epd.xlsx")

# # 2.1，数据库中复制表格(与原表类型一致)，如将sys_menu 复制成 test_menu
# with engine.connect() as con:
#     con.execute('DROP TABLE if exists test_menu')
#     con.execute('CREATE TABLE test_menu LIKE sys_menu;')
# df.to_sql('test_menu', engine, index=False, if_exists='append')


# 2.2，数据库中复制表格(与原表类型不一致)，varchar变为text，int变为bigint，取消主键
# a，目标表（test_menu）的数据类型变为数字型和字符型。
# b，取消了primary 主键
# c，多了index字段
#  注意：index=False 表示不创建index字段 ， df.to_sql('test_menu', index=False, engine)
# 分析：因为 pandas 定位是数据分析工具，数据源可以来自 CSV 这种文本型文件，本身是没有严格数据类型的。而且，pandas 数据 to_excel() 或者to_sql() 只是方便数据存放到不同的目的地，本身也不是一个数据库升迁工具。
# df.to_sql('test_menu', engine)


# 3，将 DataFrame（id,name) 写入数据库
# 要求，主键id， name varchar(30)
df = pd.DataFrame({'id': [1, 2, 3, 4], 'name': ['zhangsan', 'lisi', 'wangwu', 'zhuliu']})
with engine.connect() as con:
    con.execute('DROP TABLE if exists test1')
    df.to_sql('test1', engine, index=False)  # test1表名，engine：数据库
    con.execute('alter table test1 modify column name varchar(30);')
    con.execute('ALTER TABLE test1 ADD PRIMARY KEY (`id`);')

# 4，读取数据库sql
sql = ''' select * from test1; '''
df = pd.read_sql_query(sql, engine)
print(df)
print(df['name'][1])


print(df.duplicated().sum())
print(df.describe().T)
print(df[df.id < 3])
print(df[df.id < 3].count())
print(df.isnull().sum())
# print(df[df.IMEI.isnull()].head())
# print(df.loc[df.IMEI.isnull(), "USER_NAME"])
# # df.USER_NAME = df.USER_NAME + "NULL"
# # str(df.USER_NAME).replace("NULL", "")
# x = df.loc[df.IMEI.isnull(), "USER_NAME"]
# df.loc[df.IMEI.isnull(), "USER_NAME"] = [i + "NULL" for i in x]
# # df.columns = [x.strip() for x in df.columns.values]   # 将列表名中前后空格去掉了。

