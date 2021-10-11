# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2021-10-11
# Description: EHR 质量管理系统 (质控结果分析 - 社区签约居民New)
# chrome版本：94.0.4606.81
# webdriver驱动：https://npm.taobao.org/mirrors/chromedriver
# 本地路径：C:\Python39\Scripts
# *****************************************************************

from instance.zyjk.EHR.PageObject.DataMonitorPO import *
dataMonitor_PO = DataMonitorPO()


# 1，登录
dataMonitor_PO.login("test", "Qa@123456")

# 2，菜单
dataMonitor_PO.clickMenu("质控结果分析", "(社区)签约居民-新")

dataMonitor_PO.getCommunityNew()

# 3.1.1，签约居民中重点人群
# 3.1.2，签约未建档人数
# 3.1.3，老年人，糖尿病，高血压

# 4.1.1，60岁以上签约居民
# 4.1.2, 签约率
# 4.1.3, 签约建档率

# 5.1.1 签约居民中非重点人群
# 5.1.2 签约未建档人数
# 5.1.3 签约率
# 5.1.4 签约建档率
# 5.1.5 规范建档占比
# 5.1.6 更新率
# 5.1.7 利用率