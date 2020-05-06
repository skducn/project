# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2019-12-9
# Description: 电子健康档案数据监控中心（PC端）之 登录
# https://blog.csdn.net/xc_zhou/article/details/82415870 chrome浏览器的options参数
# https://npm.taobao.org/mirrors/chromedriver  chrome驱动 , C:\Python38\Scripts\chromedrive.exe
# *****************************************************************

from instance.zyjk.EHR.PageObject.DataMonitorPO import *
DataMonitor_PO = DataMonitorPO()
from PO.TimePO import *
time_PO = TimePO()


DataMonitor_PO.login("admin", "admin@123456")



