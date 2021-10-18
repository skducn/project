# coding=utf-8
# *****************************************************************#
# Author     : John
# Created on : 2021-10-15
# Description: EHR质量管理系统（系统管理 - 权限管理）
# 后台地址: http://192.168.0.243:8082/#/system/user
# 超级管理员: admin/admin@123456
# *****************************************************************
from instance.zyjk.EHR.PageObject.DataMonitorPO import *
dataMonitor_PO = DataMonitorPO()

# *****************************************************************
# 1，登录
dataMonitor_PO.login("admin", "admin@123456")  # 超级管理员

# 2，用户管理
dataMonitor_PO.clickMenu("系统管理", "权限管理")

# 3，搜索(菜单名称、权限值、路径、模块、位置排序)
dataMonitor_PO.sys_power_search("菜单名称", "居民")
dataMonitor_PO.sys_power_search("权限值", "newContractEcharts")
dataMonitor_PO.sys_power_search("路径", "recordService")
dataMonitor_PO.sys_power_search("模块", "crowdClassift")
dataMonitor_PO.sys_power_search("位置排序", "30")  # 未开发

# 4，新增菜单（菜单名称，权限值，路径，是否显示，模块，状态，是否缓存，图标，位置排序，所属上级，菜单ID，类型，所属系统）
# 条件：先搜索菜单名称是否存在，不存在则增加
# 是否显示：[展示，隐藏]
# 状态：[正常，异常]
# 是否缓存：['不缓存', '缓存']
# dataMonitor_PO.sys_power_add("test55", "recordServiceCrowdClassift", "recordServiceCrowdClassift", "隐藏", "recordServiceCrowdClassift", "禁止", "不缓存", "", "12", "1", "2", "")

# 5，编辑记录（旧菜单名称，新菜单名称，权限值，路径，是否显示，模块，状态，是否缓存，图标，位置排序，所属上级，菜单ID，类型，所属系统）
# dataMonitor_PO.sys_power_edit("test55", "linghuchong", "recordSer", "assift", "展示", "CrowdClassift", "正常", "不缓存", "", "88", "100", "200", "11223344")

# 6，删除记录（删除前先搜索菜单名称）
dataMonitor_PO.sys_power_del("test")

