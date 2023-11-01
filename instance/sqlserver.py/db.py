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

# import os, sys
# sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
# # from PO import SqlserverPO, MysqlPO
# *****************************************************************

from PO.SqlserverPO import *


# todo sqlserver
# **********************************************************************************************************************************
# 区域平台 - 人名医院(sqlserver)
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "peopleHospital", "utf8")  # 测试环境
# Sqlserver_PO.dbDesc('aaa')

Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "GBK")
Sqlserver_PO.dbRecord('*', 'varchar', '310101202308070001')  # 搜索所有表符合条件的记录.

# print("1 查看数据库表结构（字段、类型、大小、可空、注释）".center(100, "-"))
# Sqlserver_PO.dbDesc()  # 1，所有表结构

# **********************************************************************************************************************************
# 社区健康平台
# Sqlserver_PO = SqlserverPO.SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "GBK")  # 测试环境
# Sqlserver_PO.dbDesc()
# Sqlserver_PO.dbDesc('HRCOVER')
# Sqlserver_PO.dbDesc('原始治理规则')
# Sqlserver_PO.dbDesc('HRCOVER',  ['ID', 'NAME'])
# Sqlserver_PO.dbDesc('HRD%')
# Sqlserver_PO.dbDesc('HRD%', ['PID', 'ID', 'NAME'])
# Sqlserver_PO.dbDesc('%', ["ID", "PID"])  # 表名中带有UpmsUser字符的表中Birthday字段的结构
# Sqlserver_PO.dbRecord('HRCOVER', 'varchar', '%刘斌龙%')  # 搜索指定表符合条件的记录.
# Sqlserver_PO.dbRecord('HRCOVER', 'varchar', '%张*%')  # 搜索指定表符合条件的记录.
# Sqlserver_PO.dbRecord('*', 'varchar', '%刘斌龙%')  # 搜索所有表符合条件的记录.
# Sqlserver_PO.dbRecord('*', 'money', '%34.5%')
# **********************************************************************************************************************************
# EHR 电子健康档案(sqlserver)
# Sqlserver_PO = SqlserverPO.SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "EHRDC", "GBK")  # 测试环境
# Sqlserver_PO = SqlserverPO.SqlServerPO("192.168.0.234", "sa", "Zy@123456", "EHRITF", "utf8")  # 测试环境
# Sqlserver_PO.dbDesc()
# Sqlserver_PO.dbDesc('itf_tb_chronic_main')
# Sqlserver_PO.dbDesc('ITF_TB_EXAMINATION_INFO',  ['registerTypeCode', 'name'])
# Sqlserver_PO.dbDesc('tb_dc_dm_%')
# Sqlserver_PO.dbDesc('tb_dc_dm_%', ['guid', 'drugTypeCodeSystem'])  # # 5，批量输出tb开头表中包含id或page字段的表结构信息
# Sqlserver_PO.dbDesc('%', ["idCardNo", "ehrNum"])  # 表名中带有UpmsUser字符的表中Birthday字段的结构
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
# EHR
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "EHR_CDRINFO", "GBK")  # 测试环境
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
# **********************************************************************************************************************************
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
# **********************************************************************************************************************************
# 白茅岭 (sqlserver)
# sqlserver_PO = SqlserverPO.SqlServerPO("192.168.0.195", "DBuser", "qwer#@!", "bmlpimpro")  # 测试环境
# sqlserver_PO.dbRecord('*', 'varchar', '%王维强%')
# **********************************************************************************************************************************
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
# **********************************************************************************************************************************
# fsms 家床(sqlserver)
# sqlserver_PO = SqlserverPO.SqlServerPO("192.168.0.195", "DBuser", "qwer#@!", "fsms")  # 测试环境
# sqlserver_PO.dbDesc()  # 所有表结构
# sqlserver_PO.dbRecord('*', 'varchar', '%测试1%')  # 模糊搜索所有表中带yoy的char类型。
# sqlserver_PO.dbRecord('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
# sqlserver_PO.dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# sqlserver_PO.dbRecord('*','timestamp', u'%2019-01%')  # 模糊搜索所有表中带2019-01的timestamp类型。


# todo mysql
# **********************************************************************************************************************************
# 区域平台(mysql)
# mysql_PO = MysqlPO.MysqlPO("192.168.0.234", "root", "Zy123456", "regional-user", 3306)   # 测试环境
# mysql_PO.dbRecord('*', 'char', u'%金浩%')
# **********************************************************************************************************************************
# BI集成平台(mysql)
# mysql_PO = MysqlPO.MysqlPO("192.168.0.195", "root", "Zy123456", "bidev", 3306)  # 测试环境
# mysql_PO.dbRecord('*', 'char', u'%耳、鼻、咽喉科%')
# # mysql_PO.dbRecord('*', 'float', u'%295.54%')
# **********************************************************************************************************************************
# 患者360
# mysql_PO = MysqlPO.MysqlPO("192.168.0.195", "root", "Zy123456", "upvdev", 3306)  # 测试环境
# # mysql_PO.dbRecord('*', 'char', u'%郑和成%')
# # mysql_PO.dbRecord('*', 'float', u'%295.54%')
# **********************************************************************************************************************************
# 禅道
# mysql_PO = MysqlPO.MysqlPO("192.168.0.211", "readonly", "benetech123", "zentaoep", 3306)
# **********************************************************************************************************************************
# 招远防疫
# mysql_PO = MysqlPO.MysqlPO("121.36.248.183", "root", "Tunicorn3y2dH", "saascmstest", 2306)  # 环境
# mysql_PO = MysqlPO.MysqlPO("192.168.0.231", "root", "Zy123456", "epidemic_center", 3306)  # 测试环境
