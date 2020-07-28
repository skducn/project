# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2019-12-16
# Description: 电子健康档案数据监控中心（PC端）之 权限管理
# 技巧：去掉字符串两端的数字， astring.strip(string.digits) ,如 123姓名，输出：姓名
# 扩展：astring.lstrip(string.digits) 去掉左侧数字  , astring.rstrip(string.digits) 去掉右侧数字
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


from PO.excelPO import *
excel_PO = ExcelPO()
from instance.zyjk.EHR.PageObject.DataMonitorPO import *
DataMonitor_PO = DataMonitorPO()
from instance.zyjk.EHR.web.login import *
import numpy

# 权限管理
Level_PO.clickXpathsContain("//a", "href", '#/permission', 2)

# print("\n1，遍历权限列表")
# l_tmp = Level_PO.getXpathsText("//tr")
# print(l_tmp[0])  # 输出标题
# x = Level_PO.getXpathsText("//ul[@class='el-pager']/li")
# for i in range(1, int(x[-1])+1):
#     DataMonitor_PO.permission_printList(i)  # 输出


# print("\n2，新增菜单")
DataMonitor_PO.permission_addMenu("auto1", "pad", "pad", "隐藏", "pad", "禁止", "", "110", "1")

# print("\n3，搜索新增的用户")
# DataMonitor_PO.user_searchUser("用户名", "auto1")
# DataMonitor_PO.user_searchUser("昵称", "令狐冲1")
# DataMonitor_PO.user_searchUser("手机号", "13816109050")
#
# print("\n3，搜索用户名，操作第一条记录的角色")
# DataMonitor_PO.user_operateRole("用户名", "auto1", "院长", "诊前", "预检")
#
# print("\n4，搜索用户名，操作第一条记录的编辑")
# DataMonitor_PO.user_operateEdit("用户名", "auto1", "auto2", "令狐冲2", "13636371320", "建档专员", "否", "安亭镇黄渡社区卫生服务中心")

# print("\n5，搜索用户，操作第一条记录的删除")
# DataMonitor_PO.user_operateDel("用户名", "auto2")

