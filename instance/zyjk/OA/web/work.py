# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2019-5-7
# Description: OA - 常用工作
# ff 66.0.4 (64 位) , selenium =3.141.0，gecko = 0.24.0
# geckodriver下载：https://github.com/mozilla/geckodriver/releases
# selenium更新： pip3 install -U selenium
#***************************************************************

import os, sys
# sys.path.append("../../../../")
from instance.zyjk.OA.PageObject.OaPO import *
Oa_PO = OaPO()
List_PO = ListPO()
Time_PO = TimePO()
Net_PO = NetPO()
Data_PO = DataPO()
File_PO = FilePO()
Excel_PO = ExcelPO()





# # 申请者登录OA
# Oa_PO.open()
# Oa_PO.login("jinhao")
#
# # 点击菜单选模块
# Oa_PO.memu("工作流", "新建工作")
#
# # 检查 常用工作中表单数量，应该3个。
# Oa_PO.Web_PO.iframeXpath("//iframe[@src='/general/workflow/new/']", 2)
# Oa_PO.getWorkQty()
#
# # 请假申请单
# Oa_PO.Web_PO.clickXpathsContain("//button", "onclick", "请假申请", 2)
# # Oa_PO.Web_PO.iframeQuit(2)
# # Oa_PO.Web_PO.iframeId("tabs_w10000_iframe", 2)
# # Oa_PO.Web_PO.iframeId("work_form_data", 2)
# # Oa_PO.Web_PO.clickXpathsNum("//input[@type='radio']",3, 2)  # 公休
# # Oa_PO.Web_PO.jsIdReadonly("DATA_4", 2)
# # Oa_PO.Web_PO.inputXpath("//input[@name='DATA_4']", "2020-06-04 09:43:40")
# # Oa_PO.Web_PO.jsIdReadonly("DATA_5", 2)
# # Oa_PO.Web_PO.inputXpath("//input[@name='DATA_5']", "2020-06-05 09:43:40")
# # Oa_PO.Web_PO.inputXpath("//input[@name='DATA_67']", "2")
# # Oa_PO.Web_PO.inputXpath("//textarea[@name='DATA_7']", "请假休息")
# # Oa_PO.Web_PO.inputXpath("//textarea[@name='DATA_44']", "已交接")
# # Oa_PO.Web_PO.iframeSwitch(1)
# # Oa_PO.Web_PO.clickXpath("//input[@id='onekey_next']", 2)  # 提交
# # Oa_PO.Web_PO.alertAccept()
# Oa_PO.Web_PO.iframeQuit(2)
# Oa_PO.Web_PO.quitURL()


# -----------------------------------------------------------------------------

# # 审核员登录OA - 部门领导
# Oa_PO.open()
# Oa_PO.login("wanglei01")
#
# # 点击菜单选模块
# Oa_PO.memu("工作流", "我的工作")
# Oa_PO.Web_PO.iframeXpath("//iframe[@src='/general/workflow/list/']", 2)  # 第一层
#
# Oa_PO.Web_PO.iframeId("workflow-data-list", 2)  # 第二层
# Oa_PO.Web_PO.clickXpaths("//table[@id='gridTable']/tbody/tr[2]/td[8]/a", 2)  # 选择最近一条未审核记录
# Oa_PO.Web_PO.iframeSwitch(2)
# Oa_PO.Web_PO.iframeId("workflow-form-frame", 2)  # 第二层
# Oa_PO.Web_PO.iframeId("work_form_data", 2)  # 第三层
# Oa_PO.Web_PO.clickXpath("//input[@name='DATA_11' and @value='同意']", 2)  # 同意
# Oa_PO.Web_PO.clickXpath("//input[@name='DATA_11' and @value='不同意']", 2)  # 不同意
# Oa_PO.Web_PO.inputXpath("//textarea[@name='DATA_12']", "ok批准")
# Oa_PO.Web_PO.iframeSwitch(1)
# Oa_PO.Web_PO.clickXpath("//input[@id='onekey_next']", 2)  # 提交
# Oa_PO.Web_PO.alertAccept()
# Oa_PO.Web_PO.iframeQuit(2)
# Oa_PO.Web_PO.quitURL()


# -----------------------------------------------------------------------------

# # 审核员登录OA - 人事总监
# Oa_PO.open()
# Oa_PO.login("yanlibei")
#
# # 点击菜单选模块
# Oa_PO.memu("工作流", "我的工作")
# Oa_PO.Web_PO.iframeXpath("//iframe[@src='/general/workflow/list/']", 2)  # 第一层
#
# Oa_PO.Web_PO.iframeId("workflow-data-list", 2)  # 第二层
# Oa_PO.Web_PO.clickXpaths("//table[@id='gridTable']/tbody/tr[2]/td[8]/a", 2)  # 选择最近一条未审核记录
# Oa_PO.Web_PO.iframeSwitch(2)
# Oa_PO.Web_PO.iframeId("workflow-form-frame", 2)  # 第二层
# Oa_PO.Web_PO.iframeId("work_form_data", 2)  # 第三层
# Oa_PO.Web_PO.clickXpath("//input[@name='DATA_14' and @value='同意']", 2)  # 同意
# # Oa_PO.Web_PO.clickXpath("//input[@name='DATA_14' and @value='不同意']", 2)  # 不同意
# Oa_PO.Web_PO.inputXpath("//textarea[@name='DATA_15']", "ok批准,谢谢")
# Oa_PO.Web_PO.iframeSwitch(1)
# Oa_PO.Web_PO.clickXpath("//input[@id='onekey_next']", 2)  # 提交
# Oa_PO.Web_PO.alertAccept()
# Oa_PO.Web_PO.iframeQuit(2)
# Oa_PO.Web_PO.quitURL()

# -----------------------------------------------------------------------------
#
# # 审核员登录OA - 副总
# Oa_PO.open()
# Oa_PO.login("wanglei01")
#
# # 点击菜单选模块
# Oa_PO.memu("工作流", "我的工作")
# Oa_PO.Web_PO.iframeXpath("//iframe[@src='/general/workflow/list/']", 2)  # 第一层
#
# Oa_PO.Web_PO.iframeId("workflow-data-list", 2)  # 第二层
# Oa_PO.Web_PO.clickXpaths("//table[@id='gridTable']/tbody/tr[2]/td[8]/a", 2)  # 选择最近一条未审核记录
# Oa_PO.Web_PO.iframeSwitch(2)
# Oa_PO.Web_PO.iframeId("workflow-form-frame", 2)  # 第二层
# Oa_PO.Web_PO.iframeId("work_form_data", 2)  # 第三层  , 进入表单
# Oa_PO.Web_PO.clickXpath("//input[@name='DATA_21' and @value='同意']", 2)  # 同意
# # Oa_PO.Web_PO.clickXpath("//input[@name='DATA_21' and @value='不同意']", 2)  # 不同意
# Oa_PO.Web_PO.inputXpath("//textarea[@name='DATA_18']", "ok批准,谢谢")
# Oa_PO.Web_PO.iframeSwitch(1)
# Oa_PO.Web_PO.clickXpath("//input[@id='handle_end']", 2)  # 提交
# Oa_PO.Web_PO.alertAccept()
# Oa_PO.Web_PO.iframeQuit(2)
# Oa_PO.Web_PO.quitURL()

# -----------------------------------------------------------------------------

# 申请人登录OA - 回执确认
Oa_PO.open()
Oa_PO.login("jinhao")

# 点击菜单选模块
Oa_PO.memu("工作流", "我的工作")
Oa_PO.Web_PO.iframeXpath("//iframe[@src='/general/workflow/list/']", 2)  # 第一层
Oa_PO.Web_PO.clickLinktext("办结工作", 2)
Oa_PO.Web_PO.iframeId("workflow-data-list", 2)  # 第二层
Oa_PO.Web_PO.clickXpaths("//table[@id='gridTable']/tbody/tr[2]/td[9]/a", 2)  # 选择最近一条审核通过的记录
Oa_PO.Web_PO.iframeQuit(2)

# 前后都表达打印（弹出窗口）
all_handles = Oa_PO.Web_PO.driver.window_handles
Oa_PO.Web_PO.driver.switch_to.window(all_handles[1])
x = Oa_PO.Web_PO.getXpathsText("//td")
# print(x[0])
number = str(x[0]).split("表单")[0]
print(number.strip(" "))  # 流水号：5597

Oa_PO.Web_PO.iframeId("print_frm", 2)
list2 = Oa_PO.Web_PO.getXpathsText("//td")
# print(list2)

print(List_PO.getSectionList(List_PO.getSectionList(list2, '审核信息', 'delbefore'), "流程开始（" + number.strip(" ") + "）", 'delafter'))
# ['副总审批：同意 不同意 ', 'ok批准', '王磊 2020-06-04 16:36:07', '人事总监审批：同意 不同意 ', 'ok批准,谢谢', '严丽蓓 2020-06-04 16:42:53', '副总审批：同意 不同意 ', 'ok批准,谢谢', '王磊 2020-06-04 16:47:40', '总经理审批：同意 不同意 ', '', '']


# 获取某个字段是否存在
print(Oa_PO.Web_PO.isElementXpath("//input[@name='DATA_11' and @value='同意' and @checked]"))
print(Oa_PO.Web_PO.isElementXpath("//input[@name='DATA_11' and @value='不同意' and @checked]"))

print(Oa_PO.Web_PO.isElementXpath("//input[@name='DATA_14' and @value='同意' and @checked]"))
print(Oa_PO.Web_PO.isElementXpath("//input[@name='DATA_14' and @value='不同意' and @checked]"))

print(Oa_PO.Web_PO.isElementXpath("//input[@name='DATA_21' and @value='同意' and @checked]"))
print(Oa_PO.Web_PO.isElementXpath("//input[@name='DATA_21' and @value='不同意' and @checked]"))

print(Oa_PO.Web_PO.isElementXpath("//input[@name='DATA_68' and @value='同意' and @checked]"))
print(Oa_PO.Web_PO.isElementXpath("//input[@name='DATA_68' and @value='不同意' and @checked]"))