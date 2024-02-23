# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2019-4-16
# Description: 项目实例
# 查看表结构（字段、类型、大小、可空、注释），注意，表名区分大小写  dbDesc()
# 查找记录  dbRecord('*', 'money', '%34.5%')
# 创建、删除表，插入、删除记录
# *****************************************************************

from PO.SqlserverPO import *


# todo 公卫
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHUSERS", "GBK")
# Sqlserver_PO = SqlServerPO("192.168.180.237", "PHUR_TEST", "testPH@2023", "zyconfig_pprod", "GBK")  # 预发布，通过VPN访问
# Sqlserver_PO.dbDesc()


# 创建表（如存在先删除）
# Sqlserver_PO.execute(""" IF OBJECT_ID('a_test', 'U') IS NOT NULL DROP TABLE a_test
# CREATE TABLE a_test (
#     id INT NOT NULL,
#     name VARCHAR(100),
#     salesrep VARCHAR(100),
#     PRIMARY KEY(id)
# )
# """)

# alter table A_testrule ADD ID2 INT identity(1,1) primary key;

# # 插入多条记录
# Sqlserver_PO.executemany("INSERT INTO a_test VALUES (%d, %s, %s)", [(1, 'John Smith2', 'John Doe3'), (2, 'Jane Doe', 'Joe Dog'), (3, 'Mike T.', 'Sarah H.')])

# # 删除记录
# Sqlserver_PO.execute("DELETE FROM a_test WHERE id = 2")
#
# # 删除表
# Sqlserver_PO.execute("DROP TABLE a_test")


# todo 社区健康平台（标准版）
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "GBK")
# Sqlserver_PO.dbRecord('*', 'varchar', '110101196407281506')
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


# todo 社区健康平台（静安）
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC_JINGAN", "GBK")
# Sqlserver_PO.dbDesc()


# todo 老年人体检
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHS", "GBK")
# Sqlserver_PO.dbDesc()


# todo 重点人群
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "COVID", "GBK")
# Sqlserver_PO.dbDesc()


# todo 家床
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "fsms20", "GBK")
# Sqlserver_PO.dbDesc()

# todo PIM基层健康管理平台
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "pimtest", "GBK")
# Sqlserver_PO.dbDesc()

# todo 区域平台（人名医院）
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "peopleHospital", "utf8")  
# Sqlserver_PO.dbDesc('aaa')

# todo EHR电子健康档案
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "EHRDC", "GBK")  
# Sqlserver_PO.dbDesc()

# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "EHRITF", "GBK")  
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
# Sqlserver_PO.dbRecord('*', 'varchar', '17a7929801e54f1ca8ab69f18c086b00')
# Sqlserver_PO.dbRecord('*', 'datetime', '2018-10-15 18:21%')  # 模糊搜索所有表中带2018-10-15 18:21%的datetime类型。
# l = Sqlserver_PO.getAllFields('HrCover')  # 获取表结构字段列表
# print(l)

# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "EHR_CDRINFO", "GBK")  
# r = Sqlserver_PO.execQuery('select * from tb_org where id=%s ' % ('1'))
# print(r)
# tmpList = Sqlserver_PO.execQuery("SELECT convert(nvarchar(255), Categories)  FROM HrRule where RuleId='00081d1c0cce49fd88ac68b7627d6e1c' ")  # 数据库数据自造
# l_result = Sqlserver_PO.execQuery('select top 1 (select sum(live_people_num) from (select live_people_num,org_name from report_qyyh group by org_code,org_name,live_people_num) a)  livePeopleNum from report_qyyh')
# print(l_result)
# l_result = Sqlserver_PO.execQuery('select convert(nvarchar(20), Name) from HrCover where id=%s ' % (1))  # 中文乱码使用 convert(nvarchar(20), 字段)
# l_result = Sqlserver_PO.execQuery('select Name from HrCover where id=%s ' % (1))  # 中文乱码使用 convert(nvarchar(20), 字段)
# print(l_result)

# todo 系统用户中心
# Sqlserver_PO = SqlServerPO("192.168.0.195", "ZYDBUser", "qwer123.", "usertest", "GBK")  
# Sqlserver_PO.dbDesc()
# Sqlserver_PO.dbDesc('sys_user')   # 查看myclass表结构
# Sqlserver_PO.dbDesc('b*')  # 查看所有b开头的表结构（通配符*） ???
# Sqlserver_PO.dbDesc('book', 'id,page')   # 查看book表id,page字段的结构
# Sqlserver_PO.dbDesc('b*', 'id,page')  # 查看所有b开头的表中id字段的结构（通配符*）
# Sqlserver_PO.dbRecord('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
# Sqlserver_PO.dbRecord('*', 'varchar', '%测试%')
# Sqlserver_PO.dbRecord('*', 'money', '%34.5%')
# Sqlserver_PO.dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# Sqlserver_PO.dbRecord('*','timestamp', u'%2019-01%')  # 模糊搜索所有表中带2019-01的timestamp类型。


# todo 白茅岭 (sqlserver)
# Sqlserver_PO = SqlServerPO("192.168.0.195", "ZYDBUser", "qwer#@!", "bmlpimpro", "GBK")  
# Sqlserver_PO.dbDesc()
# Sqlserver_PO.dbRecord('*', 'varchar', '%王维强%')


# todo 白茅岭（注意：234上也存在）
# Sqlserver_PO = SqlServerPO("192.168.0.195", "DBuser", "qwer#@!", "bmlpimpro", "GBK")  
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "bmlpimpro", "GBK")
# Sqlserver_PO.dbDesc()   # 查看所有表结构


# todo fsms家床
# SqlServerPO = SqlServerPO("192.168.0.195", "DBuser", "qwer#@!", "fsms", "GBK")  
# SqlServerPO.dbDesc()  
# sqlserver_PO.dbRecord('*', 'varchar', '%测试1%')  # 模糊搜索所有表中带yoy的char类型。
# sqlserver_PO.dbRecord('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
# sqlserver_PO.dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# sqlserver_PO.dbRecord('*','timestamp', u'%2019-01%')  # 模糊搜索所有表中带2019-01的timestamp类型。
# sqlserver_PO.dbDesc('t_system_patient_basic_info')   # 查看myclass表结构
# sqlserver_PO.dbDesc('b*')  # 查看所有b开头的表结构（通配符*） ???
# sqlserver_PO.dbDesc('book', 'id,page')   # 查看book表id,page字段的结构
# sqlserver_PO.dbDesc('b*', 'id,page')  # 查看所有b开头的表中id字段的结构（通配符*）
# sqlserver_PO.dbRecord('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
# sqlserver_PO.dbRecord('*', 'varchar', '%海鹰居委会%')
# sqlserver_PO.dbRecord('*', 'money', '%34.5%')
# sqlserver_PO.dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# sqlserver_PO.dbRecord('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。


# todo BI集成平台
# SqlServerPO = SqlServerPO("192.168.0.195", "DBuser", "qwer#@!", "bidev", "GBK")  
# SqlServerPO.dbDesc()  



# todo 实例
# print("1 查看数据库表结构（字段、类型、大小、可空、注释）".center(100, "-"))
# # Sqlserver_PO.dbDesc()  # 1，所有表结构
# Sqlserver_PO.dbDesc("aaa")  # 2，单表结构
# Sqlserver_PO.dbDesc('s%')  # 3，带通配符表结构
# Sqlserver_PO.dbDesc('tb_org', ['id', 'org_name'])  # 4,单表结构的可选字段
# Sqlserver_PO.dbDesc('s%', ['id', 'kaId'])  # 5，带通配符表结构的可选字段(只输出找到字段的表)
# Sqlserver_PO.dbDesc(0, ['id', 'kaId', 'org_name'])  # 6，所有表结构的可选字段(只输出找到字段的表)

# print("2 查找记录".center(100, "-"))
# Sqlserver_PO.dbRecord('aaa', 'int', '%2%')  # 搜索指定表符合条件的记录.
# Sqlserver_PO.dbRecord('*', 'varchar', '310101202308070001')  # 搜索所有表符合条件的记录.
# Sqlserver_PO.dbRecord('QYYH', 'varchar', '132222196702240429')  # 搜索所有表符合条件的记录.
# Sqlserver_PO.dbRecord('TB_RIS_REPORT2', 'varchar', '000E434B-48BF-4B58-945B-6FDCD46CDECE')  # 搜索所有表符合条件的记录.
# Sqlserver_PO.dbRecord('*', 'money', '%34.5%')l
# Sqlserver_PO.dbRecord('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# Sqlserver_PO.dbRecord('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。

