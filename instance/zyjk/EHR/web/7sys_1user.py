# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-3-2
# Description: 电子健康档案数据监控中心（PC端）之 系统管理 - 用户管理
# 技巧：去掉字符串两端的数字， astring.strip(string.digits) ,如 123姓名，输出：姓名
# 扩展：astring.lstrip(string.digits) 去掉左侧数字  , astring.rstrip(string.digits) 去掉右侧数字
# C4 ？开发bug，编辑后会刷新页面导致提示2次（成功及无数据），用户体验不好，自动化会报错，找不到数据。
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


from instance.zyjk.EHR.PageObject.DataMonitorPO import *
dataMonitor_PO = DataMonitorPO()
from PO.TimePO import *
time_PO = TimePO()
from PO.ListPO import *
List_PO = ListPO()
from PO.ColorPO import *
Color_PO = ColorPO()
from PO.StrPO import *
Str_PO = StrPO()

varNewUser = "auto1"
varNewNickName = "令狐冲1"
varNewPhone = "13816109050"

# 1，登录 -
dataMonitor_PO.login("test", "Qa@123456")
dataMonitor_PO.clickMenu("系统管理", "用户管理")

# 2，显示用户列表
dataMonitor_PO.sys_userList()

# 3，用户管理 - 新增
# dataMonitor_PO.sys_user_add(l_userList2, "linghuchong1", "令狐冲", "13816109050", "护士")

# # 4，用户管理 - 搜索
dataMonitor_PO.sys_user_search("用户名", "alibaba122")  # 依据用户名搜索
# # dataMonitor_PO.sys_user_search("昵称", "令狐冲")  # 依据昵称搜索
# # dataMonitor_PO.sys_user_search("手机", "13816109050")  # 依据收集搜索
#
# # 5，用户管理 - 编辑
# # dataMonitor_PO.sys_user_edit("alibaba1", "阿里巴巴", "13613254658", "院长")
dataMonitor_PO.sys_user_edit("ayida1", "ayida", "阿依达", "13613250400", "家庭医生")

# 6，用户管理 - 角色(单选/多选)
dataMonitor_PO.sys_user_role("ayida", "社区机构管理员", "安全审计员", "家庭医生")

# 7，用户管理 - 删除（除了admin其他账号无权限）
# dataMonitor_PO.sys_user_del("alibaba1")

#
# varStatus = DataMonitor_PO.user_searchUser("*", "")
# print(varStatus)
#
# varStatus = DataMonitor_PO.user_searchUser("用户名", "shu")
# print(varStatus)
#
# varStatus = DataMonitor_PO.user_searchUser("昵称", "张")
# print(varStatus)
#
# varStatus = DataMonitor_PO.user_searchUser("手机", "13828333232")
# print(varStatus)



#
# # 遍历用户列表
# DataMonitor_PO.user_printList2()

# print("\nC2，分别搜用户名、昵称、手机")
# DataMonitor_PO.user_searchUser("用户名", varNewUser)
# DataMonitor_PO.user_searchUser("昵称", varNewNickName)
# DataMonitor_PO.user_searchUser("手机", varNewPhone)

# print("\nC3，搜索用户名，操作角色，勾选3个角色")
# # 角色：超级管理员，社区机构管理员，家庭医生，ai核对管理员，档案查看管理员
# DataMonitor_PO.user_operateRole(varNewUser, "社区机构管理员", "ai核对管理员", "档案查看管理员")
#
# # ？开发bug，编辑后会刷新页面导致提示2次（成功及无数据），用户体验不好，自动化会报错，找不到数据。
# print("\nC4，搜索用户名，操作编辑")
# DataMonitor_PO.user_operateEdit(varNewUser, "auto2", "令狐冲2", "13636371320", "护士", "安亭镇黄渡社区卫生服务中心")
#
# print("\nC5，搜索用户，操作删除")
# DataMonitor_PO.user_operateDel("auto2")

