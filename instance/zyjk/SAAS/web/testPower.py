# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2020-8-13
# Description: SAAS 之 权限管理
# *****************************************************************

from instance.zyjk.SAAS.PageObject.SaasPO import *
Saas_PO = SaasPO()
from PO.TimePO import *
time_PO = TimePO()
from PO.ListPO import *
List_PO = ListPO()
from PO.ColorPO import *
Color_PO = ColorPO()


# 登录
Saas_PO.login("016", "123456")

# # 1，角色管理
Saas_PO.clickMenuAll("权限管理", "角色管理")
# # 1.1，新增角色
# Saas_PO.power_role_add("管理1")
# # 1.2，编辑角色名
# Saas_PO.power_role_editName("管理1", "管理123")
# # 1.3，删除角色
# Saas_PO.power_role_del("管理123")
# # 1.4，编辑角色的菜单，勾选 ["科室注册", "标准代码", "项目管理"]
Saas_PO.power_role_editMenu("内科医生123", ["科室注册", "标准代码", "项目管理"])
