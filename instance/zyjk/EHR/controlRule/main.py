# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-5-12
# Description: 质控规则自动化脚本
# *****************************************************************

from instance.zyjk.EHR.controlRule.PageObject.RulePO import *
Rule_PO = RulePO()
Excel_PO = ExcelPO()

Excel_PO.writeXlsx(File_PO.getLayerPath("./config") + "\\crv1.xlsx", "cover", 2, 7, "ok")


# 1，对封面表、基本信息表、一对多表插入一条完整的档案
# Rule_PO.execSqlFile("HrCover.sql")  # 插入一条封面表记录
# Rule_PO.execSqlFile("HrPersonBasicInfo.sql")  # 插入一条基本信息表记录
# Rule_PO.execSqlFile("HrAssociationInfo.sql")  # 插入一对多记录

# 2，测试规则
# Rule_PO.execQuery("update HrCover set name=null")  # 设置姓名为空

# 3，执行质控脚本
# Rule_PO.execSqlFile("crScript.sql")

# 4，查看/比对质控结果
# list1 = Rule_PO.execQuery("SELECT t2.Comment,t2.Categories FROM HrRuleRecord t1 JOIN HrRule t2 ON t1.RuleId=t2.RuleId")
# for i in list1:
#     print(i[0])
#     print(i[1])
#     break

# 5，重置 HrRuleRecord 质控结果表
# Rule_PO.execQuery("delete HrRuleRecord")
