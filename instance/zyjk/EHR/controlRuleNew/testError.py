# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-6-9
# Description: 新质控规则自动化脚本,testError.py
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
    recordList = []
    varResult = "error"
    time_start = time.time()

    # 初始化质控文档
    list1 = Excel_PO.getOneRowColValue(Rule_PO.switchPath("./config", Rule_PO.excelFile), Rule_PO.excelFileSheetName, 7, varResult)

    for i in range(len(list1)):
        recordList = list1[i]
        if recordList[9] != "" and "?" in recordList[9] and varResult in recordList[7]:
            # 2，清除HrRuleRecord表数据
            Rule_PO.execQuery("delete HrRuleRecord")

            # 3，修改数据库判断规则sql1，2
            Rule_PO.execQuery(str(recordList[9]).split("?")[0])
            if recordList[9] != "":
                Rule_PO.execQuery(str(recordList[10]).split("?")[0])

            # 4，执行质控接口
            os.system(Rule_PO.curl + " " + Rule_PO.rulesApi + Rule_PO.archiveNum)

            # 5，查看质控结果
            varSign = 0
            tmpList = Rule_PO.execQuery("SELECT t2.Comment,convert(nvarchar(255), t2.Categories) FROM HrRuleRecord t1 JOIN HrRule t2 ON t1.RuleId=t2.RuleId")
            # 质控出一条规则，并与表中比对一致
            if len(tmpList) == 1:
                if str(tmpList[0][0]).strip() == recordList[4] and str(tmpList[0][1]).strip() == recordList[5]:
                    Excel_PO.writeXlsx(Rule_PO.switchPath("./config", Rule_PO.excelFile), Rule_PO.excelFileSheetName, recordList[0], 7, "ok")
                    Color_PO.consoleColor("31", "36", str(recordList[0]) + "," + recordList[1] + "," + recordList[2] + "," + recordList[4] + "," + recordList[5], "")
                else:
                    Excel_PO.writeXlsx(Rule_PO.switchPath("./config", Rule_PO.excelFile), Rule_PO.excelFileSheetName, recordList[0],7, "error")
                    Color_PO.consoleColor("31", "33", str(recordList[0]) + "," + recordList[1] + "," + recordList[2] + "," + recordList[4] + "," + recordList[5], "")
                Excel_PO.writeXlsx(Rule_PO.switchPath("./config", Rule_PO.excelFile), Rule_PO.excelFileSheetName, recordList[0], 8,str(tmpList))
            else:
                # 质控出多条规则，并与表中比对一致
                for k in tmpList:
                    if recordList[4] in str(k[0]) and recordList[5] in str(k[1]):
                        varSign = 1
                        break
                    else:
                        varSign = 0
                if varSign == 1:
                    Color_PO.consoleColor("31", "36",str(recordList[0]) + "," + recordList[1] + "," + recordList[2] + "," + recordList[4] + "," + recordList[5], "")
                    Excel_PO.writeXlsx(Rule_PO.switchPath("./config", Rule_PO.excelFile), Rule_PO.excelFileSheetName, recordList[0], 7, "partOk")
                else:
                    Excel_PO.writeXlsx(Rule_PO.switchPath("./config", Rule_PO.excelFile), Rule_PO.excelFileSheetName, recordList[0], 7, "error")
                    Color_PO.consoleColor("31", "33", str(recordList[0]) + "," + recordList[1] + "," + recordList[2] + "," + recordList[4] + "," + recordList[5], "")
                # print(str(tmpList))
                Excel_PO.writeXlsx(Rule_PO.switchPath("./config", Rule_PO.excelFile), Rule_PO.excelFileSheetName, recordList[0], 8,str(tmpList))

            # 6，恢复数据库判断规则sql1/sql2
            Rule_PO.execQuery(str(recordList[9]).split("?")[1])
            if recordList[10] != "":
                Rule_PO.execQuery(str(recordList[10]).split("?")[1])

            recordList = []
        else:
            print(i)

    time_end = time.time()

    Color_PO.consoleColor("31", "31", "结束，耗时 %s 秒" % round(time_end - time_start, 2), "")
    p.terminate()

