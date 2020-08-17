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
from PO.TimePO import *
time_PO = TimePO()
from PO.ListPO import *
List_PO = ListPO()
from PO.ColorPO import *
Color_PO = ColorPO()

# 1，登录 -  首页
dataMonitor_PO.login("test", "Qa@123456")
dataMonitor_PO.clickMenu("首页")

# 2，数据更新截止至时间：2020年07月15日
dataMonitor_PO.updateDate()

# 3，首页 - 总体指标分布
dataMonitor_PO.homePage_indicator()

# 4，首页 - 电子健康档案分布图
dataMonitor_PO.homePage_EhrMap()

# 5，首页 - 签约医生分布
dataMonitor_PO.homePage_signDoctor()

# 6，首页 - 年龄
dataMonitor_PO.homePage_age()

# 7，首页 - 疾病分布
dataMonitor_PO.homePage_disease()

# 8，首页 - 特殊人群分布
dataMonitor_PO.homePage_specialPeople()



