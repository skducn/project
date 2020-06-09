# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-6-9
# Description: 新质控规则自动化脚本
# *****************************************************************

import os
from time import sleep
from multiprocessing import Process
from instance.zyjk.EHR.controlRuleNew.PageObject.RulePO import *
Rule_PO = RulePO()
Excel_PO = ExcelPO()


def f():
    os.system('java -jar ' + File_PO.getLayerPath("./config") + "\\" + varJar)
if __name__ == '__main__':
    p = Process(target=f, args=())
    p.start()
    sleep(5)

    # 质控文档
    excelFile = File_PO.getLayerPath("./config") + "\\" + varExcel
    row, col = Excel_PO.getRowCol(excelFile, varExcelSheet)
    recordList = []

    # for i in range(2, 6):
    for i in range(2, row + 1):
        recordList = Excel_PO.getRowValue(excelFile, i, varExcelSheet)

        # if recordList[8] != "" and recordList[4] == "完整性":
        if recordList[8] != "":
            # print(i, recordList)

            # 重置 HrRuleRecord 质控结果表
            Rule_PO.execQuery("delete HrRuleRecord")
            Rule_PO.execQuery("delete HrCover")
            Rule_PO.execQuery("delete HrPersonBasicInfo")

            # 1，对封面表、基本信息表、一对多表插入一条完整的档案
            Rule_PO.execSqlFile("HrCover.sql")  # 插入一条封面表记录
            Rule_PO.execSqlFile("HrPersonBasicInfo.sql")  # 插入一条基本信息表记录
            Rule_PO.execSqlFile("HrAssociationInfo.sql")  # 插入一对多记录

            # 判断规则sql1，sql2  # 如：Rule_PO.execQuery("update HrCover set Name=Null")  # 数据库数据自造
            if len(recordList) == 9:
                Rule_PO.execQuery(recordList[8])
            elif len(recordList) == 10:
                Rule_PO.execQuery(recordList[8])
                Rule_PO.execQuery(recordList[9])

            # 执行质控命令
            os.system(varCurl)

            # 比对结果
            tmpList = Rule_PO.execQuery( "SELECT t2.Comment,convert(nvarchar(255), t2.Categories) FROM HrRuleRecord t1 JOIN HrRule t2 ON t1.RuleId=t2.RuleId")
            for j in tmpList:
                if str(j[0]).strip() == recordList[3] and str(j[1]).strip() == recordList[4]:
                    Excel_PO.writeXlsx(excelFile, varExcelSheet, i, 7, "ok")
                    Excel_PO.writeXlsx(excelFile, varExcelSheet, i, 8, "(" + j[0] + "," + j[1] + ")")
                else:
                    print("errorrrrrrrrrr, excel值(" + recordList[3] + "," + recordList[4] + "), 库值(" + j[0] + "," + j[1] + ")")
                    Excel_PO.writeXlsx(excelFile, varExcelSheet, i, 7, "error")
                    Excel_PO.writeXlsx(excelFile, varExcelSheet, i, 8, "(" + j[0] + "," + j[1] + ")")
                break
            recordList = []

            # 重置 HrRuleRecord 质控结果表
            Rule_PO.execQuery("delete HrRuleRecord")
            Rule_PO.execQuery("delete HrCover")
            Rule_PO.execQuery("delete HrPersonBasicInfo")
    print("end")
