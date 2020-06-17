# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-6-9
# Description: 新质控规则自动化脚本,testAll.py  //执行表格里所有用例
# *****************************************************************

from instance.zyjk.EHR.controlRuleNew.PageObject.RulePO import *
Rule_PO = RulePO()
Excel_PO = ExcelPO()
Color_PO = ColorPO()

def f():
    # 1，启动jar包
    os.system('java -jar ' + Rule_PO.switchPath("./config", Rule_PO.jar))

if __name__ == '__main__':

    p = Process(target=f, args=())
    p.start()
    sleep(6)

    # 初始化质控文档
    recordList = []
    row, col = Excel_PO.getRowCol(Rule_PO.switchPath("./config", Rule_PO.excelFile), Rule_PO.excelFileSheetName)

    time_start = time.time()
    for i in range(2, row + 1):
    # for i in range(591, row + 1):
        recordList = Excel_PO.getRowValue(Rule_PO.switchPath("./config", Rule_PO.excelFile), i, Rule_PO.excelFileSheetName)

        if recordList[8] != "" and "?" in recordList[8]:

            # 2，清除HrRuleRecord表数据
            Rule_PO.execQuery("delete HrRuleRecord")

            # 3，修改数据库判断规则sql1，2
            Rule_PO.execQuery(str(recordList[8]).split("?")[0])
            if recordList[9] != "":
                Rule_PO.execQuery(str(recordList[9]).split("?")[0])

            # 4，执行质控接口
            os.system(Rule_PO.curl + " " + Rule_PO.rulesApi + Rule_PO.archiveNum)

            # 5，查看质控结果
            varSign = 0
            tmpList = Rule_PO.execQuery( "SELECT t2.Comment,convert(nvarchar(255), t2.Categories) FROM HrRuleRecord t1 JOIN HrRule t2 ON t1.RuleId=t2.RuleId")
            # 质控出一条规则，并与表中比对一致
            if len(tmpList) == 1:
                if str(tmpList[0]).strip() == recordList[3] and str(tmpList[1]).strip() == recordList[4]:
                    Excel_PO.writeXlsx(Rule_PO.switchPath("./config", Rule_PO.excelFile), Rule_PO.excelFileSheetName, i, 7, "ok")
                    Color_PO.consoleColor("31", "36", str(i) + "," + recordList[0] + "," + recordList[1] + "," + recordList[3] + "," + recordList[4], "")
                else:
                    Excel_PO.writeXlsx(Rule_PO.switchPath("./config", Rule_PO.excelFile), Rule_PO.excelFileSheetName, i, 7, "error")
                    Color_PO.consoleColor("31", "33", str(i) + "," + recordList[0] + "," + recordList[1] + "," + recordList[3] + "," + recordList[4], "")
                Excel_PO.writeXlsx(Rule_PO.switchPath("./config", Rule_PO.excelFile), Rule_PO.excelFileSheetName, i, 8, str(tmpList))
            else:
                # 质控出多条规则，并与表中比对一致
                for k in tmpList:
                    if recordList[3] in str(k[0]) and recordList[4] in str(k[1]):
                        varSign = 1
                        break
                    else:
                        varSign = 0
                if varSign == 1:
                    Excel_PO.writeXlsx(Rule_PO.switchPath("./config", Rule_PO.excelFile), Rule_PO.excelFileSheetName, i, 7, "partOk")
                    Color_PO.consoleColor("31", "36", str(i) + "," + recordList[0] + "," + recordList[1] + "," + recordList[3] + "," + recordList[4], "")
                else:
                    Excel_PO.writeXlsx(Rule_PO.switchPath("./config", Rule_PO.excelFile), Rule_PO.excelFileSheetName, i, 7, "error")
                    Color_PO.consoleColor("31", "33", str(i) + "," + recordList[0] + "," + recordList[1] + "," + recordList[3] + "," + recordList[4], "")
                Excel_PO.writeXlsx(Rule_PO.switchPath("./config", Rule_PO.excelFile), Rule_PO.excelFileSheetName, i, 8, str(tmpList))

            # 6，恢复数据库判断规则sql1/sql2
            # print(str(recordList[8]).split("?")[1])
            Rule_PO.execQuery(str(recordList[8]).split("?")[1])
            if recordList[9] != "":
                Rule_PO.execQuery(str(recordList[9]).split("?")[1])

            recordList = []
        else:
            print(i)
    time_end = time.time()

    Color_PO.consoleColor("31", "31", "结束，耗时 %s 秒" % round(time_end - time_start, 2), "")
    p.terminate()

