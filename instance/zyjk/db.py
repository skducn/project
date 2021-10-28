# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2019-4-16
# Description: dbDesc()搜索表结构，dbRecord()搜索表记录
# *****************************************************************
# SELECT A.name AS table_name,B.name AS column_name,B.is_nullable,C.value AS column_description,d.name AS colType FROM sys.tables A
# INNER JOIN sys.columns B ON B.object_id = A.object_id
# LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id
# inner join systypes d on B.user_type_id=d.xusertype
# WHERE A.name ='UpmsUser'
#
# SELECT A.name AS table_name FROM sys.tables A
# SELECT * FROM sys.tables A
#
# SELECT A.name AS table_name,B.* FROM sys.tables A
# INNER JOIN sys.columns B ON B.object_id = A.object_id
# WHERE A.name ='UpmsUser'
#
# SELECT A.name AS table_name,B.name AS column_name,B.is_nullable,d.* FROM sys.tables A
# INNER JOIN sys.columns B ON B.object_id = A.object_id
# inner join systypes d on B.user_type_id=d.xusertype
# WHERE A.name ='COMMONATTACHMENT'
#
# SELECT a.name,b.name,c.DATA_TYPE,b.* FROM sys.tables a join sys.columns b on b.object_id = a.object_id
# join INFORMATION_SCHEMA.COLUMNS c on b.name=c.COLUMN_NAME and a.name=c.TABLE_NAME
# where a.name='COMMONATTACHMENT'

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from PO import SqlserverPO, MysqlPO



# 系统用户中心(sqlserver)
# sqlserver_PO = SqlserverPO.SqlServerPO("192.168.0.195", "DBuser", "qwer#@!", "usertest")  # 测试环境
# sqlserver_PO.dbDesc()   # 查看所有表结构
# sqlserver_PO.dbDesc('sys_user')   # 查看myclass表结构
# sqlserver_PO.dbDesc('b*')  # 查看所有b开头的表结构（通配符*） ???
# sqlserver_PO.dbDesc('book', 'id,page')   # 查看book表id,page字段的结构
# sqlserver_PO.dbDesc('b*', 'id,page')  # 查看所有b开头的表中id字段的结构（通配符*）
# sqlserver_PO.dbRecord('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
# sqlserver_PO.dbRecord('*', 'varchar', '%测试%')
# sqlserver_PO.dbRecord('*', 'money', '%34.5%')
# sqlserver_PO.dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# sqlserver_PO.dbRecord('*','timestamp', u'%2019-01%')  # 模糊搜索所有表中带2019-01的timestamp类型。


# 白茅岭 (sqlserver)
# sqlserver_PO = SqlserverPO.SqlServerPO("192.168.0.195", "DBuser", "qwer#@!", "bmlpimpro")  # 测试环境
# sqlserver_PO.dbRecord('*', 'varchar', '%王维强%')


# PIM 基层健康管理平台(sqlserver)
# sqlserver_PO = SqlserverPO.SqlServerPO("192.168.0.195", "DBuser", "qwer#@!", "bmlpimpro")  # 测试环境
# sqlserver_PO.dbDesc()   # 查看所有表结构
# sqlserver_PO.dbDesc('t_system_patient_basic_info')   # 查看myclass表结构
# sqlserver_PO.dbDesc('b*')  # 查看所有b开头的表结构（通配符*） ???
# sqlserver_PO.dbDesc('book', 'id,page')   # 查看book表id,page字段的结构
# sqlserver_PO.dbDesc('b*', 'id,page')  # 查看所有b开头的表中id字段的结构（通配符*）
# sqlserver_PO.dbRecord('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
# sqlserver_PO.dbRecord('*', 'varchar', '%海鹰居委会%')
# sqlserver_PO.dbRecord('*', 'money', '%34.5%')
# sqlserver_PO.dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# sqlserver_PO.dbRecord('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。


# fsms 家床(sqlserver)
# sqlserver_PO = SqlserverPO.SqlServerPO("192.168.0.195", "DBuser", "qwer#@!", "fsms")  # 测试环境
# sqlserver_PO.dbDesc()  # 所有表结构
# sqlserver_PO.dbRecord('*', 'varchar', '%测试1%')  # 模糊搜索所有表中带yoy的char类型。
# sqlserver_PO.dbRecord('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
# sqlserver_PO.dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# sqlserver_PO.dbRecord('*','timestamp', u'%2019-01%')  # 模糊搜索所有表中带2019-01的timestamp类型。


# ***************************************************************
# ***************************************************************

# EHR 电子健康档案(sqlserver)
sqlserver_PO = SqlserverPO.SqlServerPO("192.168.0.234", "sa", "Zy@123456", "EHRDC")  # 测试环境
# Sqlserver_PO.dbDesc()  # 1，输出所有表结构信息（表名、别称、字段个数、字段、类型、大小、可空、注释）
# Sqlserver_PO.dbDesc('HrCover')   # 2，输出表结构信息
# Sqlserver_PO.dbDesc('tb_code_value', 'code,id,value')  # 3，输出表的部分字段结构信息
# Sqlserver_PO.dbDesc('tb_dc*')  # 4，输出tb_dc开头的表结构信息
# Sqlserver_PO.dbDesc('tb*', 'id,page')  # 5，输出tb开头表中包含id或page字段的表结构信息
sqlserver_PO.dbDesc('*', ["idCardNo", "ehrNum"])  # 表名中带有UpmsUser字符的表中Birthday字段的结构

# Sqlserver_PO.dbRecord('CommonDictionary', 'varchar', '%录音%')  # 搜索指定表符合条件的记录.
# Sqlserver_PO.dbRecord('*', 'varchar', '%高血压%')  # 搜索所有表符合条件的记录.
# Sqlserver_PO.dbRecord('*', 'money', '%34.5%')l
# Sqlserver_PO.dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# Sqlserver_PO.dbRecord('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。
# sqlserver_PO.dbRecord('UpmsUser', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 UpmsUser 表中内容包含 e10adc3949ba59abbe56e057f20f883e 的 varchar 类型记录。
# sqlserver_PO.dbRecord('CommonDictionaryType', 'datetime', '2018-10-15 18:21%')  # 模糊搜索所有表中带2018-10-15 18:21%的datetime类型。
# sqlserver_PO.dbRecord('*', 'varchar', '17a7929801e54f1ca8ab69f18c086b00')
# sqlserver_PO.dbRecord('*', 'datetime', '2018-10-15 18:21%')  # 模糊搜索所有表中带2018-10-15 18:21%的datetime类型。

# l = Sqlserver_PO.getAllFields('HrCover')  # 获取表结构字段列表
# print(l)


# **********************************************************************************************************************************

# 盛蕴CRM小程序(mysql)
# mysql_PO = MysqlPO.MysqlPO("192.168.0.233", "ceshi", "123456", "TD_APP", 3336)  # 测试环境
# mysql_PO.dbDesc()   # 所有表结构
# mysql_PO.dbDesc('fact*')  # 查看所有b开头的表结构（通配符*）
# mysql_PO.dbDesc('app_info')   # app_info表结构
# mysql_PO.dbDesc('fact*', 'Id,page')  # 查看所有b开头的表中id字段的结构（通配符*）
# mysql_PO.dbDesc('app_info', 'id,mid')   # 查看book表id,page字段的结构
# mysql_PO.dbRecord('user','char', '%13816109050%')  # 搜索myclass表中内容包含yoyo的char类型记录。
# mysql_PO.dbRecord('*', 'char', '13816109050')  # 模糊搜索所有表中带yoy的char类型。
# mysql_PO.dbRecord('*', 'varchar', u'%一次性使用有创压力传感器%')  # 模糊搜索所有表中带35的double类型。
# mysql_PO.dbRecord('*', 'datetime', u'%2019-04-12 15:13:23%')  # 模糊搜索所有表中日期类型为datetime的2019-04-12 15:13:23记录。
# mysql_PO.dbCreateDate()   # 查看所有表的创建时间
# mysql_PO.dbCreateDate('app_code')   # 查看book表创建时间
# mysql_PO.dbCreateDate('fact*')   # 查看所有b开头表的创建时间，通配符*
# mysql_PO.dbCreateDate('after', '2019-02-18')  # 查看所有在2019-02-18之后创建的表
# mysql_PO.dbCreateDate('>', '2019-02-18')  # 查看所有在2019-02-18之后创建的表
# mysql_PO.dbCreateDate('before', "2019-04-10")  # 显示所有在2019-12-08之前创建的表
# mysql_PO.dbCreateDate('<', "2019-02-18")  # 显示所有在2019-12-08之前创建的表


# # BI集成平台(mysql)
# mysql_PO = MysqlPO.MysqlPO("192.168.0.195", "root", "Zy123456", "bidev", 3306)  # 测试环境
# mysql_PO.dbRecord('*', 'char', u'%耳、鼻、咽喉科%')
# # mysql_PO.dbRecord('*', 'float', u'%295.54%')

# # 患者360(mysql)
# mysql_PO = MysqlPO.MysqlPO("192.168.0.195", "root", "Zy123456", "upvdev", 3306)  # 测试环境
# # mysql_PO.dbRecord('*', 'char', u'%郑和成%')
# # mysql_PO.dbRecord('*', 'float', u'%295.54%')
# # mysql_PO.dbDesc()   # 所有表结构
# mysql_PO.dbDesc('upv_blood_match_report')   # UpmsUser表结构

# # SAAS(mysql)
# mysql_PO = MysqlPO.MysqlPO("192.168.0.195", "root", "Zy123456", "saasecgdev", 3306)  # 测试环境
# mysql_PO = MysqlPO.MysqlPO("192.168.0.195", "root", "Zy123456", "saasuserdev", 3306)  # 测试环境
# mysql_PO.dbRecord('*', 'char', u'%什么是脑血栓%')
