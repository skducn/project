# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2022-6-30
# Description: erp - 统计报表
# 测试：
# 接口文档：http://192.168.0.238:8090/doc.html
# 数据库：192.168.0.238
# 预发布：
# 接口文档：http://192.168.0.245:8080/doc.html
# 数据库：192.168.0.244
#***************************************************************

import requests, json
import urllib3, math
urllib3.disable_warnings()
from ErpPO import *
Erp_PO = ErpPO()
from PO.StrPO import *
Str_PO = StrPO()
from PO.TimePO import *
Time_PO = TimePO()
from PO.DataPO import *
Data_PO = DataPO()
from PO.MysqlPO import *
from PO.OpenpyxlPO import *
Sys_PO.killPid('EXCEL.EXE')
caseExcel = "i_erp_reportField_case.xlsx"
Openpyxl_PO = OpenpyxlPO(caseExcel)
# 预发布接口文档ip
iUrl = "http://192.168.0.245:8080"
# 预发布数据库ip
db_ip = "192.168.0.244"
Mysql_PO = MysqlPO(db_ip, "root", "ZAQ!2wsx", "crm", 3306)
Mysql_PO_OA = MysqlPO("192.168.0.65", "ceshi", "123456", "TD_OA", 3336)

# 获取所有地区经理和代表的id
# db_t_userId_userName = Mysql_PO_OA.execQuery("select BYNAME, UID, USER_NAME from `user` where NOT_LOGIN=0 AND USER_PRIV_NAME='地区经理' or USER_PRIV_NAME='医药代表'")
# (('niuxuebin', 81, '钮学彬'), ('huangxinhui', 84, '黄新晖'),

Erp_PO.getToken("liuting")
# 爬取微信小程序页面数据（Charles爬取小程序数据，对SSL链接，需设置Proxy - SSL Proxying setting中 Enabel及include SSL地址）
# 消息
Erp_PO.getResponseByApplet("https://oa-test.zy-health.net/workSummary/pageList?currPage=1&pageSize=10")
# 获取客户信息
Erp_PO.postResponseByApplet("https://oa-test.zy-health.net/customer/queryCustomerApprovalPendingList",{
	"currPage": 1,
	"pageSize": 999,
	"searchCondition": ""
})

Erp_PO.postResponseByApplet("https://oa-test.zy-health.net/customer/queryCustomerInfoList",
                            {
                                "approveMark": "",
                                "currPage": 1,
                                "doubleAMark": "",
                                "meetingAfterMark": "",
                                "meetingBeforeMark": "",
                                "meetingDevelopMark": "",
                                "pageSize": 10,
                                "patientCaseMark": 1,
                                "potentialityMark": "",
                                "searchCondition": "",
                                "cusMoreData": True
                            }
                            )
# sys.exit(0)

# # [main]

# # 1拜访分析表(visitAnalysis)
# print("1，获取拜访分析表接口数据")
# varTitle, startTime, endTime = Erp_PO.visitAnalysis_I(db_ip, iUrl, Openpyxl_PO, Mysql_PO)
#
# print("2，获取浏览器前端页面数据")
# Erp_PO.getBrowserData_visitAnalysis(startTime, endTime, 'b', Openpyxl_PO)
#
# print("3，将i接口sheet与b浏览器数据sheet比对,生成新表i%b")
# varNewSheet = Openpyxl_PO.setSheetByDiff("i", "b")
#
# print("4，对新表生成结果状态")
# Erp_PO.getResult(varNewSheet, Openpyxl_PO)
#
# print("5，excel导入数据库表")
# Mysql_PO.xlsx2db(caseExcel, "12345", sheet_name=varNewSheet, index=True)
#
# print("6，生成html，打开表格")
# Erp_PO.db2html(Mysql_PO, varTitle)
# Openpyxl_PO.openSheet(Sheet="i%b")
#
#-----------------------------------------------------------------------------------------------------------------------
#
# # 2会议分析表(meetingAnalysis)
# print("1，获取会议分析表接口数据")
# varTitle, startTime, endTime = Erp_PO.meetingAnalysis_I(db_ip, iUrl, Openpyxl_PO, Mysql_PO)
# #
# print("2，获取浏览器前端页面数据")
# Erp_PO.getBrowserData_meetingAnalysis(startTime, endTime, 'b', Openpyxl_PO)
#
# print("3，将i接口sheet与b浏览器数据sheet比对,生成新表i%b")
# varNewSheet = Openpyxl_PO.setSheetByDiff("i", "b")
# #
# print("4，对新表生成结果状态")
# Erp_PO.getResult(varNewSheet, Openpyxl_PO)
#
# print("5，excel导入数据库表")
# Mysql_PO.xlsx2db(caseExcel, "12345", sheet_name=varNewSheet, index=True)
#
# print("6，生成html，打开表格")
# Erp_PO.db2html(Mysql_PO, varTitle)
# Openpyxl_PO.openSheet(Sheet="i%b")


# #-----------------------------------------------------------------------------------------------------------------------
# #
# # # 3投入产出分析表(inputOutput)
# print("1，获取投入产出分析表接口数据")
# varTitle, startTime, endTime = Erp_PO.inputOutput_I(db_ip, iUrl, Openpyxl_PO, Mysql_PO)
# # #
# print("2，获取浏览器前端页面数据")
# # startTime = "2022-07-01"
# # endTime = "2022-07-30"
# Erp_PO.getBrowserData_inputOutput(startTime, endTime, 'b', Openpyxl_PO)
# #
# print("3，将i接口sheet与b浏览器数据sheet比对,生成新表i%b")
# varNewSheet = Openpyxl_PO.setSheetByDiff("i", "b")
# #
# print("4，对新表生成结果状态")
# Erp_PO.getResult(varNewSheet, Openpyxl_PO)
#
# print("5，excel导入数据库表")
# Mysql_PO.xlsx2db(caseExcel, "12345", sheet_name=varNewSheet, index=True)
#
# print("6，生成html，打开表格")
# Erp_PO.db2html(Mysql_PO, varTitle)
# Openpyxl_PO.openSheet(Sheet="i%b")

# -----------------------------------------------------------------------------------------------------------------------
# # 4协访分析表(helpingAnalysis)
# print("1，获取协访分析表接口数据")
# varTitle, startTime, endTime = Erp_PO.helpingAnalysis_I(db_ip, iUrl, Openpyxl_PO, Mysql_PO)
#
# print("2，获取浏览器前端页面数据")
# Erp_PO.getBrowserData_helpingAnalysis(startTime, endTime, 'b', Openpyxl_PO)
#
# print("3，接口sheet（i）与浏览器sheet（b）比对，生成差异表i%b")
# varNewSheet = Openpyxl_PO.setSheetByDiff("i", "b")
#
# print("4，更新差异表结果状态")
# Erp_PO.getResult(varNewSheet, Openpyxl_PO)
#
# print("5，将差异表导入数据库")
# Mysql_PO.xlsx2db(caseExcel, "12345", sheet_name=varNewSheet, index=True)
#
# print("6，生成html，打开表格")
# Erp_PO.db2html(Mysql_PO, varTitle)
# Openpyxl_PO.openSheet(Sheet="i%b")Input


#-----------------------------------------------------------------------------------------------------------------------
# #
# # # 5重点客户投入有效性分析(customerInput)
# print("1，获取重点客户投入有效性分析接口数据")
# varTitle, tbl_month = Erp_PO.customerInput_I(db_ip, iUrl, Openpyxl_PO, Mysql_PO)
#
# print("2，获取浏览器前端页面数据")
# Erp_PO.getBrowserData_customerInput(tbl_month, 'b', Openpyxl_PO)
#
# print("3，将i接口sheet与b浏览器数据sheet比对,生成新表i%b")
# varNewSheet = Openpyxl_PO.setSheetByDiff("i", "b")
#
# print("4，对新表生成结果状态")
# Erp_PO.getResult(varNewSheet, Openpyxl_PO)
#
# print("5，excel导入数据库表")
# Mysql_PO.xlsx2db(caseExcel, "12345", sheet_name=varNewSheet, index=True)
#
# print("6，生成html，打开表格")
# Erp_PO.db2html(Mysql_PO, varTitle)
# Openpyxl_PO.openSheet(Sheet="i%b")


# -----------------------------------------------------------------------------------------------------------------------
# # 6开发计划总揽(devPlanOverall)
# print("1，获取开发计划总揽接口数据")
# varTitle, product_id = Erp_PO.devPlanOverall_I(db_ip, iUrl, Openpyxl_PO, Mysql_PO)
#
# print("2，获取浏览器前端页面数据")
# Erp_PO.getBrowserData_devPlanOverall(product_id, 'b', Openpyxl_PO)
#
# print("3，将i接口sheet与b浏览器数据sheet比对,生成新表i%b")
# varNewSheet = Openpyxl_PO.setSheetByDiff("i", "b")
#
# print("4，对新表生成结果状态")
# Erp_PO.getResult(varNewSheet, Openpyxl_PO)
#
# print("5，excel导入数据库表")
# Mysql_PO.xlsx2db(caseExcel, "12345", sheet_name=varNewSheet, index=True)
#
# print("6，生成html，打开表格")
# Erp_PO.db2html(Mysql_PO, varTitle)
# Openpyxl_PO.openSheet(Sheet="i%b")