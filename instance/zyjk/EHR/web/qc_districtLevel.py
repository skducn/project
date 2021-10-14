# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2020-9-30
# Description: EHR 质量管理系统 (质控结果分析 - 区级)
# chrome版本：94.0.4606.81
# webdriver驱动：https://npm.taobao.org/mirrors/chromedriver
# 本地路径：C:\Python39\Scripts
# *****************************************************************

from instance.zyjk.EHR.PageObject.DataMonitorPO import *
dataMonitor_PO = DataMonitorPO()

# *****************************************************************
# 登录
dataMonitor_PO.login("test", "Qa@123456")

# 菜单
dataMonitor_PO.clickMenu("质控结果分析", "区级")

# *****************************************************************
# 检查点
dataMonitor_PO.checkDate(" c1，质控数据截止日期不能早于2000.1.5", dataMonitor_PO.getUpdateDate(), "2020-1-5")


# 辖区常住人口（人） - 人数、建档率、截止日期
# 1+1+1签约居民人数（人） - 人数、签约率、签约完成率、签约人数、签约机构与档案管理机构不一致人数
# 签约居民分类（重点人群，非重点人群）
czrk, jdl, jzrq, qyjm, qyl, qywcl, byz, focusGroup, noFocusGroup = dataMonitor_PO.getDistrictLevel()


# 检查点
# 注意：签约完成率可大于100%
dataMonitor_PO.checkDigitalborder(" c2，辖区常住人口不能小于0", int(czrk), ">", 0)
dataMonitor_PO.checkDigitalborder(" c3，建档率不能大于100", int(jdl), "<=", 100)
dataMonitor_PO.checkDigitalborder(" c4，建档率不能小于0", int(jdl), ">=", 0)
dataMonitor_PO.checkDigitalborder(" c5，签约率不能大于100", int(qyl), "<=", 100)
dataMonitor_PO.checkDigitalborder(" c6，签约率不能小于0", int(qyl), ">=", 0)
dataMonitor_PO.checkDigitalborder(" c7，签约完成率不能小于0", int(qywcl), ">=", 0)
dataMonitor_PO.checkDigitalborder(" c8，签约机构与档案管理机构不一致人数不能小于0", int(byz), ">=", 0)
dataMonitor_PO.checkDigitalborder(" c9，签约居民分类之重点人群比率不能大于100%", int(focusGroup), "<=", 100)
dataMonitor_PO.checkDigitalborder(" c10，签约居民分类之重点人群比率不能小于0%", int(focusGroup), ">=", 0)
dataMonitor_PO.checkDigitalborder(" c11，签约居民分类之非重点人群比率不能大于100%", int(noFocusGroup), "<=", 100)
dataMonitor_PO.checkDigitalborder(" c12，签约居民分类之非重点人群比率不能小于0%", int(focusGroup), ">=", 0)


# *****************************************************************
# 各社区签约居民电子健康档案指标 - 详细
dataMonitor_PO.openNewLabel("http://192.168.0.243:8082/#/recordService/list?docCode=0041&orgCode=310118001&isDistrict=true")
l_all = dataMonitor_PO.recordService("医疗机构名称")  # 获取字段与所有值列表
# print(l_all)
# value = dataMonitor_PO.getRecordServiceValue(l_all, "上海市青浦区练塘镇社区卫生服务中心", "档案更新率(%)")   # 获取某机构的某个字段值。
# print(value)

l_all = dataMonitor_PO.recordService("签约医生", 4)
# print(l_all)
# value = dataMonitor_PO.getRecordServiceValue(l_all, "黄*美", "建档率(%)")   # 获取某医生的某个字段值。
# print(value)





