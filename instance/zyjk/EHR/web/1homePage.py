# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2020-7-23
# Description: 电子健康档案数据监控中心（PC端）之 首页
# https://blog.csdn.net/xc_zhou/article/details/82415870 chrome浏览器的options参数
# https://npm.taobao.org/mirrors/chromedriver  chrome驱动 , C:\Python38\Scripts\chromedrive.exe
# *****************************************************************






from instance.zyjk.EHR.PageObject.DataMonitorPO import *
dataMonitor_PO = DataMonitorPO()


# 1，登录
dataMonitor_PO.login("test", "Qa@123456")

# 2，菜单
dataMonitor_PO.clickMenu("质控结果分析", "区级")

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
print("-" * 50)

# 3.5, 各社区签约居民电子健康档案指标 - 详细
dataMonitor_PO.openNewLabel("http://192.168.0.243:8082/#/recordService/list?docCode=0041&orgCode=310118001&isDistrict=true")
l_all = dataMonitor_PO.recordService("医疗机构名称")  # 获取字段与所有值列表
print(l_all)
value = dataMonitor_PO.getRecordServiceValue(l_all, "上海市青浦区练塘镇社区卫生服务中心", "档案更新率(%)")   # 获取某机构的某个字段值。
print(value)
print("-" * 50)

l_all = dataMonitor_PO.recordService("签约医生")
print(l_all)
value = dataMonitor_PO.getRecordServiceValue(l_all, "李*琳", "建档率(%)")   # 获取某医生的某个字段值。
print(value)











# # 3，首页 - 总体指标分布
# dataMonitor_PO.homePage_indicator()
#
# # 4，首页 - 电子健康档案分布图
# dataMonitor_PO.homePage_EhrMap()
#
# # 5，首页 - 签约医生分布
# dataMonitor_PO.homePage_signDoctor()
#
# # 6，首页 - 年龄
# dataMonitor_PO.homePage_age()
#
# # 7，首页 - 疾病分布
# dataMonitor_PO.homePage_disease()
#
# # 8，首页 - 特殊人群分布
# dataMonitor_PO.homePage_specialPeople()



