# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2020-9-30
# Description: EHR 质量管理系统 (质控结果分析 - 社区)
# chrome版本：94.0.4606.81
# webdriver驱动：https://npm.taobao.org/mirrors/chromedriver
# 本地路径：C:\Python39\Scripts
# *****************************************************************

from instance.zyjk.EHR.PageObject.DataMonitorPO import *
dataMonitor_PO = DataMonitorPO()


# 1，登录
dataMonitor_PO.login("test", "Qa@123456")

# 2，菜单
dataMonitor_PO.clickMenu("质控结果分析", "社区")

# 3.1，检查质控数据截止日期
# 3.1.1，日期不能早于2000.1.5
dataMonitor_PO.checkDate(dataMonitor_PO.getUpdateDate())
print("-" * 50)
# 3.2, 辖区常住人口（人） - 人数、建档率、截止日期
resident, createRate, endDate = dataMonitor_PO.getResident()
print("-" * 50)
# 3.3, 1+1+1签约居民人数（人） - 人数、签约率、签约完成率、签约人数、签约机构与档案管理机构不一致人数
contract, signRate, finishRate, differP = dataMonitor_PO.getContract()
print("-" * 50)
# 3.4, 签约居民分类（重点人群，非重点人群）
emphasis, noEmphasis = dataMonitor_PO.getProgress()


# # 3.5, 家庭医生团队电子健康档案指标 - 详细
dataMonitor_PO.openNewLabel("http://192.168.0.243:8082/#/recordService/list?orgCode=310118001")
l_all = dataMonitor_PO.recordService("签约医生", "社区")  # 获取字段与所有值列表
# print(l_all)
# value = dataMonitor_PO.getRecordServiceValue(l_all, "李*琳", "档案更新率(%)")   # 获取某机构的某个字段值。
# print(value)

l_all = dataMonitor_PO.recordServiceCommunity("签约居民列表")
# print(l_all)
# # value = dataMonitor_PO.getRecordServiceValue(l_all, "李*琳", "建档率(%)")   # 获取某医生的某个字段值。
# # print(value)

