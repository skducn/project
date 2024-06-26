# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-12-27
# Description: petl 数据迁移
# http://www.51testing.com/?action-viewnews-itemid-7799188
# ·from_csv()：从CSV文件中读取数据表格。　　
# · from_excel()：从Excel文件中读取数据表格。　　
# · from_json()：从JSON文件中读取数据表格。　　
# · from_sql()：从SQL数据库中读取数据表格。　　
# · to_csv()：将数据表格写入CSV文件。　　
# · to_excel()：将数据表格写入Excel文件。　　
# · to_json()：将数据表格写入JSON文件。　　
# · to_sql()：将数据表格写入SQL数据库。

# https://pythonhosted.org/petl/0.10.2/index.html  petl v.0.10.12 文档
#***************************************************************

import petl as etl

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHUSERS", "utf8")  # 测试环境

# todo csv导入db
data = etl.fromcsv('data.csv')
print(data)
# +-----+------+-----+
# |id | name | age |
# +=====+======+=====+
# | 1   | john | 44  |
# +-----+------+-----+
# | 2   | yoyo | 42  |
# +-----+------+-----+
# | 3   | tige | 4   |
# +-----+------+-----+
Sqlserver_PO.crtTable('a_test000', 'id INTEGER PRIMARY KEY, name TEXT, age INTEGER')
etl.todb(data, Sqlserver_PO.conn, 'a_test000')


# todo xlsx转json文件
# import json
# data2 = etl.fromxlsx('data.xlsx')
# print(data2)
# d = etl.dicts(data2)  # <class 'petl.util.base.DictsView'>
# print(d)
# # {'id': 1, 'name': 'john', 'age': 44}
# # {'id': 2, 'name': 'yoyo', 'age': 42}
# # {'id': 3, 'name': 'tt', 'age': 4}
#
# for i in d:
#     json_data = json.dumps(i)
#     with open('jsondata1.json', 'a') as f:
#         f.write(json_data)


# todo db迁移到excel文件
from petl import look, fromdb
table1 = etl.fromdb(Sqlserver_PO.conn, 'select * from a_test000')
print(table1)

# etl.fromdb(Sqlserver_PO.conn, 'SELECT * FROM a_test').toxlsx('data22.xlsx')

# etl.fromdb(Sqlserver_PO.conn, 'a_test').toxlsx('data22.xlsx')
