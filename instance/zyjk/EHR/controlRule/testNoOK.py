# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-5-12
# Description: 质控规则自动化脚本 for noOK
# *****************************************************************

import sys
sys.path.append("../../../../")
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

        # 1，初始化测试数据（封面表、基本信息表、一对多表）
        Rule_PO.execSqlFile("HrCover.sql")  # 插入一条封面表记录
        Rule_PO.execSqlFile("HrPersonBasicInfo.sql")  # 插入一条基本信息表记录
        Rule_PO.execSqlFile("HrAssociationInfo.sql")  # 插入一对多记录

        # 2，依据判断规则，执行判断规则sql语句
        if len(recordList) == 9:
            Rule_PO.execQuery(recordList[8])
        elif len(recordList) == 10:
            Rule_PO.execQuery(recordList[8])
            Rule_PO.execQuery(recordList[9])
        elif len(recordList) == 11:
            Rule_PO.execQuery(recordList[8])
            Rule_PO.execQuery(recordList[9])
            Rule_PO.execQuery(recordList[10])
        elif len(recordList) == 12:
            Rule_PO.execQuery(recordList[8])
            Rule_PO.execQuery(recordList[9])
            Rule_PO.execQuery(recordList[10])
            Rule_PO.execQuery(recordList[11])

        # 3，执行质控存储过程
        Rule_PO.execProcedure('proControl')

        # 4，表格与数据库比对质控结果，将测试结果、质控结果写入表格；同时console控制台输出测试记录与错误测试结果。
        # 2['封面', '姓名', '姓名为空值', '姓名未填写', '完整性', '', 'error', '(姓名未填写)(数据缺失 )', 'update HrCover set name=null', '', '']
        # errorrrrrrrrrr, 表格值(姓名未填写, 完整性) <> 库值(姓名未填写, 数据缺失)
        # 如上所示，测试第二条记录，及返回错误结果
        tmpList = Rule_PO.execQuery("SELECT t2.Comment,t2.Categories FROM HrRuleRecord t1 JOIN HrRule t2 ON t1.RuleId=t2.RuleId")
        for j in tmpList:
            if str(j[0]).strip() == recordList[3] and str(j[1]).strip() == recordList[4]:
                Excel_PO.writeXlsx(excelFile, "controlRule", i, 7, "ok")
            else:
                print("errorrrrrrrrrr, 表格值(" + recordList[3] + "," + recordList[4] + ") <> 库值(" + j[0] + "," + j[1] + ")")
                Excel_PO.writeXlsx(excelFile, "controlRule", i, 7, "error")
                Excel_PO.writeXlsx(excelFile, "controlRule", i, 8, "(" + j[0] + ")(" + j[1] + ")")
            break
        recordList = []

        # 5，重置各表
        Rule_PO.execQuery("delete HrCover")  # 封面表
        Rule_PO.execQuery("delete HrPersonBasicInfo")  # 基本信息表
        Rule_PO.execQuery("delete HrRuleRecord")  # 质控结果表

