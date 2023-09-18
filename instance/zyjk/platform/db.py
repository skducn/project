# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-9-11
# Description: 数据库创建记录
# *****************************************************************

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from PO import SqlserverPO, MysqlPO


# 社区健康平台
Sqlserver_PO = SqlserverPO.SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "peopleHospital", "GBK")  # 测试环境

# todo 创建表
# Sqlserver_PO.crtTable('''CREATE TABLE jh2
#        (ID INT PRIMARY KEY     NOT NULL,
#         NAME           TEXT    NOT NULL,
#         AGE            INT     NOT NULL,
#         ADDRESS        CHAR(50),
#         SALARY         REAL);''')

#
# a = Sqlserver_PO.getFieldType('jh2','datetime1')
# print(a)

# todo 获取表中必填项的字段名和类型
# d_NotNullNameType = Sqlserver_PO.getNotNullNameType('jh')
# print(d_NotNullNameType)  # # {'ID': 'int', 'NAME': 'text', 'AGE': 'int'}

# todo 生成记录（默认必填项有值)
# Sqlserver_PO.instRecordByNotNull("jh")

# todo 获取表主键key
# primaryKey = Sqlserver_PO.getPrimaryKey('jh')
# print(primaryKey)  # ID

# todo 获取表主键的最大值
# d_primaryKeyMaxValue = (Sqlserver_PO.getPrimaryKeyMaxValue('jh'))
# print(d_primaryKeyMaxValue)  #  # {'ID': 77}

# todo 获取表主键最大值
# d_primaryValue = Sqlserver_PO.getPrimaryKeyMaxValue('jh')
# print(d_primaryValue)  # {'ID': 1}

# todo 更改数据
# Sqlserver_PO.updtRecord('jh', "AGE=443,salary=13,address='中国'")
# Sqlserver_PO.updtRecord('jh', 'AGE=100,salary=235', varTop=2)

# todo 遍历所有表，对空表生成记录
# l_tables = Sqlserver_PO.getTables()
# print(l_tables)
# for t in range(len(l_tables)):
#     # 直接从系统表中查询表的总记录数（特别适合大数据）
#     a = Sqlserver_PO.execQuery("SELECT rows FROM sysindexes WHERE id = OBJECT_ID('" + l_tables[t] + "') AND indid < 2")
#     # print(l_tables[t], a[0]['rows'])
#     if a[0]['rows'] == 0 :
#         Sqlserver_PO.instRecordByNotNull(l_tables[t])
#         print(l_tables[t])
#         # ASSESS_MEDICATION
#         # DATE_TAME_INFO
#         # HRCOVER_copy1
#         # jh2
#         # T_ASSESS_DATEFORM
#         # T_ASSESS_VICCINE_copy1
#         # T_EHALTH_NCG
#         # T_EHALTH_XZ
#         # T_EHALTH_XZ_ZIZB
#         # T_HEALTH_REPORT
#         # TB_CIS_BED_INFO
#         # TB_CIS_MAIN
#         # TB_DC_DM_CLINICAL
#         # TB_DC_DM_VISIT
#         # TB_DC_EXAMINATION_ASSESS
#         # TB_DC_EXAMINATION_EXPOSURE
#         # TB_DC_EXAMINATION_FAMILY_HISTORY
#         # TB_DC_EXAMINATION_IMMUNIZATION
#         # TB_DC_EXAMINATION_IP_HISTORY
#         # TB_DC_HTN_ASSESS_FIRST
#         # TB_DC_HTN_ASSESS_YEAR
#         # TB_DC_HTN_CLINICAL
#         # TB_LIS_REPORT_MICROBIO

# todo 对生成记录（默认必填项有值)
# Sqlserver_PO.instRecordByNotNull("TB_LIS_REPORT_MICROBIO")
# Sqlserver_PO.instRecordByNotNull("TB_HIS_MZ_Reg")
Sqlserver_PO.instRecordByNotNull("EMR_ADMISSION_ASSESSMENT")


# todo 设置非空字段
# varList = ['jh2', 'ADDRESS']
# Sqlserver_PO.updtRecord(varList[0], varList[1] + "=''")

# Sqlserver_PO.updtRecord()
# Sqlserver_PO.updtRecord('jh', "ADDRESS=''", varTop=1)



# 区域平台
# mysql_PO = MysqlPO.MysqlPO("192.168.0.234", "root", "Zy123456", "regional-user", 3306)   # 测试环境
# mysql_PO.dbRecord('*', 'char', u'%金浩%')