# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-6-9
# Description: 新质控规则自动化脚本
# test
# *****************************************************************

from time import sleep
from multiprocessing import Process
from instance.zyjk.EHR.controlRuleNew.PageObject.RulePO import *
Rule_PO = RulePO()
Excel_PO = ExcelPO()
Color_PO = ColorPO()

def f():
    os.system('java -jar ' + File_PO.getLayerPath("./config") + "\\" + varJar)
if __name__ == '__main__':
    p = Process(target=f, args=())
    p.start()
    sleep(6)
    # 质控文档
    excelFile = File_PO.getLayerPath("./config") + "\\" + varExcel
    row, col = Excel_PO.getRowCol(excelFile, varExcelSheet)
    recordList = []

    time_start = time.time()
    # for i in range(99, 600):
    for i in range(2, row + 1):
        recordList = Excel_PO.getRowValue(excelFile, i, varExcelSheet)
        # print(i)

        if recordList[8] != "" and "?" in recordList[8]:
            if varRuleType == "" and varIsRun in recordList[6]:
                print(i, recordList)

                # 重置 HrRuleRecord 质控结果表
                Rule_PO.execQuery("delete HrRuleRecord")

                # 执行判断规则sql1，sql2
                Rule_PO.execQuery(str(recordList[8]).split("?")[0])
                if recordList[9] != "":
                    Rule_PO.execQuery(str(recordList[9]).split("?")[0])

                # 执行质控命令
                os.system(varCurl)

                # 比对结果
                tmpCount = Rule_PO.execQuery( "SELECT count(*) FROM HrRuleRecord t1 JOIN HrRule t2 ON t1.RuleId=t2.RuleId")
                if tmpCount[0][0] != 1:
                    Color_PO.consoleColor("31", "33", "ERROR, 表格第<" + str(i) + ">行（" + recordList[0] + "," + recordList[1] + "," + recordList[3] + "," + recordList[4] + "）有<" + str(tmpCount[0][0]) + ">条质控结果！", "")
                    Excel_PO.writeXlsx(excelFile, varExcelSheet, i, 7, "error," + str(tmpCount[0][0]))
                    Excel_PO.writeXlsx(excelFile, varExcelSheet, i, 8, str(tmpCount[0][0]) + "条问题描述！")
                else:
                    tmpList = Rule_PO.execQuery( "SELECT t2.Comment,convert(nvarchar(255), t2.Categories) FROM HrRuleRecord t1 JOIN HrRule t2 ON t1.RuleId=t2.RuleId")
                    for j in tmpList:
                        if str(j[0]).strip() == recordList[3] and str(j[1]).strip() == recordList[4]:
                            Excel_PO.writeXlsx(excelFile, varExcelSheet, i, 7, "ok")
                            Excel_PO.writeXlsx(excelFile, varExcelSheet, i, 8, "(" + j[0] + "," + j[1] + ")")
                        else:
                            Color_PO.consoleColor("31", "33", "ERROR, excel值(" + recordList[3] + "," + recordList[4] + "), 库值(" + j[0] + "," + j[1] + ")", "")
                            Excel_PO.writeXlsx(excelFile, varExcelSheet, i, 7, "error")
                            Excel_PO.writeXlsx(excelFile, varExcelSheet, i, 8, "(" + j[0] + "," + j[1] + ")")
                        break
                    recordList = []
            elif recordList[4] == varRuleType and varIsRun in recordList[6]:
                print(i, recordList)

                # 重置 HrRuleRecord 质控结果表
                Rule_PO.execQuery("delete HrRuleRecord")

                # 执行判断规则sql1，sql2  # 如：Rule_PO.execQuery("update HrCover set Name=Null")  # 数据库数据自造
                Rule_PO.execQuery(str(recordList[8]).split("?")[0])
                if recordList[9] != "":
                    Rule_PO.execQuery(str(recordList[9]).split("?")[0])

                # 执行质控命令
                os.system(varCurl)

                # 比对结果
                tmpCount = Rule_PO.execQuery(
                    "SELECT count(*) FROM HrRuleRecord t1 JOIN HrRule t2 ON t1.RuleId=t2.RuleId")
                if tmpCount[0][0] != 1:
                    Color_PO.consoleColor("31", "33",
                                          "ERROR, 表格第<" + str(i) + ">行（" + recordList[0] + "," + recordList[1] + "," +
                                          recordList[3] + "," + recordList[4] + "）有<" + str(tmpCount[0][0]) + ">条质控结果！",
                                          "")
                    Excel_PO.writeXlsx(excelFile, varExcelSheet, i, 7, "error," + str(tmpCount[0][0]))
                    Excel_PO.writeXlsx(excelFile, varExcelSheet, i, 8, str(tmpCount[0][0]) + "条问题描述！")
                else:
                    tmpList = Rule_PO.execQuery(
                        "SELECT t2.Comment,convert(nvarchar(255), t2.Categories) FROM HrRuleRecord t1 JOIN HrRule t2 ON t1.RuleId=t2.RuleId")
                    for j in tmpList:
                        if str(j[0]).strip() == recordList[3] and str(j[1]).strip() == recordList[4]:
                            Excel_PO.writeXlsx(excelFile, varExcelSheet, i, 7, "ok")
                            Excel_PO.writeXlsx(excelFile, varExcelSheet, i, 8, "(" + j[0] + "," + j[1] + ")")
                        else:
                            Color_PO.consoleColor("31", "33",
                                                  "ERROR, excel值(" + recordList[3] + "," + recordList[4] + "), 库值(" + j[
                                                      0] + "," + j[1] + ")", "")
                            Excel_PO.writeXlsx(excelFile, varExcelSheet, i, 7, "error")
                            Excel_PO.writeXlsx(excelFile, varExcelSheet, i, 8, "(" + j[0] + "," + j[1] + ")")
                        break
                    recordList = []


            # # 恢复判断规则sql1，sql2
            Rule_PO.execQuery(str(recordList[8]).split("?")[1])
            if recordList[9] != "":
                Rule_PO.execQuery(str(recordList[9]).split("?")[1])
    time_end = time.time()

    Color_PO.consoleColor("31", "31", "结束，耗时 %s 秒" % round(time_end - time_start,2), "")
    p.terminate()

