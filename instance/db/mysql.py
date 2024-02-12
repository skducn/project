# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2019-4-16
# Description: 项目实例
# 1，查看表结构  dbDesc()
# 2，搜索记录  dbRecord('*', 'money', '%34.5%')
# 3，查询表创建时间  dbCreateDate()
# *****************************************************************

from PO.MysqlPO import *


# todo 健康俱乐部
Mysql_PO = MysqlPO("121.36.248.183", "clubtest", "Club5678", "hclub", 2306)
# Mysql_PO.dbDesc()


# todo 区域平台
# Mysql_PO = MysqlPO("192.168.0.234", "root", "Zy_123456", "regional-user", 3306)   
# Mysql_PO = MysqlPO("192.168.0.234", "root", "Zy_123456", "regional-upv", 3306)
# Mysql_PO = MysqlPO("192.168.0.234", "root", "Zy_123456", "regional-dict", 3306)
# Mysql_PO.dbDesc()
# Mysql_PO.dbRecord('*', 'char', u'%金浩%')


# todo 招远妇幼
# Mysql_PO = MysqlPO("192.168.0.234", "root", "Zy_123456", "hfauser", 3306)
# Mysql_PO.dbDesc()


# todo 高血压
# Mysql_PO = MysqlPO("192.168.0.234", "root", "Zy_123456", "saasusertest", 3306)   
# Mysql_PO = MysqlPO("192.168.0.234", "root", "Zy_123456", "saasosstest", 3306)   
# Mysql_PO = MysqlPO("192.168.0.234", "root", "Zy_123456", "saasecgtest", 3306)   
# Mysql_PO = MysqlPO("192.168.0.234", "root", "Zy_123456", "saascrftest", 3306)   
# Mysql_PO.dbDesc()


# todo 沪享瘦
# Mysql_PO = MysqlPO("192.168.0.234", "root", "Zy_123456", "saashypertensiontest", 3306)
# Mysql_PO = MysqlPO("192.168.0.234", "root", "Zy_123456", "saasusertest", 3306)   
# Mysql_PO.dbDesc()


# todo EPR3.0
# Mysql_PO = MysqlPO("192.168.0.234", "root", "Zy_123456", "crmtest", 3306)
# Mysql_PO = MysqlPO("192.168.0.234", "root", "Zy_123456", "zy_crmtest", 3306)  # 预发布
# Mysql_PO.dbDesc()


# todo OA
# Mysql_PO = MysqlPO("192.168.0.65", "ceshi", "123456", "TD_OA", 3336)
# Mysql_PO = MysqlPO("192.168.0.65", "ceshi", "123456", "TD_APP", 3336)
# Mysql_PO.dbDesc()


# todo 招远防疫
# Mysql_PO = MysqlPO("192.168.0.234", "root", "Zy_123456", "epidemic_center", 3306)   
# Mysql_PO.dbDesc()


# todo 禅道
# Mysql_PO = MysqlPO("192.168.0.211", "readonly", "benetech123", "zentaoep", 3306)
# Mysql_PO.dbDesc()