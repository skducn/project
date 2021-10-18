# coding=utf-8
# *****************************************************************#
# Author     : John
# Created on : 2021-10-15
# Description: EHR质量管理系统（系统管理 - 日志查询）
# 后台地址: http://192.168.0.243:8082/#/system/user
# 超级管理员: admin/admin@123456
# *****************************************************************
from instance.zyjk.EHR.PageObject.DataMonitorPO import *
dataMonitor_PO = DataMonitorPO()

# *****************************************************************
# 1，登录
dataMonitor_PO.login("admin", "admin@123456")  # 超级管理员

# 2，用户管理
dataMonitor_PO.clickMenu("系统管理", "日志查询")

# # 3，显示角色列表
# dataMonitor_PO.sys_logList()

# 4，搜索（账号，记录类型，开始日期，结束日期）
dataMonitor_PO.sys_log_search("xyzeng")
dataMonitor_PO.sys_log_search("", "查看档案查阅人员列表界面")
dataMonitor_PO.sys_log_search("", "", "2021-10-12")
dataMonitor_PO.sys_log_search("", "", "2021-10-15")
dataMonitor_PO.sys_log_search("", "", "2021-10-01", "2021-10-16")




