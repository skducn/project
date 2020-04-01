# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2019-12-6
# Description: 电子健康档案数据监控中心（PC端）之 字段更新配置
# 技巧：去掉字符串两端的数字， astring.strip(string.digits) ,如 123姓名，输出：姓名
# 扩展：astring.lstrip(string.digits) 去掉左侧数字  , astring.rstrip(string.digits) 去掉右侧数字
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



from PO.excelPO import *
excel_PO = ExcelPO()
from instance.zyjk.EHR.PageObject.DataMonitorPO import *
DataMonitor_PO = DataMonitorPO()
from instance.zyjk.EHR.web.login import *

# 字段更新配置
Level_PO.clickXpathsContain("//a", "href", '#/updateField', 2)


print("1，搜索字段名称，如搜索‘体’")
l_result, varCount = DataMonitor_PO.searchField('体')
print(l_result)
print("[OK] 模糊搜索到 " + str(varCount) + " 个‘体’，如下：")
for i in range(varCount):
    print(l_result[i])
print("\n")

sleep(1212)

print("2，获取某个渠道所有字段列表")
l_AllField, varSum = DataMonitor_PO.getAllFieldByChannel("预检")
print("[info] 预检（" + str(varSum) + "）=> " + str(l_AllField))
print("\n")


print("3,获取某个渠道所有字段名称、设置的字典")
varSum, d_FieldSetup = DataMonitor_PO.getFieldSetupByChannel("诊前")
print("[info] 诊前（" + str(varSum) + "）=> " + str(d_FieldSetup))
print("\n")


print("4,检查字段转移功能 ，如 将挂号（varSRC）中的姓名(varField)字段转移到诊前(varDEST)中")
varSRC = "预检"
varField = "体重"
varDEST = "诊前"
# 第一步，获取 源更新渠道 所有字段名
l_AllField, varSum = DataMonitor_PO.getAllFieldByChannel(varSRC)
print("[info] " + varSRC + "（" + str(varSum) + "）=> " + str(l_AllField))
# 第二步，将 源更新渠道的某个字段 转移到 目标更新渠道，并检查目标更新渠道是否存在这个字段。
l_fieldName2 = DataMonitor_PO.updateChannel(varSRC, varField, varDEST, l_AllField)
varTemp = 0
for j in range(len(l_fieldName2)):
    if varField == l_fieldName2[j]:
        varTemp = varTemp + j
if varTemp > 0:
    print("[OK] " + varSRC + "." + varField + " => " + varDEST + " 中第（" + str(varTemp+1) + "）个。")
    print("[info] " + varDEST + " => " + str(l_fieldName2))
else:
    print("[error] 字段转移失败！")
    exit()
print("\n")


print("5，将某个字段设置为启用或停用")
l_AllField, varSum = DataMonitor_PO.getAllFieldByChannel("预检")
d_AllFieldStatus = DataMonitor_PO.getAllFieldStatus("预检")
d = {}
for key in d_AllFieldStatus:
    if key == "体温":
        d.update({'体温': d_AllFieldStatus[key]})
print("[info] " + varSRC + " => 更改前：" + str(d))
DataMonitor_PO.setSingleFieldStatus(d_AllFieldStatus, "体温", "停用", l_AllField)
d_AllFieldStatus = DataMonitor_PO.getAllFieldStatus("预检")
d = {}
for key in d_AllFieldStatus:
    if key == "体温":
        d.update({'体温': d_AllFieldStatus[key]})
print("[info] " + varSRC + " => 更改后：" + str(d))
print("\n")


print("6，将所有字段设置为启用或停用")
d_AllFieldStatus = DataMonitor_PO.getAllFieldStatus("预检")
print("[info] " + varSRC + " => 更改前：" + str(d_AllFieldStatus))
DataMonitor_PO.setAllFieldStatus("启用")
d_AllFieldStatus = DataMonitor_PO.getAllFieldStatus("预检")
print("[info] " + varSRC + " => 更改后：" + str(d_AllFieldStatus))

