# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-6-9
# Description: 新质控规则自动化脚本，testError.py  //执行表格里测试结果为error的用例
# *****************************************************************

from instance.zyjk.EHR.controlRuleNew.PageObject.RulePO import *
Rule_PO = RulePO()
Excel_PO = ExcelPO()
Color_PO = ColorPO()

def f():
    # 1，启动jar包
    os.system('java -jar ' + Rule_PO.switchPath("./config", Rule_PO.jar))

if __name__ == '__main__':
    p = Process(target=f(), args=())
    p.start()
    sleep(6)

    # 初始化质控文档
    recordList = []
    row, col = Excel_PO.getRowCol(Rule_PO.switchPath("./config", Rule_PO.excelFile), Rule_PO.excelFileSheetName)

    time_start = time.time()
    for i in range(2, row + 1):
        recordList = Excel_PO.getRowValue(Rule_PO.switchPath("./config", Rule_PO.excelFile), i, Rule_PO.excelFileSheetName)
        # print(i)

        if recordList[8] != "" and "?" in recordList[8]:
            if "error" in recordList[6]:
                print(i, recordList)

                # 2，清除HrRuleRecord表数据
                Rule_PO.execQuery("delete HrRuleRecord")

                # 3，修改数据库判断规则sql1，2
                Rule_PO.execQuery(str(recordList[8]).split("?")[0])
                if recordList[9] != "":
                    Rule_PO.execQuery(str(recordList[9]).split("?")[0])

                # 4，执行质控接口
                os.system(Rule_PO.curl + " " + Rule_PO.rulesApi + Rule_PO.archiveNum)

                # 比对结果
                tmpCount = Rule_PO.execQuery( "SELECT count(*) FROM HrRuleRecord t1 JOIN HrRule t2 ON t1.RuleId=t2.RuleId")
                if tmpCount[0][0] != 1:
                    Color_PO.consoleColor("31", "33", "ERROR, 表格第<" + str(i) + ">行（" + recordList[0] + "," + recordList[1] + "," + recordList[3] + "," + recordList[4] + "）有<" + str(tmpCount[0][0]) + ">条质控结果！", "")
                    Excel_PO.writeXlsx(Rule_PO.switchPath("./config", Rule_PO.excelFile), Rule_PO.excelFileSheetName, i, 7, "error," + str(tmpCount[0][0]))
                    Excel_PO.writeXlsx(Rule_PO.switchPath("./config", Rule_PO.excelFile), Rule_PO.excelFileSheetName, i, 8, str(tmpCount[0][0]) + "条问题描述！")
                else:
                    # 5，查看质控结果
                    tmpList = Rule_PO.execQuery( "SELECT t2.Comment,convert(nvarchar(255), t2.Categories) FROM HrRuleRecord t1 JOIN HrRule t2 ON t1.RuleId=t2.RuleId")
                    for j in tmpList:
                        if str(j[0]).strip() == recordList[3] and str(j[1]).strip() == recordList[4]:
                            Excel_PO.writeXlsx(Rule_PO.switchPath("./config", Rule_PO.excelFile), Rule_PO.excelFileSheetName, i, 7, "ok")
                            Excel_PO.writeXlsx(Rule_PO.switchPath("./config", Rule_PO.excelFile), Rule_PO.excelFileSheetName, i, 8, "(" + j[0] + "," + j[1] + ")")
                        else:
                            Color_PO.consoleColor("31", "33", "ERROR, excel值(" + recordList[3] + "," + recordList[4] + "), 库值(" + j[0] + "," + j[1] + ")", "")
                            Excel_PO.writeXlsx(Rule_PO.switchPath("./config", Rule_PO.excelFile), Rule_PO.excelFileSheetName, i, 7, "error")
                            Excel_PO.writeXlsx(Rule_PO.switchPath("./config", Rule_PO.excelFile), Rule_PO.excelFileSheetName, i, 8, "(" + j[0] + "," + j[1] + ")")
                        break
                    recordList = []

            # 6，恢复数据库判断规则sql1/sql2
            Rule_PO.execQuery(str(recordList[8]).split("?")[1])
            if recordList[9] != "":
                Rule_PO.execQuery(str(recordList[9]).split("?")[1])
    time_end = time.time()

    Color_PO.consoleColor("31", "31", "结束，耗时 %s 秒" % round(time_end - time_start, 2), "")
    p.terminate()

