# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2019-12-16
# Description: PIM基层健康管理平台之 门诊配发药
# https://blog.csdn.net/xc_zhou/article/details/82415870 chrome浏览器的options参数
# http://192.168.0.81:8324/login
# *****************************************************************

from instance.zyjk.PIM.PageObject.PimPO import *
Pim_PO = PimPO()

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# # # 前置条件：测试药房给患者进行门诊配发药时，需选择患者，因此需要先创建一个患者挂号、就诊、收费结算流程。
# # 步骤1/4：收费管理员给患者进行挂号操作。
varInputCode = Pim_PO.registration(user_admin, varPatient)  # 返回输入码，如：nkmzpz
#
# # 步骤2/4：医生给患者就诊，开处方
Pim_PO.prescribe(user_doctor, varPatient, varInputCode)
#
# # 步骤3/4：收费管理员给患者收费结算
Pim_PO.charge(user_admin, varPatient)

# # # 步骤4/4：测试药房给患者进行门诊配发药
# Pim_PO.peifayao(user_drugstore)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





# # Pim_PO.modelMenu("医保")
# # Level_PO.clickXpath("//div[@aria-label='医保类型']/div[2]/button[3]/span", 2)  # 医保类型3  ? bug 无法点击文字
# Pim_PO.modelMenu("批量配发药")
# Pim_PO.modelMenu("\ue6f1 配发药")
# Pim_PO.modelMenu("叫号")
# Pim_PO.modelMenu("刷新")
# Pim_PO.modelMenu("挂起")
# # Pim_PO.modelMenu("暂停")  # 点击暂定后，设置和菜单的元素位置发生变化，则无法定位。
# Pim_PO.modelMenu("设置")
# Level_PO.clickXpath("//div[@aria-label='显示列设置']/div[3]/div/div/button[1]", 2)  # 确定
# Pim_PO.modelMenu("菜单")
# Level_PO.clickLinktext("配发药统计", 2)

