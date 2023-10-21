# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-10-20
# Description: excel导入db，通过pandas读取
#***************************************************************

from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO(Configparser_PO.DB("host"), Configparser_PO.DB("user"), Configparser_PO.DB("password"), Configparser_PO.DB("database"), "utf8")  # 测试环境
Sqlserver_PO.execute("drop table 健康评估")
Sqlserver_PO.xlsx2db('规则db.xlsx', "健康评估", "健康评估")
Sqlserver_PO.execute("ALTER TABLE %s ADD id INT NOT NULL IDENTITY(1,1) primary key (id) " % ('健康评估'))  # 新增id自增主键
Sqlserver_PO.execute("ALTER TABLE %s ADD var varchar(111)" % ('健康评估')) # 临时变量


# Sqlserver_PO.execute("drop table jh_jkgy")
# Sqlserver_PO.xlsx2db('规则db.xlsx', "健康干预", "jh_jkgy")
# Sqlserver_PO.execute("ALTER TABLE %s ADD id INT NOT NULL IDENTITY(1,1) primary key (id) " % ('jh_jkgy'))  # 新增id自增主键
# Sqlserver_PO.execute("ALTER TABLE %s ADD var varchar(55)" % ('jh_jkgy')) # # 临时变量


# Sqlserver_PO.xlsx2db('规则db.xlsx', "健康干预中医体质辨识", "1_jh_zytzsb")
# Sqlserver_PO.xlsx2db('规则db.xlsx', "儿童健康干预", "1_jh_etjkgy")
# Sqlserver_PO.xlsx2db('规则db.xlsx', "已患和高风险疾病评估", "1_jh_yhhgfxjbpg")

# Sqlserver_PO.xlsx2db('规则db.xlsx', "疾病身份证", "jh_idcard")

