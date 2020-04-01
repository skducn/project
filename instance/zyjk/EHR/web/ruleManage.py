# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2019-12-12
# Description: 电子健康档案数据监控中心（PC端）之 规则管理
# 技巧：去掉字符串两端的数字， astring.strip(string.digits) ,如 123姓名，输出：姓名
# 扩展：astring.lstrip(string.digits) 去掉左侧数字  , astring.rstrip(string.digits) 去掉右侧数字
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# priceList = ['\n\t\t\t\t\t\t\t\tCHF\xa0\r\n        \r\n    \t64.90',
#              '\n\t\t\t\t\t\t\t\tCHF\xa0\r\n        \r\n    \t58.40',
#              '\n\t\t\t\t\t\t\t\tCHF\xa0\r\n        \r\n    \t48.70']
#
# print([' '.join([i.strip() for i in price.strip().split('\t')]) for price in priceList])
#
# x = ['编号 规则名称', '1\n既往史精神与门诊就诊记录逻辑错误', '2\n既往史肝炎与门诊就诊记录逻辑错误', '3\n既往史结核与门诊就诊记录逻辑错误', '4\n既往史脑卒与门诊就诊记录逻辑错误', '5\n既往肿瘤与门诊就诊记录逻辑错误', '6\n既往史冠心病与门诊就诊记录逻辑错误', '7\n既往史肺病与门诊就诊记录逻辑错误', '8\n既往史疾病糖尿病与门诊就诊记录逻辑错误', '9\n既往史疾病高血压与门诊就诊记录逻辑错误', '10\n家族史亲属关系填写错误', '操作', '编辑停用', '编辑停用', '编辑停用', '编辑停用', '编辑停用', '编辑停用', '编辑停用', '编辑停用', '编辑停用', '编辑停用']
# a = [''.join([i.strip() for i in price.strip()]) for price in x]
# b = [''.join([i.strip() for i in price.strip().replace("\n",", ")]) for price in x]
# print(a)
# print(b)




from PO.excelPO import *
excel_PO = ExcelPO()
from instance.zyjk.EHR.PageObject.DataMonitorPO import *
DataMonitor_PO = DataMonitorPO()
from instance.zyjk.EHR.web.login import *
import numpy

# 规则管理
Level_PO.clickXpathsContain("//a", "href", '#/ruleManagement', 2)

print("\n1，查找规则名称与重置功能")
print("\n2，增加规则名称")

print("\n3，显示规则名称列表")
l_merge = DataMonitor_PO.ruleManage_getRuleList()
print(l_merge)

# l_merge = [list(zip(l_tmp, l_status))[i][j] for i in range(len(l_tmp)) for j in range(len(list(zip(l_tmp, l_status))[0]))]
# print(l_merge)
#
# for i in range(len(l_merge)):
#     # if l_rule[i] != '操作' and l_rule[i] != '编辑停用' and l_rule[i] != '编辑使用' :
#     print(l_merge[i])

# print(dict(zip(l_rule,l_status)))

print("\n4，编辑第3个规则")
print("编辑前：" + str(l_merge[2]))
Level_PO.clickXpath("//div[@class='el-table__fixed-body-wrapper']/table/tbody/tr[" + str(3) + "]/td[3]/div/button", 2)  # 编辑
Level_PO.inputXpathClear("//div[@class='el-table__body-wrapper is-scrolling-none']/table/tbody/tr[" + str(3) + "]/td[2]/div/span/div/input", "既往史结核与门诊就诊记录逻辑错误123")  # 替换内容
Level_PO.clickXpath("//div[@class='el-table__fixed-body-wrapper']/table/tbody/tr[" + str(3) + "]/td[3]/div/button[2]", 2)  # 保存
l_status = Level_PO.getXpathsText("//div[@class='el-table__fixed-body-wrapper']/table/tbody/tr")
l_merge = DataMonitor_PO.ruleManage_getRuleList()
print("编辑前：" + str(l_merge[2]))



print("\n5，启用第三个规则")
l_merge = DataMonitor_PO.ruleManage_getRuleList()
print("操作前：" + str(l_merge[2]))
varStatus = Level_PO.getXpathText("//div[@class='el-table__fixed-body-wrapper']/table/tbody/tr[" + str(3) + "]/td[3]/div/button[2]")
if varStatus == "停用":
    Level_PO.clickXpath("//div[@class='el-table__fixed-body-wrapper']/table/tbody/tr[" + str(3) + "]/td[3]/div/button[2]", 2)  # 点击状态按钮
    Level_PO.clickXpath("//div[@class='el-message-box']/div[3]/button[2]", 2)  # 点击确定
l_merge = DataMonitor_PO.ruleManage_getRuleList()
print("操作后：" + str(l_merge[2]))
