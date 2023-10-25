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


def updateTable(sheetName, tableName):
    Sqlserver_PO.execute("drop table " + tableName)
    Sqlserver_PO.xlsx2db('规则db.xlsx', sheetName, tableName)
    # Sqlserver_PO.execute("ALTER TABLE %s ADD id1 INT NOT NULL IDENTITY(1,1) primary key (id1) " % ('健康评估'))  # 新增id自增主键
    Sqlserver_PO.execute("ALTER TABLE %s alter column id int not null" % (tableName))  # 设置主id不能为Null
    Sqlserver_PO.execute("ALTER TABLE %s add PRIMARY KEY (id)" % (tableName))  # 设置主键（条件是id不能为Null）
    Sqlserver_PO.execute("ALTER TABLE %s ADD var varchar(111)" % (tableName))  # 临时变量

# updateTable('健康评估', '健康评估')
# updateTable('健康干预', '健康干预')
# updateTable('中医体质辨识', '中医体质辨识')
# updateTable('儿童健康干预', '儿童健康干预')
# updateTable('已患和高风险疾病评估', '疾病评估')


# updateTable('疾病身份证', '疾病身份证')
updateTable('测试规则', '测试规则')



