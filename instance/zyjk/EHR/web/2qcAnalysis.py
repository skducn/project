# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2019-12-11
# Description: 电子健康档案数据监控中心（PC端）之 质控分析
# 技巧：去掉字符串两端的数字， astring.strip(string.digits) ,如 123姓名，输出：姓名
# 扩展：astring.lstrip(string.digits) 去掉左侧数字  , astring.rstrip(string.digits) 去掉右侧数字
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


import numpy
from instance.zyjk.EHR.PageObject.DataMonitorPO import *
dataMonitor_PO = DataMonitorPO()
from PO.TimePO import *
time_PO = TimePO()
from PO.ListPO import *
List_PO = ListPO()
from PO.ColorPO import *
Color_PO = ColorPO()
from PO.CharPO import *
char_PO = CharPO()

# 1，登录 -  档案质控分析
dataMonitor_PO.login("test", "Qa@123456")
dataMonitor_PO.clickMenu("档案质控分析")

# 2，数据更新截止至时间：2020年07月15日
dataMonitor_PO.updateDate()

# 3，档案质控总体情况 - 查询 - 按档案年份查询 （场景1）
dataMonitor_PO.qcAnalysis_dropDownList1("按档案年份查询")
dataMonitor_PO.qcAnalysis_dropDownList1_opr("2016", "规范建档率提升分析")  # 操作 - 规范建档率提升分析
# 情况1
l_problemList1 = dataMonitor_PO.qcAnalysis_dropDownList1_opr("2016", "详情", "规范性,有效性")   # 勾选规范性和有效性，默认当前页
dataMonitor_PO.qcAnalysis_problem_opr(l_problemList1, "330121193312110346")  # 依据患者身份证点击患者详情，如林佩珍
# # 情况2
# l_problemList1 = dataMonitor_PO.qcAnalysis_dropDownList1_opr("2016", "详情", varPageNum=4)  # 操作 - 详情（问题档案列表），跳转到第四页，默认所有规则
# dataMonitor_PO.qcAnalysis_problem_opr(l_problemList1, "330482198604232419")  # 依据患者身份证点击患者详情，如徐启明
# # 情况3
# l_problemList1 = dataMonitor_PO.qcAnalysis_dropDownList1_opr("2016", "详情", "规范性", 5)  # 勾选规范性，跳转到19页
# dataMonitor_PO.qcAnalysis_problem_opr(l_problemList1, "330682198911251223")  # 依据患者身份证点击患者详情，如金丽娜


# # 3，档案质控总体情况 - 查询 - 全部档案 （场景2）
# dataMonitor_PO.qcAnalysis_dropDownList1("全部档案")
# dataMonitor_PO.qcAnalysis_dropDownList1_opr("2020-07-15", "规范建档率提升分析")  # 操作 - 规范建档率提升分析
# # 情况1
# l_problemList1 = dataMonitor_PO.qcAnalysis_dropDownList1_opr("2016", "详情", "规范性,有效性")   # 勾选规范性和有效性，默认当前页
# dataMonitor_PO.qcAnalysis_problem_opr(l_problemList1, "32210119490127322X")  # 依据患者身份证点击患者详情，如王琦
# # 情况2
# l_problemList1 = dataMonitor_PO.qcAnalysis_dropDownList1_opr("2016", "详情", varPageNum=4)  # 操作 - 详情（问题档案列表），跳转到第四页，默认所有规则
# dataMonitor_PO.qcAnalysis_problem_opr(l_problemList1, "330102196710180029")  # 依据患者身份证点击患者详情，如戴星
# # 情况3
# l_problemList1 = dataMonitor_PO.qcAnalysis_dropDownList1_opr("2016", "详情", "规范性", 5)  # 勾选规范性，跳转到19页
# dataMonitor_PO.qcAnalysis_problem_opr(l_problemList1, "330102730518002")  # 依据患者身份证点击患者详情，如易梅










