# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2020-8-11
# Description: SAAS 之 注册管理
# *****************************************************************

from instance.zyjk.SAAS.PageObject.SaasPO import *
Saas_PO = SaasPO()
from PO.TimePO import *
time_PO = TimePO()
from PO.ListPO import *
List_PO = ListPO()
from PO.ColorPO import *
Color_PO = ColorPO()

# 1，登录
Saas_PO.login("016", "123456")

# # 2，选择菜单
# Saas_PO.clickMenuAll("注册管理", "医疗机构注册")
# # 2.1，搜索医院名称（精确搜索）
# varSearchResult = Saas_PO.reg_medicalReg_search("中国保健医院")
# # 2.2，新增医院
# Saas_PO.reg_medicalReg_add(varSearchResult, "中国保健医院", "123456", "令狐冲", "上海市", "市辖区", "浦东新区东方路100号", "张三", "13816109055", "本院专治不孕不育之疑难杂症！")
# # 2.3，编辑医院
# Saas_PO.reg_medicalReg_edit(varSearchResult, "中国保健医院1", "44444", "令狐冲1", "台湾", "连江县", "浦东新区东方路100号1", "张三1", "13016109050", "本院专治不孕不育之疑难杂症！123")
# # 2.4，操作启用/停用
# Saas_PO.reg_medicalReg_opr(varSearchResult, "启用")


# # 3，选择菜单
# Saas_PO.clickMenuAll("注册管理", "科室注册")
# # 3.1,搜索医疗机构
# varSearchResult = Saas_PO.reg_officeReg_search("中国保健医院")
# # # 3.2,给指定医疗机构添加科室
# Saas_PO.reg_officeReg_add(varSearchResult, "保健科", "介绍明细")
# # # 3.3,给指定医疗机构编辑科室? bug
# # Saas_PO.reg_officeReg_edit(varSearchResult, "骨科")


# 4，选择菜单
Saas_PO.clickMenuAll("注册管理", "医护人员注册")
# 4.1,搜索
varSearchResult = Saas_PO.reg_nurseReg_search("董明珠")
# 4.2,新增  ?  头像? 九至医院及科室?
Saas_PO.reg_nurseReg_add(varSearchResult, "董明珠", "test.jpg", "13816109088", "310101198004110014", "1980-04-11", "2020-08-09", "专治不孕不育之疑难杂症")


# 4.3,操作用户
# 4.4,操作账号
# 4.5,操作启用/停用