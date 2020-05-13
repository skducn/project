# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-5-12
# Description: 质控规则自动化脚本 for noOK
# *****************************************************************

from instance.zyjk.EHR.controlRule.PageObject.RulePO import *
Rule_PO = RulePO()
Excel_PO = ExcelPO()

excelFile = File_PO.getLayerPath("./config") + "\\cr1.1.xlsx"
row, col = Excel_PO.getRowCol(excelFile, "controlRule")
recordList = []

for i in range(2, 3):
    recordList = Excel_PO.getRowValue(excelFile, i, "controlRule")
    if recordList[6] != "ok":
        print(i, recordList)

        # # 1，对封面表、基本信息表、一对多表插入一条完整的档案
        # Rule_PO.execSqlFile("HrCover.sql")  # 插入一条封面表记录
        # Rule_PO.execSqlFile("HrPersonBasicInfo.sql")  # 插入一条基本信息表记录
        # Rule_PO.execSqlFile("HrAssociationInfo.sql")  # 插入一对多记录
        #

        # # 2，判断质控规则
        if len(recordList) == 8:
            Rule_PO.execQuery(recordList[7])
        elif len(recordList) == 9:
            Rule_PO.execQuery(recordList[7])
            Rule_PO.execQuery(recordList[8])
        elif len(recordList) == 10:
            Rule_PO.execQuery(recordList[7])
            Rule_PO.execQuery(recordList[8])
            Rule_PO.execQuery(recordList[9])
        elif len(recordList) == 11:
            Rule_PO.execQuery(recordList[7])
            Rule_PO.execQuery(recordList[8])
            Rule_PO.execQuery(recordList[9])
            Rule_PO.execQuery(recordList[10])


        # 3，执行质控存储过程 ?未解决
        # Rule_PO.execSqlFile1("controlRule.sql")  # 插入一对多记录
        # Rule_PO.execQuery("exec proControl")  # 设置姓名为空
        # Rule_PO.execProcedure('testjohn')


        # 4，查看/比对质控结果
        tmpList = Rule_PO.execQuery("SELECT t2.Comment,t2.Categories FROM HrRuleRecord t1 JOIN HrRule t2 ON t1.RuleId=t2.RuleId")
        for j in tmpList:
            if str(j[0]).strip() == recordList[3] and str(j[1]).strip() == recordList[4]:
                Excel_PO.writeXlsx(excelFile, "controlRule", i, 7, "ok")
            else:
                print("errorrrrrrrrrr, excel值(" + recordList[3] + "," + recordList[4] + "), 库值(" + j[0] + "," + j[1] + ")")
                Excel_PO.writeXlsx(excelFile, "controlRule", i, 7, "error")
            break

        recordList = []

        # 5，重置 HrRuleRecord 质控结果表
        # Rule_PO.execQuery("delete HrRuleRecord")
        # Rule_PO.execQuery("delete HrCover")
        # Rule_PO.execQuery("delete HrPersonBasicInfo")



