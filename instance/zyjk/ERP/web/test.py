# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2022-7-19
# Description: 盛蕴erp管理平台
# 192.168.0.65

#***************************************************************

import os, sys

from ErpPO import *
Erp_PO = ErpPO()

from PO.StrPO import *
Str_PO = StrPO()
from PO.TimePO import *
Time_PO = TimePO()
from PO.DataPO import *
Data_PO = DataPO()

from PO.MysqlPO import *
# iUrl = "http://192.168.0.238:8090"
# db_ip = "192.168.0.238"
# db_database = "crmtest"

iUrl = "http://192.168.0.245:8080"
db_ip = "192.168.0.244"
db_database = "crm"
db_username = "root"
db_password = "ZAQ!2wsx"
db_port = 3306
Mysql_PO = MysqlPO(db_ip, db_username, db_password, db_database, db_port)

db_ip2 = "192.168.0.65"
db_username2 = "ceshi"
db_password2 = "123456"
db_port2 = 3336
db_database2 = "TD_OA"
Mysql_PO_OA = MysqlPO(db_ip2, db_username2, db_password2, db_database2, db_port2)

# 加载表格数据，读取测试用例
from PO.OpenpyxlPO import *
Sys_PO.killPid('EXCEL.EXE')
Openpyxl_PO = OpenpyxlPO("report.xlsx")



# ------------------------------------------------------------------------------------------------

# oa
Erp_PO.login("http://192.168.0.65", "liuting", "")
Erp_PO.clickMemuOA("盛蕴ERP", "盛蕴ERP（演示）")


# erp，全屏盛蕴erp管理平台
Erp_PO.maxBrowser(1)
# Oa_Po.memuERP("统计报表", "会议分析表")

# 将 “开发计划总揽” 内容保存excel
Erp_PO.clickMemuERP("统计报表", "开发计划总揽")
list1 = Erp_PO.Web_PO.getXpathsText("//tr")
# print(list1)
for i in range(len(list1)):
    list3 = str(list1[i]).split("\n")
    Openpyxl_PO.setRowValue({i+1: list3})
Openpyxl_PO.save()


# excel导入数据库表
Mysql_PO.xlsx2db("report.xlsx", "12345", sheet_name="Sheet1", index=True)
# 生成html
Mysql_PO.getReportFromDb("erp_开发计划总揽_", str(Time_PO.getDateTime()), "12345")


