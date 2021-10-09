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


# 3.5, 家庭医生团队电子健康档案指标 - 详细
dataMonitor_PO.openNewLabel("http://192.168.0.243:8082/#/recordService/list?orgCode=310118001")

l_all = dataMonitor_PO.recordServiceCommunity("签约医生", 6)
print(l_all)

# 检查所有包含%字段的值是否大于100，输出错误的字段与值，如 error, 建档率(%) - ['197.5', '195', '1100']
dataMonitor_PO.testPercentage(l_all)

# 获取某一列的值
l_dagxl = dataMonitor_PO.recordServiceCommunityCol(l_all, "档案更新率(%)")
print(l_dagxl)  # ['90.9', '87.2', '94.7', '91.4', '81.3', '93.5', '71', '83.3', '86.5', '76.7']


l_all = dataMonitor_PO.recordServiceCommunity("签约居民列表", 3)   # 获取 签约居民列表详情页第三页的数据
print(l_all)

# 获取某一列的值
l_dagxl = dataMonitor_PO.recordServiceCommunityCol(l_all, "规范建档占比(%)")
print(l_dagxl)  # ['90.9', '87.2', '94.7', '91.4', '81.3', '93.5', '71', '83.3', '86.5', '76.7']
