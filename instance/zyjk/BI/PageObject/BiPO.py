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
        self.Log_PO = LogPO(logFile, fmt='%(levelname)s - %(message)s - %(asctime)s')  # 输出日志

    def assertEqual(self, expected, actual, okMsg="[ok]", errMsg="[errorrrrrrrrrr]"):
        if expected == actual:            
            print("[ok]，" + okMsg)
            self.Log_PO.logger.info(okMsg)  # 输出到日志
        else:
            # print("[errorrrrrrrrrr]，" + errMsg)
            self.Color_PO.consoleColor("31", "38", "[errorrrrrrrrrr]，" + errMsg, "")
            self.Log_PO.logger.error(errMsg)  # 输出到日志

    # 登录 运营决策系统
    def login(self):

        ''' 登录 '''

        self.Web_PO.clickId("details-button", 2)
        self.Web_PO.clickId("proceed-link", 2)

        self.Web_PO.inputXpath("//input[@placeholder='用户名']", varUser)
        self.Web_PO.inputXpath("//input[@placeholder='密码']", varPass)
        self.Web_PO.clickXpath("//button[@type='button']", 2)

        # 运营决策系统
        self.Web_PO.clickXpath('//*[@id="app"]/section/section/aside/div[2]/div[2]/div/div[2]/div/div[1]/div[1]', 4)

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
    def menu2ByHref(self, varTitle, varHref, varUpdateDate):
        print(varTitle + "（" + varUpdateDate + ")" + " -" * 30)
        self.Log_PO.logger.info(varTitle + "（" + varUpdateDate + ")" + " -" * 30)  # # 输出到日志
        self.Web_PO.clickXpaths("//a[contains(@href,'" + varHref +"')]", 2)
        # 选择日期或自定义日期
        self.searchCustom(varUpdateDate, varUpdateDate)
        sleep(2)

    def getContent(self, varPath):
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
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def winByDiv(self, varCurrentTitle, varRightTitle, varKey=""):

        try:
            tmpList = self.getContent("//div")
            if varRightTitle != "":
                if varKey == "":
                    return (self.List_PO.list2dictBySerial(tmpList[0].split(varCurrentTitle)[1].split(varRightTitle)[0].split("\n")))
                else:
                    tmpDict = self.List_PO.list2dictBySerial(tmpList[0].split(varCurrentTitle)[1].split(varRightTitle)[0].split("\n"))
                    return (tmpDict[varKey])
            else:
                if varKey == "":
                    return (self.List_PO.list2dictBySerial(tmpList[0].split(varCurrentTitle)[1].split("\n")))
                else:
                    tmpDict = self.List_PO.list2dictBySerial(tmpList[0].split(varCurrentTitle)[1].split("\n"))
                    return (tmpDict[varKey])
        except:
            print("errorrrrrrrrrr," + sys._getframe().f_code.co_name + "()")

    def monitor(self, varNo, varName, varSql, *varDate):

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
            if len(varDate) == 2:
                Mysql_PO.cur.execute(varSql % (varDate[0], varDate[1]))
                errorSql1 = str(varSql).replace("%s", varDate[0])
            else:
                Mysql_PO.cur.execute(varSql % (varDate))
                errorSql1 = str(varSql).replace("%s", varDate[0])
            tmpTuple1 = Mysql_PO.cur.fetchall()

            if tmpTuple1[0][0] == None or tmpTuple1[0][0] == 0:
                varDatabase = 0
            else:
                varDatabase = tmpTuple1[0][0]
                # varDatabase = ('%.2f' % (float(tmpTuple1[0][0]) / 10000))
            varCount1 = self.Web_PO.assertEqualgetValue(str(a), str(varDatabase))

            # 昨日
            varLastDate = (self.Time_PO.getBeforeAfterDate(varDate[0], -1))
            if len(varDate) == 2:
                Mysql_PO.cur.execute(varSql % (varLastDate, varLastDate))
                errorSql2 = str(varSql).replace("%s", str(varLastDate))
            else:
                Mysql_PO.cur.execute(varSql % (varLastDate))
                errorSql2 = str(varSql).replace("%s", str(varLastDate))

            tmpTuple2 = Mysql_PO.cur.fetchall()

            if tmpTuple2[0][0] == None or tmpTuple2[0][0] == 0:
                varDatabase = 0
            else:
                # varDatabase = ('%.2f' % (float(tmpTuple2[0][0]) / 10000))
                varDatabase = tmpTuple2[0][0]
            varCount2 = self.Web_PO.assertEqualgetValue(str(varY), str(varDatabase))

        else:
            # 当前a与库存对比
            if len(varDate) == 2:
                Mysql_PO.cur.execute(varSql % (varDate[0], varDate[1]))
            else:
                Mysql_PO.cur.execute(varSql % (varDate))
            tmpTuple1 = Mysql_PO.cur.fetchall()

            if tmpTuple1[0][0] == None or tmpTuple1[0][0] == 0:
                varCount1 = self.Web_PO.assertEqualgetValue(str(a), str(0))
            else:
                varCount1 = self.Web_PO.assertEqualgetValue(str(a), str(tmpTuple1[0][0]))

            # 昨日
            varLastDate = (self.Time_PO.getBeforeAfterDate(varDate[0], -1))
            if len(varDate) == 2:
                Mysql_PO.cur.execute(varSql % (varLastDate, varLastDate))
            else:
                Mysql_PO.cur.execute(varSql % (varLastDate))
            tmpTuple2 = Mysql_PO.cur.fetchall()

            if tmpTuple2[0][0] == None or tmpTuple2[0][0] == 0:
                varCount2 = self.Web_PO.assertEqualgetValue(str(varY), str(0))
            else:
                varCount2 = self.Web_PO.assertEqualgetValue(str(varY), str(tmpTuple2[0][0]))

        # 合并后输出结果
        if varCount1 == 1 and varCount2 == 1:
            self.assertEqual(varCount1, varCount2, varNo + " " + varName + "，" + str(a) + "，" + str(b), "")
            # self.assertEqual(varCount1, varCount2, "[ok], " + varNo + " " + varName + "（" + str(a) + "）,（" + str(b) + "）", "")
        else:
            if varCount1 == 0:
                self.assertEqual(1, 0, "", varNo + " " + varName + "，页面值（" + str(a) + "），库值（" + str(tmpTuple1[0][0]) + "）\n" + str(errorSql1) + "\n")
                # self.assertEqual(1, 0, "", "[errorrrrrrrrrr], " + varNo + " " + varName + "（" + str(a) + "）, 库值：" + str(tmpTuple1[0][0]) + "\n" + str(errorSql1) + "\n")
            if varCount2 == 0:
                self.assertEqual(1, 2, "", varNo + " " + varName + "，页面值（" + str(b) + "），库值（" + str(tmpTuple2[0][0]) + "）\n" + str(errorSql2) + "\n")

    def tongqi(self, varNo, varName, varSql, *varDate):

        # 检查 今日运营分析各名称的值与库值是否一致，如 更新日期值，昨日值，同比值
        # checkValue("今日门急诊量", 'select sum(outPCount) from bi_outpatient_yard where statisticsDate ="%s" ', varDate)

        a, b, c = self.winByP(varName)
        if "同期" in b:
            bb = str(b).split("同期：")[1]
        varCount1 = 0
        varCount2 = 0

        # 如：今日门急诊量（更新日值）
        if len(varDate) == 2:
            Mysql_PO.cur.execute(varSql % (varDate[0], varDate[1]))
            errorSql = str(varSql).replace("%s", varDate[0])
        else:
            Mysql_PO.cur.execute(varSql % (varDate))
            errorSql = str(varSql).replace("%s", varDate[0])
        tmpTuple1 = Mysql_PO.cur.fetchall()
        if "(万" in varName or "(日" in varName:
            if tmpTuple1[0][0] == None or tmpTuple1[0][0] == 0 or tmpTuple1[0][0] == 0.00:
                varDatabase = 0
            else:
                varDatabase = tmpTuple1[0][0]
            varCount1 = self.Web_PO.assertEqualgetValue(str(a), str(varDatabase))
            self.assertEqual(varCount1, 1, varNo + " " + varName + "，" + str(a), varNo + " " + varName + "页面值（" + str(a) + "），库值（" + str(varDatabase) + "）\n" + str(errorSql) + "\n")
            # self.assertEqual(varCount1, 1, "[ok], " + varName + "（" + str(a) + "）", "[errorrrrrrrrrr], " + varName + "（" + str(a) + "）, 库值：" + str(varDatabase) + "\n" + str(errorSql) + "\n")
        else:
            if "使用率" in varName or "退号率" in varName or "占比" in varName or "百分比" in varName:
                if "%" in str(a):  # 页面上是否有 % 符号
                    if tmpTuple1[0][0] == None or tmpTuple1[0][0] == 0 or tmpTuple1[0][0] == 0.00:
                        varDatabase = "0%"
                    else:
                        varDatabase = ('%.2f' % (float(tmpTuple1[0][0]))) + "%"
                        if "." in a :
                            x = str(a).split(".")[1].split("%")[0]
                            if len(x) < 2:
                                a = str(a).split("%")[0] + "0%"
                    varCount1 = self.Web_PO.assertEqualgetValue(str(a), str(varDatabase))
                    self.assertEqual(varCount1, 1, varNo + " " + varName + "，" + str(a), varNo + " " + varName + "，页面值（" + str(a) + "），库值（" + str(varDatabase) + "）\n" + str(errorSql) + "\n")
                    # self.assertEqual(varCount1, 1, "[ok], " + varName + "（" + str(a) + "）", "[errorrrrrrrrrr], " + varName + "（" + str(a) + "）, 库值：" + str(varDatabase) + "\n" + str(errorSql) + "\n")
                else:
                    self.assertEqual(0, 1, "", varNo + " " + varName + "（" + str(a) + "）, 页面上缺少%")
                    # self.assertEqual(0, 1, "", "[errorrrrrrrrrr], " + varName + "（" + str(a) + "）, 页面上缺少%")
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
                varCount1 = self.Web_PO.assertEqualgetValue(str(a), str(varDatabase))
                self.assertEqual(varCount1, 1, varNo + " " + varName + "，" + str(a), varNo + " " + varName + "，页面值（" + str(a) + "），库值（" + str(varDatabase) + "）\n" + str(errorSql) + "\n")
                # self.assertEqual(varCount1, 1, "[ok], " + varName + "（" + str(a) + "）","[errorrrrrrrrrr], " + varName + "（" + str(a) + "）, 库值：" + str(varDatabase) + "\n" + str(errorSql) + "\n")

        # 同期，没有逻辑？

        # # 合并后输出结果
        # if varCount1 == 1 and varCount2 == 1:
        #     self.assertEqual(varCount1, varCount2, "[ok], " + varName + "（" + str(a) + "）,（" + str(b) + "）", "")
        # else:
        #     if varCount1 == 0:
        #         self.assertEqual(1, 0, "", "[errorrrrrrrrrr], " + varName + "（" + str(a) + "）, 库值：" + str(tmpTuple1[0][0]))
        #     if varCount2 == 0:
        #         self.assertEqual(1, 2, "", "[errorrrrrrrrrr], " + varName + "（" + str(b) + "）, 库值：" + str(tmpTuple2[0][0]))


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
        self.Web_PO.inputXpathEnter("//input[@placeholder='开始日期']", varStartDate)
        self.Web_PO.inputXpathEnter("//input[@placeholder='结束日期']", varEndDate)
        sleep(2)

    def singleSQL(self, varPageDict, varName, varSql, *varDate):

        pageDict = ""
        for k in varPageDict:
            if k == varName:
                pageDict = varPageDict[k]

        if len(varDate) == 2:
            Mysql_PO.cur.execute(varSql % (varDate[0], varDate[1]))
        else:
            Mysql_PO.cur.execute(varSql % (varDate))
        errorSql = str(varSql).replace("%s", varDate[0])

        tmpTuple1 = Mysql_PO.cur.fetchall()

        self.assertEqual(str(pageDict), str(tmpTuple1[0][0]), varName + "（" + str(pageDict) + "%）", varName + "（" + str(pageDict) + "%）, 库值：" + str(tmpTuple1[0][0]) + "\n" + str(errorSql) + "\n")
        # self.assertEqual(str(pageDict), str(tmpTuple1[0][0]), "[ok], " + varName + "（" + str(pageDict) + "%）", "[errorrrrrrrrrr], " + varName + "（" + str(pageDict) + "%）, 库值：" + str(tmpTuple1[0][0]) + "\n" + str(errorSql) + "\n")


    def top10(self, varNo, varAfterDot, varDict, varName, varSql, *varDate):
        # varAfterDot = 0 表示取整，如 12.00则转换成12
        # varAfterDot = 0.00 表示保留2位小数，如 12 转换成 12。00

        if len(varDate) == 2:
            Mysql_PO.cur.execute(varSql % (varDate[0], varDate[1]))
        else:
            Mysql_PO.cur.execute(varSql % (varDate))
        errorSql = str(varSql).replace("%s", varDate[0])
        tmpTuple = Mysql_PO.cur.fetchall()

        tmpdict1 = {}
        for k, v in tmpTuple:
            if varAfterDot == "0.00":
                if "." in str(v):
                    dotLen = str(v).split(".")[1]   # 小数点后一个0
                    if len(dotLen) == 1:
                        v = str(v) + "0"    # 补0
                else:   # 整数
                    v = str(v) + ".00"  # 补.00
            elif varAfterDot == "0":
                if "." in str(v):
                    dotLen = str(v).split(".")[1]
                    if dotLen == "00":
                        v = str(v).split(".")[0]
            tmpdict1[k] = str(v)

        self.assertEqual(varDict, tmpdict1, varNo + " " + varName + "，" + str(tmpdict1),  varNo + " " + varName + "\n页面：" + str(varDict) + "\n库值：" + str(tmpdict1) + "\n" + str(errorSql) + "\n")
        # self.assertEqual(varDict, tmpdict1, "[ok], " + varName + "（" + str(tmpdict1) + "）", "[errorrrrrrrrrr], " + varName + "\n页面：" + str(varDict) + "\n库值：" + str(tmpdict1) + "\n" + str(errorSql) + "\n")


