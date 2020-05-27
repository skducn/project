# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-5-12
# Description: 质控规则自动化脚本 for all
# *****************************************************************

from time import sleep
from instance.zyjk.EHR.controlRule.PageObject.RulePO import *
Rule_PO = RulePO()
Excel_PO = ExcelPO()

excelFile = File_PO.getLayerPath("./config") + "\\cr1.1.xlsx"
row, col = Excel_PO.getRowCol(excelFile, "controlRule")
recordList = []


# for i in range(2, 3):
for i in range(2, row + 1):
    recordList = Excel_PO.getRowValue(excelFile, i, "controlRule")
    # print(i, recordList)
    # print(recordList[7])
    # print(recordList[8])
    # print(len(recordList))
    # sleep(1212)

    # if recordList[8] != "" and recordList[4] == "完整性":
    if recordList[8] != "" :

        print(i, recordList)

        # 5，重置 HrRuleRecord 质控结果表
        Rule_PO.execQuery("delete HrRuleRecord")
        Rule_PO.execQuery("delete HrCover")
        Rule_PO.execQuery("delete HrPersonBasicInfo")

        # 1，对封面表、基本信息表、一对多表插入一条完整的档案
        Rule_PO.execSqlFile("HrCover.sql")  # 插入一条封面表记录
        Rule_PO.execSqlFile("HrPersonBasicInfo.sql")  # 插入一条基本信息表记录
        Rule_PO.execSqlFile("HrAssociationInfo.sql")  # 插入一对多记录

        # # 2，判断质控规则
        if len(recordList) == 9:
            Rule_PO.execQuery(recordList[8])
        elif len(recordList) == 10:
            Rule_PO.execQuery(recordList[8])
            Rule_PO.execQuery(recordList[9])

        # 3，执行质控存储过程
        Rule_PO.execProcedure('proControl')

        # 4，查看/比对质控结果
        tmpList = Rule_PO.execQuery("SELECT t2.Comment,t2.Categories FROM HrRuleRecord t1 JOIN HrRule t2 ON t1.RuleId=t2.RuleId")
        for j in tmpList:
            if str(j[0]).strip() == recordList[3] and str(j[1]).strip() == recordList[4]:
                Excel_PO.writeXlsx(excelFile, "controlRule", i, 7, "ok")
                Excel_PO.writeXlsx(excelFile, "controlRule", i, 8, "(" + j[0] + "," + j[1] + ")")
            else:
                print("errorrrrrrrrrr, excel值(" + recordList[3] + "," + recordList[4] + "), 库值(" + j[0] + "," + j[1] + ")")
                Excel_PO.writeXlsx(excelFile, "controlRule", i, 7, "error")
                Excel_PO.writeXlsx(excelFile, "controlRule", i, 8, "(" + j[0] + "," + j[1] + ")")
            break

        recordList = []

        # 5，重置 HrRuleRecord 质控结果表
        Rule_PO.execQuery("delete HrRuleRecord")
        Rule_PO.execQuery("delete HrCover")
        Rule_PO.execQuery("delete HrPersonBasicInfo")

print("end")
