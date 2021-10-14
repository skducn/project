# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-9-30
# Description: EHR 质量管理系统 (质控结果分析 - 家庭医生)
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
dataMonitor_PO.clickMenu("质控结果分析", "家庭医生")

# *****************************************************************
# 检查点
dataMonitor_PO.checkDate(" c1，质控数据截止日期不能早于2000.1.5", dataMonitor_PO.getUpdateDate(), "2020-1-5")

# 1+1+1签约居民人数（人）
# 签约机构与档案管理机构不一致人数
# 签约居民分类 - 重点人群
# 签约居民分类 - 非重点人群
qyjm, byz, focusGroup, noFocusGroup = dataMonitor_PO.getDoctor()

# 检查点
dataMonitor_PO.checkDigitalborder(" c2，1+1+1签约居民人数不能小于等于0", int(qyjm), ">=", 0)
dataMonitor_PO.checkDigitalborder(" c3，签约机构与档案管理机构不一致人数不能小于0", int(byz), ">=", 0)
dataMonitor_PO.checkDigitalborder(" c4，签约居民分类之重点人群比率不能大于100%", int(focusGroup), "<=", 100)
dataMonitor_PO.checkDigitalborder(" c5，签约居民分类之重点人群比率不能小于0%", int(focusGroup), ">=", 0)
dataMonitor_PO.checkDigitalborder(" c6，签约居民分类之非重点人群比率不能大于100%", int(noFocusGroup), "<=", 100)
dataMonitor_PO.checkDigitalborder(" c7，签约居民分类之非重点人群比率不能小于0%", int(focusGroup), ">=", 0)

# *****************************************************************
# 详情 - 签约居民列表
dataMonitor_PO.openNewLabel("http://192.168.0.243:8082/#/recordService/list?docCode=0041&orgCode=310118001&isDoctor=true")
l_all = dataMonitor_PO.recordServiceCommunity("签约居民列表", 3)   # 获取 签约居民列表详情页第三页的数据
