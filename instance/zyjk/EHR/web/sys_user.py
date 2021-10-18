# coding=utf-8
# *****************************************************************#
# Author     : John
# Created on : 2021-10-15
# Description: EHR质量管理系统（系统管理 - 用户管理）
# 后台地址: http://192.168.0.243:8082/#/system/user
# 超级管理员: admin/admin@123456
# *****************************************************************
from instance.zyjk.EHR.PageObject.DataMonitorPO import *
dataMonitor_PO = DataMonitorPO()

# *****************************************************************
# 1，登录
dataMonitor_PO.login("admin", "admin@123456")  # 超级管理员

# 2，用户管理
dataMonitor_PO.clickMenu("系统管理", "用户管理")

# 3，显示用户列表
dataMonitor_PO.sys_userList()

# 4，搜索(用户名、昵称、手机)
dataMonitor_PO.sys_user_search("用户名", "lh")
# dataMonitor_PO.sys_user_search("用户名", "lh")
# dataMonitor_PO.sys_user_search("手机", "13816109050")

# 5，删除用户（删除前先搜索用户）
dataMonitor_PO.sys_user_del("linghuchong1")
# dataMonitor_PO.sys_user_del("lh")

# 6，新增用户（用户名，昵称，手机，第三方用户编码，用户属性，所属社区）
# 条件：先搜索用户名是否存在，不存在则添加
# 用户属性：['家庭医生', '家庭医生助理', '院长', '护士']
# 所属社区： ['上海市青浦区夏阳街道社区卫生服务中心', '上海市青浦区盈浦街道社区卫生服务中心', '上海市青浦区香花桥街道社区卫生服务中心', '上海市青浦区朱家角镇社区卫生服务中心', '上海市青浦区练塘镇社区卫生服务中心', '上海市青浦区金泽镇社区卫生服务中心', '上海市青浦区赵巷镇社区卫生服务中心', '上海市青浦区徐泾镇社区卫生服务中心', '上海市青浦区华新镇社区卫生服务中心', '上海市青浦区重固镇社区卫生服务中心']
# dataMonitor_PO.sys_user_add("lh", "令狐冲", "13816109050", "123123", "家庭医生助理", "上海市青浦区金泽镇社区卫生服务中心")
# dataMonitor_PO.sys_user_add("linghuchong12", "令狐冲", "13816109050", "123123", "护士", "上海市青浦区朱家角镇社区卫生服务中心")

# 7，编辑用户（旧用户名，新用户名，新昵称，新手机，新第三方用户编码，新用户属性，新所属社区）
dataMonitor_PO.sys_user_edit("linghuchong100", "linghuchong1", "提提2", "13012345679", "2121277777", "院长", "上海市青浦区金泽镇社区卫生服务中心")

# 8，编辑用户角色(可多选)
# 角色：['社区管理员', '家庭医生', '区级管理员', '规则和指标强度管理', '系统管理模块权限', '数据评测质量分析','test']
dataMonitor_PO.sys_user_role("linghuchong1", "区级管理员", "系统管理模块权限", "test")
# dataMonitor_PO.sys_user_role("linghuchong1")  # 清空所有角色



