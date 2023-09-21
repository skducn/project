# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-9-11
# Description: 区域平台 - 数据交换规则
# 【腾讯文档】数据交换之校验规则自动化
# https://docs.qq.com/sheet/DYmtpa2pTSUJhT0ZD?tab=xfisl0
# 接口文档 http://192.168.0.201:28801/doc.html
# 前端：http://192.168.0.213:1080/
# 【腾讯文档】区域平台数据质控流程  https://docs.qq.com/doc/DS2J0T1VsRlplWHF3
#***************************************************************

from PlatformRulePO import *
PlatformRule_PO = PlatformRulePO()
from PO.MysqlPO import *
Mysql_PO = MysqlPO("192.168.0.234", "root", "Zy_123456", "regional-dqc", 3306)
from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "peopleHospital", "utf8")  # 测试环境

TOKEN = PlatformRule_PO.getToken("jh", "123456")
print(TOKEN)

# 1，初始化测试数据，新增挂号表数据 全部为null，2023-9-18
Sqlserver_PO.genRecord("TB_HIS_MZ_Reg", {"GTHBZ": None, "GHRQ":"777"})  # 自动生成数据
# Sqlserver_PO.genRecord("TB_HIS_MZ_Reg")
# Sqlserver_PO.execute()

# # 2 测试-汇总测试
# PlatformRule_PO.testStatistics("2023-09-18 00:00:00", "2023-09-19 23:35:45", TOKEN)
#
# # 3，mysql中检查 t_data_report 和  t_data_log_err 数量
# a = Mysql_PO.execQuery("select count(*) from t_data_report")
# print(a)





