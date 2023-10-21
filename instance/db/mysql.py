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

from PO.MysqlPO import *


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

