# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-7-18
# Description: Bi 对象库
# *****************************************************************

from instance.zyjk.BI.config.config import *

class BiPO(object):

    def __init__(self):
        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(varURL)
        self.Web_PO.driver.maximize_window()  # 全屏
        # self.Web_PO.driver.set_window_size(1366,768)  # 按分辨率1366*768打开
        self.List_PO = ListPO()
        self.Time_PO = TimePO()
        self.Color_PO = ColorPO()
        self.List_PO = ListPO()
        self.Log_PO = LogPO(logFile, fmt='%(levelname)s - %(message)s - %(asctime)s')  # 输出日志

    def assertEqual(self, expected, actual, okMsg="[ok]", errMsg="[ERROR]"):
        if expected == actual:            
            print("[ok]，" + okMsg)
            self.Log_PO.logger.info(okMsg)  # 输出到日志
        else:
            # print("[errorrrrrrrrrr]，" + errMsg)
            self.Color_PO.consoleColor("31", "38", "[ERROR]，" + errMsg, "")
            self.Log_PO.logger.error(errMsg)  # 输出到日志

    # 登录 运营决策系统
    def login(self):

        ''' 登录 '''

        self.Web_PO.clickId("details-button", 2)
        self.Web_PO.clickId("proceed-link", 2)

        self.Web_PO.inputXpath("//input[@placeholder='用户名']", varUser)
        self.Web_PO.inputXpath("//input[@placeholder='密码']", varPass)
        self.Web_PO.clickXpath("//button[@type='button']", 2)

        # 移动决策系统
        self.Web_PO.clickXpath('//*[@id="app"]/section/section/aside/div[2]/div[2]/div/div[5]/div/div[1]/div[1]', 4)

        n = self.Web_PO.driver.window_handles
        self.Web_PO.driver.switch_to_window(n[1])

    # 一级菜单
    def menu1(self, varNo, varMenuName):
        self.Web_PO.clickXpathsTextContain("//li[@role='menuitem']/div/span", varMenuName, 2)
        print("\n")
        print((varNo + "，" + varMenuName).center(100, "-"))
        self.Log_PO.logger.info((varNo + "，" + varMenuName).center(100, "-"))  # 输出到日志

    def menu1Close(self, varMenuName):
        self.Web_PO.clickXpathsTextContain("//li[@role='menuitem']/div/span", varMenuName, 2)

    # 二级菜单
    def menu2ByHref(self, varNo2, varModel2, varHref, varUpdateDate=""):
        print(str(varNo2) + varModel2 + "（" + varUpdateDate + ")" + " -" * 30)
        self.Log_PO.logger.info(str(varNo2) + varModel2 + "（" + varUpdateDate + ")" + " -" * 30)  # # 输出到日志
        self.Web_PO.clickXpaths("//a[contains(@href,'" + varHref + "')]", 2)
        # 选择日期或自定义日期
        if varUpdateDate != "":
            self.searchCustom(varUpdateDate, varUpdateDate)
        sleep(2)

    def getContent(self, varPath):
        # return self.Web_PO.getXpathText(varPath)
        return self.Web_PO.getXpathsText(varPath)

    # 模块菜单
    def winByP(self, varName=""):

        ''' 模块之窗口
        输入名称，返回其他3个值(
        6.75
        昨日：007)
        同比：1545%'''

        try:
            tmpList1 = self.List_PO.listSplitSubList(self.getContent("//p"), 4)
            if varName == "":
                for i in range(len(tmpList1)):
                    print(tmpList1[i])
            else:
                for i in range(len(tmpList1)):
                    if varName == tmpList1[i][1]:
                        return tmpList1[i][0], tmpList1[i][2], tmpList1[i][3]
                return (varName + "不存在，请检查！")
        except:
            print("[ERROR], " + sys._getframe().f_code.co_filename + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe().f_code.co_name)



    def winByDiv(self, varName):

        tmp = self.getContent("//span")
        tmp1 = str(tmp).split(varName + "', '")[1].split("'")[0]
        # # print(tmp1)
        # tmp1 = tmp1
        # # print(tmp1)

        try:
            tmpList = self.getContent("//div")
            tmpDict = self.List_PO.list2dictBySerial(tmpList[0].split(varName)[1].split(tmp1)[0].split("\n"))
            return tmpDict

            # if varRightTitle != "":
            #     if varKey == "":
            #         return (self.List_PO.list2dictBySerial(tmpList[0].split(varCurrentTitle)[1].split(varRightTitle)[0].split("\n")))
            #     else:
            #         tmpDict = self.List_PO.list2dictBySerial(tmpList[0].split(varCurrentTitle)[1].split(varRightTitle)[0].split("\n"))
            #         return (tmpDict[varKey])
            # else:
            #     if varKey == "":
            #         return (self.List_PO.list2dictBySerial(tmpList[0].split(varCurrentTitle)[1].split("\n")))
            #     else:
            #         tmpDict = self.List_PO.list2dictBySerial(tmpList[0].split(varCurrentTitle)[1].split("\n"))
            #         return (tmpDict[varKey])
        except:
            print("[ERROR], " + sys._getframe().f_code.co_filename + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe().f_code.co_name)

    def monitor(self, varNo, varName, varSql, varDate):

        # 获取模块4个值（当前值，模块名，昨日，同比），并检查与库值是否一致
        # 如：今日运营分析 ，医院总收入的当前值，昨日，同比。
        # 备注：同比未处理？
        # checkValue("今日门急诊量", 'select sum(outPCount) from bi_outpatient_yard where statisticsDate ="%s" ', varDate)

        a, b, c = self.winByP(varName)
        if "昨日" in b:
            varY = str(b).split("昨日：")[1]
        varCount1 = 0
        varCount2 = 0
        errorSql1 = ""
        errorSql2 = ""


        if "(万" in varName:
            # 当前金额a与库存对比

            if "," in varDate:
                tmpDate = str(varDate).split(",")
                if len(tmpDate) == 2:
                    Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1]))
                elif len(tmpDate) == 3:
                    Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2]))
                elif len(tmpDate) == 4:
                    Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2], tmpDate[3]))
                elif len(tmpDate) == 5:
                    Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2], tmpDate[3], tmpDate[4]))
                elif len(tmpDate) == 6:
                    Mysql_PO.cur.execute(
                        varSql % (tmpDate[0], tmpDate[1], tmpDate[2], tmpDate[3], tmpDate[4], tmpDate[5]))
                errorSql = ""
            else:
                Mysql_PO.cur.execute(varSql % (varDate))
                errorSql = str(varSql).replace("%s", varDate)
            tmpTuple1 = Mysql_PO.cur.fetchall()


            if tmpTuple1[0][0] == None or tmpTuple1[0][0] == 0:
                varDatabase = 0
            else:
                varDatabase = tmpTuple1[0][0]
                # varDatabase = ('%.2f' % (float(tmpTuple1[0][0]) / 10000))
            # varCount1 = self.Web_PO.assertEqualgetValue(str(a), str(varDatabase))
            varCount1 = self.Web_PO.assertEqualgetValue(Char_PO.zeroByDotSmartStr(a), Char_PO.zeroByDotSmartStr(varDatabase))

            # 昨日

            if "," in varDate:
                tmp1 = str(varDate).split(",")[0]
                varLastDate = (self.Time_PO.getBeforeAfterDate(tmp1, -1))
            else:
                varLastDate = (self.Time_PO.getBeforeAfterDate(varDate, -1))

            if "," in varDate:
                tmpDate = str(varDate).split(",")
                if len(tmpDate) == 2:
                    Mysql_PO.cur.execute(varSql % (varLastDate, varLastDate))
                errorSql2 = ""
            else:
                Mysql_PO.cur.execute(varSql % (varLastDate))
                errorSql2 = str(varSql).replace("%s", str(varLastDate))

            tmpTuple2 = Mysql_PO.cur.fetchall()

            if tmpTuple2[0][0] == None or tmpTuple2[0][0] == 0:
                varDatabase = 0
            else:
                # varDatabase = ('%.2f' % (float(tmpTuple2[0][0]) / 10000))
                varDatabase = tmpTuple2[0][0]
            # varCount2 = self.Web_PO.assertEqualgetValue(str(varY), str(varDatabase))
            varCount2 = self.Web_PO.assertEqualgetValue(Char_PO.zeroByDotSmartStr(varY), Char_PO.zeroByDotSmartStr(varDatabase))

        else:
            # 当前a与库存对比
            if "," in varDate:
                tmpDate = str(varDate).split(",")
                if len(tmpDate) == 2:
                    Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1]))
                elif len(tmpDate) == 3:
                    Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2]))
                elif len(tmpDate) == 4:
                    Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2], tmpDate[3]))
                elif len(tmpDate) == 5:
                    Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2], tmpDate[3], tmpDate[4]))
                elif len(tmpDate) == 6:
                    Mysql_PO.cur.execute(
                        varSql % (tmpDate[0], tmpDate[1], tmpDate[2], tmpDate[3], tmpDate[4], tmpDate[5]))
                errorSql = ""
            else:
                Mysql_PO.cur.execute(varSql % (varDate))
                errorSql = str(varSql).replace("%s", varDate)
            tmpTuple1 = Mysql_PO.cur.fetchall()

            if tmpTuple1[0][0] == None or tmpTuple1[0][0] == 0:
                # varCount1 = self.Web_PO.assertEqualgetValue(str(a), str(0))
                varCount1 = self.Web_PO.assertEqualgetValue(Char_PO.zeroByDotSmartStr(a), Char_PO.zeroByDotSmartStr(0))
            else:
                varCount1 = self.Web_PO.assertEqualgetValue(Char_PO.zeroByDotSmartStr(a), Char_PO.zeroByDotSmartStr(tmpTuple1[0][0]))
                # varCount1 = self.Web_PO.assertEqualgetValue(str(a), str(tmpTuple1[0][0]))

            # 昨日
            tmp1 = str(varDate).split(",")[0]
            varLastDate = (self.Time_PO.getBeforeAfterDate(tmp1, -1))
            if "," in varDate:
                tmpDate = str(varDate).split(",")
                if len(tmpDate) == 2:
                    Mysql_PO.cur.execute(varSql % (varLastDate, varLastDate))
                errorSql2 = ""
            else:
                Mysql_PO.cur.execute(varSql % (varLastDate))
                errorSql2 = str(varSql).replace("%s", str(varLastDate))

            tmpTuple2 = Mysql_PO.cur.fetchall()

            if tmpTuple2[0][0] == None or tmpTuple2[0][0] == 0:
                # varCount2 = self.Web_PO.assertEqualgetValue(str(varY), str(0))
                varCount2 = self.Web_PO.assertEqualgetValue(Char_PO.zeroByDotSmartStr(varY), Char_PO.zeroByDotSmartStr(0))
            else:
                # varCount2 = self.Web_PO.assertEqualgetValue(str(varY), str(tmpTuple2[0][0]))
                varCount2 = self.Web_PO.assertEqualgetValue(Char_PO.zeroByDotSmartStr(varY), Char_PO.zeroByDotSmartStr(tmpTuple2[0][0]))

        # 合并后输出结果
        if varCount1 == 1 and varCount2 == 1:
            self.assertEqual(varCount1, varCount2, varNo + " " + varName + "，" + str(a) + "，" + str(b), "")
            # self.assertEqual(varCount1, varCount2, "[ok], " + varNo + " " + varName + "（" + str(a) + "）,（" + str(b) + "）", "")
        else:
            if varCount1 == 0:
                self.assertEqual(1, 0, "", varNo + " " + varName + "\n页面值（" + str(a) + "）\n库值（" + str(tmpTuple1[0][0]) + "）\n" + str(errorSql1) + "\n")
                # self.assertEqual(1, 0, "", "[errorrrrrrrrrr], " + varNo + " " + varName + "（" + str(a) + "）, 库值：" + str(tmpTuple1[0][0]) + "\n" + str(errorSql1) + "\n")
            if varCount2 == 0:
                self.assertEqual(1, 2, "", varNo + " " + varName + "\n页面值（" + str(b) + "）\n库值（" + str(tmpTuple2[0][0]) + "）\n" + str(errorSql2) + "\n")
        if varCount1 == 1:
            return "ok", ""
        else:
            return "error", "页面值（" + str(a) + "），库值（" + str(tmpTuple2[0][0]) + "）"

    def currentValue(self, varNo, varName, varSql, varDate):

        # 针对同期，同比模块，检查各模块当前值与库值是否一致，如 当前值，同期，同比值
        # a = 当前值，b = 同期值，c = 同比值
        a, b, c = self.winByP(varName)

        varCount1 = 0
        varCount2 = 0

        if "," in varDate:
            tmpDate = str(varDate).split(",")
            if len(tmpDate) == 2:
                Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1]))
            elif len(tmpDate) == 3:
                Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2]))
            elif len(tmpDate) == 4:
                Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2], tmpDate[3]))
            elif len(tmpDate) == 5:
                Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2], tmpDate[3], tmpDate[4]))
            elif len(tmpDate) == 6:
                Mysql_PO.cur.execute(
                    varSql % (tmpDate[0], tmpDate[1], tmpDate[2], tmpDate[3], tmpDate[4], tmpDate[5]))
            errorSql = varSql
        else:
            Mysql_PO.cur.execute(varSql % (varDate))
            errorSql = str(varSql).replace("%s", varDate)
        tmpTuple1 = Mysql_PO.cur.fetchall()

        if "(万" in varName or "(日" in varName:
            if tmpTuple1[0][0] == None or tmpTuple1[0][0] == 0 or tmpTuple1[0][0] == 0.00:
                varDatabase = 0
            else:
                varDatabase = tmpTuple1[0][0]
            # varCount1 = self.Web_PO.assertEqualgetValue(str(a), str(varDatabase))
            varCount1 = self.Web_PO.assertEqualgetValue(Char_PO.zeroByDotSmartStr(a), Char_PO.zeroByDotSmartStr(varDatabase))
            self.assertEqual(varCount1, 1, varNo + " " + varName + "，" + str(a), varNo + " " + varName + "\nclient(" + str(a) + ")\nserver(" + str(varDatabase) + ")\n" + str(errorSql) + "\n")
            if varCount1 == 1:
                return "ok", ""
            else:
                return "error", str(Time_PO.getDate_minus()) + "，" + str(varNo) + "，client(" + str(a) + ")，server(" + str(varDatabase) + ")"

        else:
            if "使用率" in varName or "退号率" in varName or "占比" in varName or "百分比" in varName:
                if "%" in str(a):  # 页面上是否有 % 符号
                    if tmpTuple1[0][0] == None or tmpTuple1[0][0] == 0 or tmpTuple1[0][0] == 0.00:
                        varDatabase = "0"
                    else:
                        varDatabase = ('%.2f' % (float(tmpTuple1[0][0])))

                    a = str(a).split("%")[0]
                        # if "." in a :
                        #     x = str(a).split(".")[1].split("%")[0]
                            # if len(x) < 2:  # 小数后位数
                            #     a = str(a).split("%")[0]

                    # varCount1 = self.Web_PO.assertEqualgetValue(str(a), str(varDatabase))
                    varCount1 = self.Web_PO.assertEqualgetValue(Char_PO.zeroByDotSmartStr(a), Char_PO.zeroByDotSmartStr(varDatabase))
                    self.assertEqual(varCount1, 1, varNo + " " + varName + "，" + str(a), varNo + " " + varName + "\n页面值（" + str(a) + "）\n库值（" + str(varDatabase) + "）\n" + str(errorSql) + "\n")
                    # self.assertEqual(varCount1, 1, "[ok], " + varName + "（" + str(a) + "）", "[errorrrrrrrrrr], " + varName + "（" + str(a) + "）, 库值：" + str(varDatabase) + "\n" + str(errorSql) + "\n")

                    if varCount1 == 1:
                        return "ok", ""
                    else:
                        return "error", "页面值（" + str(a) + "），库值（" + str(varDatabase) + "）"
                else:
                    self.assertEqual(0, 1, "", varNo + " " + varName + "（" + str(a) + "）, 页面上缺少%")
                    if varCount1 == 1:
                        return "ok", ""
                    else:
                        return "error",  str(a) + " 页面上缺少%"

            else:
                if "." in str(tmpTuple1[0][0]):
                    x = str(tmpTuple1[0][0]).split(".")[1]
                    if x == "0" or x == "00":
                        varDatabase = str(tmpTuple1[0][0]).split(".")[0]
                    else:
                        if str(tmpTuple1[0][0]) =="0.00":
                            varDatabase = 0
                        else:
                            varDatabase = tmpTuple1[0][0]
                else:
                    varDatabase = tmpTuple1[0][0]
                # varCount1 = self.Web_PO.assertEqualgetValue(str(a), str(varDatabase))
                varCount1 = self.Web_PO.assertEqualgetValue(Char_PO.zeroByDotSmartStr(a), Char_PO.zeroByDotSmartStr(varDatabase))
                self.assertEqual(varCount1, 1, varNo + " " + varName + "，" + str(a), varNo + " " + varName + "\n页面值（" + str(a) + "）\n库值（" + str(varDatabase) + "）\n" + str(errorSql) + "\n")
                # self.assertEqual(varCount1, 1, "[ok], " + varName + "（" + str(a) + "）","[errorrrrrrrrrr], " + varName + "（" + str(a) + "）, 库值：" + str(varDatabase) + "\n" + str(errorSql) + "\n")
                if varCount1 == 1:
                    return "ok", ""
                else:
                    return "error", "页面值（" + str(a) + "），库值（" + str(varDatabase) + "）"

    def tongqi(self, varNo, varName, varSql, varDate):

        # 检查 今日运营分析各名称的值与库值是否一致，如 更新日期值，昨日值，同比值
        # checkValue("今日门急诊量", 'select sum(outPCount) from bi_outpatient_yard where statisticsDate ="%s" ', varDate)

        # a = 当前值，b = 同期值，c = 同比值
        a, b, c = self.winByP(varName)
        # print(a)
        # print(b)
        # print(c)

        varCount1 = 0
        varCount2 = 0

        # 同期，同比
        if "同期" in b:
            bb = str(b).split("同期：")[1]
            # print(bb)

            if "," in varDate:
                tmpDate = str(varDate).split(",")
                if len(tmpDate) == 2:
                    Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1]))
                elif len(tmpDate) == 3:
                    Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2]))
                elif len(tmpDate) == 4:
                    Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2], tmpDate[3]))
                elif len(tmpDate) == 5:
                    Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2], tmpDate[3], tmpDate[4]))
                elif len(tmpDate) == 6:
                    Mysql_PO.cur.execute(
                        varSql % (tmpDate[0], tmpDate[1], tmpDate[2], tmpDate[3], tmpDate[4], tmpDate[5]))
                errorSql = varSql
            else:
                Mysql_PO.cur.execute(varSql % (varDate))
                errorSql = str(varSql).replace("%s", varDate)
            tmpTuple1 = Mysql_PO.cur.fetchall()

            if "(万" in varName or "(日" in varName or "(张" in varName:

                if tmpTuple1[0][0] == None or tmpTuple1[0][0] == 0 or tmpTuple1[0][0] == 0.00:
                    varDatabase = 0
                else:
                    varDatabase = tmpTuple1[0][0]
                varCount1 = self.Web_PO.assertEqualgetValue(Char_PO.zeroByDotSmartStr(bb), Char_PO.zeroByDotSmartStr(varDatabase))
                self.assertEqual(varCount1, 1, varNo + " " + varName + "，" + "同期，" + str(bb), varNo + " " + varName + "，同期 \nclient(" + str(bb) + ")\nserver（" + str(varDatabase) + "）\n" + str(errorSql) + "\n")
                if varCount1 == 1:
                    return "ok", ""
                else:
                    return "error", str(Time_PO.getDate_minus()) + "，" + str(varNo) + "，client(" + str(bb) + ")，server(" + str(varDatabase) + ")"
            else:
                if "使用率" in varName or "退号率" in varName or "占比" in varName or "百分比" in varName:
                    if "%" in str(bb):  # 页面上是否有 % 符号
                        if tmpTuple1[0][0] == None or tmpTuple1[0][0] == 0 or tmpTuple1[0][0] == 0.00:
                            varDatabase = "0"
                        else:
                            varDatabase = ('%.2f' % (float(tmpTuple1[0][0])))
                            bb = str(bb).split("%")[0]
                            # if "." in bb:
                            #     x = str(bb).split(".")[1].split("%")[0]
                            #     if len(x) < 2:
                            #         bb = str(bb).split("%")[0] + "0%"
                        # varCount1 = self.Web_PO.assertEqualgetValue(str(bb), str(varDatabase))
                        varCount1 = self.Web_PO.assertEqualgetValue(Char_PO.zeroByDotSmartStr(bb), Char_PO.zeroByDotSmartStr(varDatabase))
                        self.assertEqual(varCount1, 1, varNo + " " + varName + "，" + "同期，" + str(bb),varNo + " " + varName + "，同期\nclient(" + str(bb) + ")\nserver(" + str(varDatabase) + ")\n" + str(errorSql) + "\n")
                        if varCount1 == 1:
                            return "ok", ""
                        else:
                            return "error", str(Time_PO.getDate_minus()) + "，" + str(varNo) + "，client(" + str(bb) + ")，server(" + str(varDatabase) + ")"
                    else:
                        self.assertEqual(0, 1, "", varNo + " " + varName + "（" + str(bb) + "）, 页面上缺少%")
                        if varCount1 == 1:
                            return "ok", ""
                        else:
                            return "error", str(bb) + " 页面上缺少%"
                else:
                    if "." in str(tmpTuple1[0][0]):
                        x = str(tmpTuple1[0][0]).split(".")[1]
                        if x == "0" or x == "00":
                            varDatabase = str(tmpTuple1[0][0]).split(".")[0]
                        else:
                            if str(tmpTuple1[0][0]) == "0.00":
                                varDatabase = 0
                            else:
                                varDatabase = tmpTuple1[0][0]
                    else:
                        varDatabase = tmpTuple1[0][0]
                    # varCount1 = self.Web_PO.assertEqualgetValue(str(bb), str(varDatabase))
                    varCount1 = self.Web_PO.assertEqualgetValue(Char_PO.zeroByDotSmartStr(bb), Char_PO.zeroByDotSmartStr(varDatabase))
                    self.assertEqual(varCount1, 1, varNo + " " + varName + "，" + "同期，" + str(bb), varNo + " " + varName + "，同期\nclient(" + str(bb) + ")\nserver(" + str(varDatabase) + ")\n" + str(errorSql) + "\n")
                    if varCount1 == 1:
                        return "ok", ""
                    else:
                        return "error", str(Time_PO.getDate_minus()) + "，" + str(varNo) + "，client(" + str(bb) + ")，server(" + str(varDatabase) + ")"

    def tongbi(self, varNo, varName, varSql, varDate):

        # a = 当前值，b = 同期值，c = 同比值
        a, b, tongbi = self.winByP(varName)

        varCount1 = 0
        varCount2 = 0

        # 同比 138.60% ↑
        if "同比" in tongbi:
            tongbi = str(tongbi).split("同比： ")[1]
            # print(tongbi)

            if "," in varDate:
                tmpDate = str(varDate).split(",")
                if len(tmpDate) == 2:
                    Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1]))
                elif len(tmpDate) == 3:
                    Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2]))
                elif len(tmpDate) == 4:
                    Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2], tmpDate[3]))
                elif len(tmpDate) == 5:
                    Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2], tmpDate[3], tmpDate[4]))
                elif len(tmpDate) == 6:
                    Mysql_PO.cur.execute(
                        varSql % (tmpDate[0], tmpDate[1], tmpDate[2], tmpDate[3], tmpDate[4], tmpDate[5]))
                errorSql = varSql
            else:
                Mysql_PO.cur.execute(varSql % (varDate))
                errorSql = str(varSql).replace("%s", varDate)

            tmpTuple1 = Mysql_PO.cur.fetchall()


            if "%" in str(tongbi):  # 页面上是否有 % 符号
                varDatabase = str(tmpTuple1[0][0])
                tongbiBefore = tongbi.split("%")[0]
                # varCount1 = self.Web_PO.assertEqualgetValue(tongbiBefore, varDatabase)
                varCount1 = self.Web_PO.assertEqualgetValue(Char_PO.zeroByDotSmartStr(tongbiBefore), Char_PO.zeroByDotSmartStr(varDatabase))
                self.assertEqual(varCount1, 1, varNo + " " + varName + "，" + "同比，" + str(tongbi), varNo + " " + varName + "，同比\nclient(" + str(tongbi) + ")\nserver(" + str(tmpTuple1[0][0]) + ")\n" + str(errorSql) + "\n")
                if varCount1 == 1:
                    return "ok", ""
                else:
                    return "error", str(Time_PO.getDate_minus()) + "，" + str(varNo) + "，client(" + str(tongbi) + ")，server(" + str(tmpTuple1[0][0]) + ")"

            else:
                self.assertEqual(0, 1, "", varNo + " " + varName + "，页面上缺少%")
                if varCount1 == 1:
                    return "ok", ""
                else:
                    return "error",  str(Time_PO.getDate_minus()) + "，" + str(varNo) + " 页面上缺少%"


   # 搜索 - 选择年
    def searchYear(self, varYear):
        # 选择月
        self.Web_PO.inputXpathEnter("//input[@placeholder='选择年']", varYear)
        sleep(2)

    # 搜索 - 选择季度
    def searchSeason(self, varSeason):
        # 选择季度
        self.Web_PO.inputXpathEnter("//input[@placeholder='请选择季度']", varSeason)
        sleep(2)

    # 搜索 - 选择月
    def searchMonth(self, varMonth):
        # 选择月
        self.Web_PO.inputXpathEnter("//input[@placeholder='选择月']", varMonth)
        sleep(2)

    # 搜索 - 自定义日期
    def searchCustom(self, varStartDate, varEndDate):
        # 自定义日期
        try:
            self.Web_PO.inputXpathEnter("//input[@placeholder='开始日期']", varStartDate)
            self.Web_PO.inputXpathEnter("//input[@placeholder='结束日期']", varEndDate)
            sleep(2)
        except:
            return None

    def prescriptionRate(self, varNo, varName, varSql, varDate):
        # 门诊处方 - 处方率
        prescriptionList = []
        tmpList1 = self.getContent("//div")
        tmpList9 = tmpList1[0].split("%\n"+varName)[0].split("\n")
        prescriptionList.append(varName)
        prescriptionList.append(tmpList9[-1])
        varPageDict = self.List_PO.list2dictBySerial(prescriptionList)

        pageDict = ""
        for k in varPageDict:
            if k == varName:
                pageDict = varPageDict[k]

        if "," in varDate:
            tmpDate = str(varDate).split(",")
            if len(tmpDate) == 2:
                Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1]))
            elif len(tmpDate) == 3:
                Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2]))
            elif len(tmpDate) == 4:
                Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2], tmpDate[3]))
            elif len(tmpDate) == 5:
                Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2], tmpDate[3], tmpDate[4]))
            elif len(tmpDate) == 6:
                Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2], tmpDate[3], tmpDate[4], tmpDate[5]))
            errorSql = varSql
        else:
            Mysql_PO.cur.execute(varSql % (varDate))
            errorSql = str(varSql).replace("%s", varDate)

        tmpTuple1 = Mysql_PO.cur.fetchall()

        self.assertEqual(Char_PO.zeroByDotSmartStr(pageDict), Char_PO.zeroByDotSmartStr(tmpTuple1[0][0]), varNo + " " + varName + "，" + str(pageDict),  varNo + " " + varName + "\nclient(" + str(pageDict) + "）\nserver(" + str(tmpTuple1[0][0]) + ")\n" + str(errorSql) + "\n")
        if Char_PO.zeroByDotSmartStr(pageDict) == Char_PO.zeroByDotSmartStr(tmpTuple1[0][0]):
            return "ok", " "
        else:
            # return "error", "页面值（" + str(pageDict) + "），库值（" + str(tmpTuple1[0][0]) + "）"
            return "error", str(Time_PO.getDate_minus()) + "，" + str(varNo) + "，client(" + str(pageDict) + ")，server(" + str(tmpTuple1[0][0]) + ")"
        # self.assertEqual(str(pageDict), str(tmpTuple1[0][0]), "[ok], " + varName + "（" + str(pageDict) + "%）", "[errorrrrrrrrrr], " + varName + "（" + str(pageDict) + "%）, 库值：" + str(tmpTuple1[0][0]) + "\n" + str(errorSql) + "\n")


    def top10(self, varNo, varAfterDot, varName, varSql, varDate):
        # varAfterDot = 0 表示取整，如 12.00则转换成12
        # varAfterDot = 0.00 表示保留2位小数，如 12 转换成 12。00

        tmpList1 = self.getContent("//div")
        tmpList2 = tmpList1[0].split(varName+"\n")[1].split("%")[0].split("\n")
        tmpList2 = self.List_PO.listConvertElement(tmpList2)
        varDict = self.List_PO.list2dictBySerial(tmpList2)

        if "," in varDate:
            tmpDate = str(varDate).split(",")
            if len(tmpDate) == 2 :
                Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1]))
            elif len(tmpDate) == 3:
                Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2]))
            elif len(tmpDate) == 4:
                Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2], tmpDate[3]))
            elif len(tmpDate) == 5:
                Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2],tmpDate[3],tmpDate[4]))
            elif len(tmpDate) == 6:
                Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2],tmpDate[3],tmpDate[4],tmpDate[5]))
            errorSql = varSql
        else:
            Mysql_PO.cur.execute(varSql % (varDate))
            errorSql = str(varSql).replace("%s", varDate)

        tmpTuple = Mysql_PO.cur.fetchall()

        tmpdict1 = {}
        for k, v in tmpTuple:
            tmpdict1[k] = str(Char_PO.zeroByDotSmartStr(v))

        self.assertEqual(varDict, tmpdict1, varNo + " " + varName + "，" + str(tmpdict1),  varNo + " " + varName + "\nclient(" + str(varDict) + ")\nserver(" + str(tmpdict1) + ")\n" + str(errorSql) + "\n")
        if varDict == tmpdict1:
            return "ok", ""
        else:
            # return "error", "页面值（" + str(varDict) + "），库值（" + str(tmpdict1) + "）"
            return "error", str(Time_PO.getDate_minus()) + "，" + str(varNo) + "，client(" + str(varDict) + ")，server(" + str(tmpdict1) + ")"

    def top10right(self, varNo, varAfterDot, varName, varSql, varDate):
        # varAfterDot = 0 表示取整，如 12.00则转换成12
        # varAfterDot = 0.00 表示保留2位小数，如 12 转换成 12。00

        tmpList1 = self.getContent("//div")
        tmpList2 = self.getContent("//span")
        tmpList2 = str(tmpList2).split(varName + "', '")[1].split("'")[0]
        tmpList2 = tmpList1[0].split(varName)[1].split(tmpList2)[0].split("\n")
        tmpList2.pop()
        tmpList2.pop(0)
        varDict = self.List_PO.list2dictBySerial(tmpList2)
        # print(varDict)
        if varDict != None:
            for k,v in varDict.items():
                varDict[k] = str(Char_PO.zeroByDotSmartStr(v))

        if "," in varDate:
            tmpDate = str(varDate).split(",")
            if len(tmpDate) == 2 :
                Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1]))
            elif len(tmpDate) == 3:
                Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2]))
            elif len(tmpDate) == 4:
                Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2], tmpDate[3]))
            elif len(tmpDate) == 5:
                Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2],tmpDate[3],tmpDate[4]))
            elif len(tmpDate) == 6:
                Mysql_PO.cur.execute(varSql % (tmpDate[0], tmpDate[1], tmpDate[2],tmpDate[3],tmpDate[4],tmpDate[5]))
            errorSql = varSql
        else:
            Mysql_PO.cur.execute(varSql % (varDate))
            errorSql = str(varSql).replace("%s", varDate)

        tmpTuple = Mysql_PO.cur.fetchall()

        tmpdict1 = {}
        for k, v in tmpTuple:
            tmpdict1[k] = str(Char_PO.zeroByDotSmartStr(v))

        self.assertEqual(varDict, tmpdict1, varNo + " " + varName + "，" + str(tmpdict1),  varNo + " " + varName + "\nclient(" + str(varDict) + ")\nserver(" + str(tmpdict1) + ")\n" + str(errorSql) + "\n")
        if varDict == tmpdict1:
            return "ok", ""
        else:
            # return "error", "页面值（" + str(varDict) + "），库值（" + str(tmpdict1) + "）"
            return "error", str(Time_PO.getDate_minus()) + "，" + str(varNo) + "，client(" + str(varDict) + ")，server(" + str(tmpdict1) + ")"



