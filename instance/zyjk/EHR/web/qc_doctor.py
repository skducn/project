# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2020-9-30
# Description: EHR 质量管理系统 (质控结果分析 - 家庭医生)
# chrome版本：94.0.4606.81
# webdriver驱动：https://npm.taobao.org/mirrors/chromedriver
# 本地路径：C:\Python39\Scripts
# *****************************************************************

from instance.zyjk.EHR.PageObject.DataMonitorPO import *
dataMonitor_PO = DataMonitorPO()


# 1，登录
dataMonitor_PO.login("test", "Qa@123456")

# 2，菜单
dataMonitor_PO.clickMenu("质控结果分析", "家庭医生")

# 3.1，检查质控数据截止日期
# 3.1.1，日期不能早于2000.1.5
dataMonitor_PO.checkDate(dataMonitor_PO.getUpdateDate())
print("-" * 50)
# 3.1.2, 1+1+1签约居民人数（人） 、签约机构与档案管理机构不一致人数
contract, differP = dataMonitor_PO.getContract()

print("-" * 50)
# 3.4, 签约居民分类（重点人群，非重点人群）
emphasis, noEmphasis = dataMonitor_PO.getProgress()

