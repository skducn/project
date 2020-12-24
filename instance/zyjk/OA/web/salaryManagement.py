# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2020-12-22
# Description: 人力资源 - 薪酬管理（药品数据、试剂数据、提成奖金汇总、奖金明细）
# 权限：人事总监、人事专员、市场助理

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
Char_PO = CharPO()
drugFile = os.getcwd() + "\\drugTemplet.xlsx"
reagentFile = os.getcwd() + "\\reagentTemplet.xlsx"
# ******************************************************************************************************************************************************

Oa_PO.open()
Oa_PO.login("zhangyiwen")


# # 1，检查【药品数据】页中的导入药品和字段值
# Oa_PO.memu2("人力资源", "药品数据")
# Excel_PO = ExcelPO(drugFile)
# Oa_PO.Web_PO.iframeXpath("//iframe[@src='/general/appbuilder/web/zyhr/bonus-import/drug/']", 2)
# # 1）导入药品
# Oa_PO.Web_PO.clickXpath("//button[@data-url='/general/appbuilder/web/zyhr/bonus-import/import-drug']", 2)  # 导入药品
# Oa_PO.Web_PO.sendKeysId("impload", drugFile)  # 选择文件
# Oa_PO.Web_PO.clickXpath("//a[@href='/general/appbuilder/web/zyhr/bonus-import/import-drug']", 2)  # 上传
# Oa_PO.Web_PO.clickXpath("//button[@class='btn btn-default']", 2)  # 确认
# # 2）查询字段条件（药品、医药代表、医院）
# Oa_PO.Web_PO.inputXpathClear("//input[@placeholder='输入药品名称']", Excel_PO.getCellValue(1, 0))
# Oa_PO.Web_PO.inputXpathClear("//input[@placeholder='输入代表姓名']", Excel_PO.getCellValue(1, 2))
# Oa_PO.Web_PO.inputXpathClear("//input[@placeholder='输入医院名称']", Excel_PO.getCellValue(1, 5))
# Oa_PO.Web_PO.clickXpath("//button[@id='do-serach']", 2)  # 查询
# # 验证单价是否一致
# l_drug_price = Oa_PO.Web_PO.getXpathsText("//tr/td[9]")
# Oa_PO.Web_PO.assertContain(str(Excel_PO.getCellValue(1, 6)), l_drug_price[0], "[ok] 导入药品单价正确", "[error] 导入药品单价错误！" + str(Excel_PO.getCellValue(1, 6)) + "<>" + l_drug_price[0])



# # 2，检查【试剂数据】页中的导入试剂和字段值
# Oa_PO.memu2("人力资源", "试剂数据")
# Excel_PO = ExcelPO(reagentFile)
# Oa_PO.Web_PO.iframeXpath("//iframe[@src='/general/appbuilder/web/zyhr/bonus-import/reagent/']", 2)
# # # 1）导入试剂
# # Oa_PO.Web_PO.clickXpath("//button[@data-url='/general/appbuilder/web/zyhr/bonus-import/import-reagent']", 2)  # 导入试剂
# # Oa_PO.Web_PO.sendKeysId("impload", reagentFile)  # 选择文件
# # Oa_PO.Web_PO.clickXpath("//a[@href='/general/appbuilder/web/zyhr/bonus-import/import-reagent']", 2)  # 上传
# # Oa_PO.Web_PO.clickXpath("//button[@class='btn btn-default']", 2)  # 确认
# # 2）查询字段条件（回款月份、货号、代表、送货医院）
# varReceiveDate = str(Excel_PO.getCellValue(1, 15))
# print(varReceiveDate[0:7])
# Oa_PO.Web_PO.inputXpathClearEnter("//input[@placeholder='选择回款月份']", varReceiveDate[0:7])  # 回款月份 = 已收款
# Oa_PO.Web_PO.inputXpathClear("//input[@placeholder='输入货号']", Excel_PO.getCellValue(1, 7))  # 货号
# Oa_PO.Web_PO.inputXpathClear("//input[@placeholder='输入代表姓名']", Excel_PO.getCellValue(1, 18))  # 代表
# Oa_PO.Web_PO.inputXpathClear("//input[@placeholder='输入送货医院名称']", Excel_PO.getCellValue(1, 4))  # 送货医院
# Oa_PO.Web_PO.clickXpath("//button[@id='do-serach']", 2)  # 查询
# # 依据已收款日期验证含税单价是否与表格里的值一致
# l_reagent_receipt = Oa_PO.Web_PO.getXpathsText("//tr/td[14]")  # 含税单价
# Oa_PO.Web_PO.assertContain(str(Excel_PO.getCellValue(1, 12)), l_reagent_receipt[0], "[ok] 导入试剂含税单价正确", "[error] 导入试剂含税单价错误！" + str(Excel_PO.getCellValue(1, 12)) + "<>" + l_reagent_receipt[0])



# # 4,奖金明细
# # # 1），奖金计算（提成奖金汇总）
# # Oa_PO.memu2("人力资源", "提成奖金汇总")
# # Oa_PO.Web_PO.iframeXpath("//iframe[@src='/general/appbuilder/web/zyhr/bonus/total/']", 2)
# # Oa_PO.Web_PO.clickId("compute")  # 奖金计算
# # Oa_PO.Web_PO.clickXpath("//button[@class='btn btn-warning']", 2)  # 确认
# # Oa_PO.Web_PO.iframeQuit(2)
#
# # 2），检查字段值
# Oa_PO.memu2("人力资源", "奖金明细")
# Oa_PO.Web_PO.iframeXpath("//iframe[@src='/general/appbuilder/web/zyhr/bonus/index/']", 2)
# Excel_PO = ExcelPO(drugFile)
# Oa_PO.Web_PO.inputXpathClear("//input[@placeholder='输入姓名']", Excel_PO.getCellValue(1, 2))  # 姓名
# Oa_PO.Web_PO.inputXpathClearEnter("//input[@placeholder='输入月份']", "2020-09")  # 月份
# Oa_PO.Web_PO.clickXpath("//button[@id='do-serach']", 2)  # 查询
# l_month9 = Oa_PO.Web_PO.getXpathsText("//tr/td")
# # ['1', '2020-09', '王浩文+恒康正清', '王浩文+恒康正清', '王浩文', '恒康正清', '恒康正清', '140', '600', '1', '1.00', '300.00', '金山2']
# Oa_PO.Web_PO.iframeQuit(2)
# # 双月指标
# quota9 = Excel_PO.getCellValue(1, 7)
# quota10 = Excel_PO.getCellValue(1, 13)
# quota = quota9 + quota10
# Oa_PO.Web_PO.assertEqual(str(l_month9[7]), str(int(quota)), "[ok] 9月份双月指标正确", "[error] 9月份双月指标错误!" + str(l_month9[7]) + "<>" + str(int(quota)))
# # 双月进货
# purchaseStock9 = Excel_PO.getCellValue(1, 9)
# purchaseStock10 = Excel_PO.getCellValue(1, 15)
# purchaseStock = purchaseStock9 + purchaseStock10
# Oa_PO.Web_PO.assertEqual(str(l_month9[8]), str(int(purchaseStock)), "[ok] 9月份双月进货正确", "[error] 9月份双月进货错误!" + str(l_month9[8]) + "<>" + str(int(purchaseStock)))
# # 完成率
# completionRate = (purchaseStock9+purchaseStock10) / (quota9+quota10)
# if completionRate >= 0.8 :
#     Oa_PO.Web_PO.assertEqual(l_month9[9], str(1), "[ok] 9月份完成率正确", "[error] 9月份完成率错误!" + str(l_month9[9]) + "<>" + str(completionRate))
# else:
#     Oa_PO.Web_PO.assertEqual(l_month9[9], str(round(completionRate, 2)), "[ok] 9月份完成率正确","[error] 9月份完成率错误!" + str(l_month9[9]) + "<>" + str(completionRate))
# # 基础奖金单价
# baseBonusPrice = 1
# Oa_PO.Web_PO.assertContain(str(baseBonusPrice), str(l_month9[10]), "[ok] 9月份基础奖金单价正确", "[error] 9月份基础奖金单价错误!" + str(l_month9[10]) + "<>" + str(baseBonusPrice))
# # 单月奖金
# if completionRate >= 0.8 :
#     singleMonthBonus = (purchaseStock9 + purchaseStock10) * baseBonusPrice / 2
# else:
#     singleMonthBonus = (purchaseStock9 + purchaseStock10) * baseBonusPrice / 4
# Oa_PO.Web_PO.assertContain(str(singleMonthBonus), l_month9[11], "[ok] 9月份单月奖金正确", "[error] 9月份单月奖金错误!" + str(l_month9[11]) + "<>" + str(singleMonthBonus))


# 5,提成奖金汇总
# # 1），奖金计算
Oa_PO.memu2("人力资源", "提成奖金汇总")
Oa_PO.Web_PO.iframeXpath("//iframe[@src='/general/appbuilder/web/zyhr/bonus/total/']", 2)
Oa_PO.Web_PO.clickId("compute")  # 奖金计算
Oa_PO.Web_PO.clickXpath("//button[@class='btn btn-warning']", 2)  # 确认
# 查询字段
Oa_PO.Web_PO.inputXpathClearEnter("//input[@placeholder='开始']", "2020-12")  # 月份开始
Oa_PO.Web_PO.inputXpathClearEnter("//input[@placeholder='结束']", "2020-12")  # 月份结束
Oa_PO.Web_PO.inputXpathClear("//input[@placeholder='输入代表姓名']", "王浩文")  #代表
# Oa_PO.Web_PO.inputXpathClear("//input[@placeholder='输入地区']", "？")  # 地区
Oa_PO.Web_PO.clickXpath("//button[@id='do-serach']", 2)  # 查询
l_month12 = Oa_PO.Web_PO.getXpathsText("//tr/td")
print(l_month12)