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

# 3，显示角色列表
# dataMonitor_PO.sys_roleList()

# 4，搜索(名称、标题、描述)
# dataMonitor_PO.sys_role_search("名称", "guize")
# dataMonitor_PO.sys_role_search("标题", "区级管理员")
dataMonitor_PO.sys_role_search("描述", "勾选此模块，显示数据测评质量分析模块功能")

# 5，删除名称（删除前先搜索名称） - 谨慎，谨慎，谨慎
# dataMonitor_PO.sys_role_del("t")

# 6，新增名称（名称，标题，描述，排序）
# 条件：先搜索名称是否存在，不存在则添加
# dataMonitor_PO.sys_role_add("linghuchong", "我是令狐冲", "测试功能", "123")

# 7，编辑名称（旧名称，名称，标题，描述，排序）
# dataMonitor_PO.sys_role_edit("baidu", "tianmao", "我是百度", "性能功能", "777")

# 8，编辑名称权限(可多选)
# 权限：['循环质量测评分析', '质控分析报告详情', '质控分析报告（社区）', '质控结果分析', '指标强度管理', '质控规则管理', '数据质量测评分析', '系统管理', '首页']
# dataMonitor_PO.sys_role_power("tianmao", "首页", "系统管理", "质控结果分析")    # 只有主权限
# dataMonitor_PO.sys_role_power("tianmao", "首页", ["质控结果分析", "问题编辑", "家庭医生"], "系统管理")   # 有主权限和子权限
# dataMonitor_PO.sys_role_power("tianmao")  # 清空所有角色
# dataMonitor_PO.sys_role_power("tianmao", ["质控规则管理", "个人基本信息表规则", "糖尿病随访表规则", "档案封面规则"])   # 有主权限和子权限




