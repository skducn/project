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


# 登录
Saas_PO.login("016", "123456")

# # 1，医疗机构注册
# Saas_PO.clickMenuAll("注册管理", "医疗机构注册")
# # 1.1，搜索医院名称（精确搜索）
# varSearchResult = Saas_PO.reg_medicalReg_search("中国保健医院")
# # 1.2，新增医院
# Saas_PO.reg_medicalReg_add(varSearchResult, "中国保健医院", "123456", "令狐冲", "上海市", "市辖区", "浦东新区东方路100号", "张三", "13816109055", "本院专治不孕不育之疑难杂症！")
# # 1.3，编辑医院
# Saas_PO.reg_medicalReg_edit(varSearchResult, "中国保健医院1", "44444", "令狐冲1", "台湾", "连江县", "浦东新区东方路100号1", "张三1", "13016109050", "本院专治不孕不育之疑难杂症！123")
# # 1.4，操作启用/停用
# Saas_PO.reg_medicalReg_opr(varSearchResult, "启用")


# # 2，科室注册
# Saas_PO.clickMenuAll("注册管理", "科室注册")
# # 2.1,搜索医疗机构
# varSearchResult = Saas_PO.reg_officeReg_search("中国保健医院")
# # 2.2,给指定医疗机构添加科室
# Saas_PO.reg_officeReg_add(varSearchResult, "保健科", "介绍明细")
# # 2.3,给指定医疗机构编辑科室? bug
# # Saas_PO.reg_officeReg_edit(varSearchResult, "骨科")


# # 3，医护人员注册
# Saas_PO.clickMenuAll("注册管理", "医护人员注册")
# # 3.1,搜索
# # varSearchResult = Saas_PO.reg_nurseReg_search("董存瑞")
# # 3.2,新增  医院及科室?
# # Saas_PO.reg_nurseReg_add(varSearchResult, "董明珠", r"D:\test.jpg", "13816109088", "护照", "310101198004110014", "女", "1980-04-11", "护士", "中国保健医院", "骨科", "护士长", str(Time_PO.get_day_of_day(1)), "专治不孕不育之疑难杂症")
# # 3.3,用户（编辑）
# # Saas_PO.reg_nurseReg_edit(varSearchResult, "董存瑞", r"D:\test.jpg", "13816109089", "身份证", "310101198004120015", "男", "1980-04-12", "医生", "中国保健医院", "心内科", "主治医生", str(Time_PO.get_day_of_day(2)), "专治脚气疑难杂症")
# # 3.4,账号（编辑）忽略不做
# # 3.5,操作启用/停用
# # Saas_PO.reg_nurseReg_opr(varSearchResult, "启用")


# # # 4，配置维护
# Saas_PO.clickMenuAll("注册管理", "配置维护")
# # 4.1，搜索配置名称并修改当前值
# Saas_PO.reg_Config_opr("启用状态", "启用")
# Saas_PO.reg_Config_opr("行数", "6")
# Saas_PO.reg_Config_opr("是否启用强密码校验", "是")
