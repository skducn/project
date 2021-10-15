# coding=utf-8
# *****************************************************************#
# Author     : John
# Created on : 2021-10-15
# Description: EHR质量管理系统（系统管理 - 角色管理）
# 后台地址: http://192.168.0.243:8082/#/system/user
# 超级管理员: admin/admin@123456
# *****************************************************************
from instance.zyjk.EHR.PageObject.DataMonitorPO import *
dataMonitor_PO = DataMonitorPO()

# *****************************************************************
# 1，登录
dataMonitor_PO.login("admin", "admin@123456")  # 超级管理员

# 2，用户管理
dataMonitor_PO.clickMenu("系统管理", "角色管理")

# # 3，显示用户列表
# dataMonitor_PO.sys_roleList()

# 4，搜索(名称、标题、描述)
# dataMonitor_PO.sys_role_search("名称", "guize")
# dataMonitor_PO.sys_role_search("标题", "区级管理员")
# dataMonitor_PO.sys_role_search("描述", "勾选此模块，显示数据测评质量分析模块功能")

# 5，删除名称（删除前先搜索名称）?
# dataMonitor_PO.sys_role_del("linghuchong")


# 6，新增名称（名称，标题，描述，排序）
# 条件：先搜索名称是否存在，不存在则添加
# dataMonitor_PO.sys_role_add("linghuchong", "我是令狐冲", "测试功能", "123")

# 7，编辑名称（旧名称，名称，标题，描述，排序）
dataMonitor_PO.sys_role_edit("baidu", "tianmao", "我是百度", "性能功能", "777")


# 8，编辑名称权限(可多选)？
# 角色：['社区管理员', '家庭医生', '区级管理员', '规则和指标强度管理', '系统管理模块权限', '数据评测质量分析','test']
# dataMonitor_PO.sys_user_role("linghuchong1", "区级管理员", "系统管理模块权限", "test")
# dataMonitor_PO.sys_user_role("linghuchong1")  # 清空所有角色



