# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-11-6
# Description: # dm for win
# ***************************************************************u**


from PO.DmPO import *
Dm_PO = DmPO("192.168.0.234", "PHUSERS", "Zy123456789", "5236")  # 测试环境


# result = Dm_PO.execQuery("select * from PHUSERS.SYS_DRUG where id=1")
# print(result[0])  # (1, '1', '阿莫西林', 'AMXL', '111', '1111', 'QD', '每天一次', '1', '颗', '3', '12:00', '1', '规律', False)


# result = Dm_PO.execQuery("select * from 中医体质辨识 where id=%s" % (1))
# print(result[0])  # (1, 'ok', '2023/10/26 13:16:46', 'r12', 'ABNORMAL_STATUS', 'GY_TZBS01', '体质=平和质', '郭斐', '')



# Dm_PO.xlsx2db('规则db.xlsx', "疾病身份证", "疾病身份证")

def updateTable(sheetName, tableName):
    Dm_PO.execute("drop table " + tableName)
    Dm_PO.xlsx2db('规则db.xlsx', sheetName, tableName)
    # Sqlserver_PO.execute("ALTER TABLE %s ADD id1 INT NOT NULL IDENTITY(1,1) primary key (id1) " % ('健康评估'))  # 新增id自增主键
    Dm_PO.execute("ALTER TABLE %s alter column id int not null" % (tableName))  # 设置主id不能为Null
    Dm_PO.execute("ALTER TABLE %s add PRIMARY KEY (id)" % (tableName))  # 设置主键（条件是id不能为Null）
    Dm_PO.execute("ALTER TABLE %s ADD var varchar(111)" % (tableName))  # 临时变量


# updateTable('健康评估', '健康评估')
updateTable('健康干预', '健康干预')
# updateTable('中医体质辨识', '中医体质辨识')
# updateTable('儿童健康干预', '儿童健康干预')
# updateTable('疾病评估', '疾病评估')
# updateTable('疾病身份证', '疾病身份证')
