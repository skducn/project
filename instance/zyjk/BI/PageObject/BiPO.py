# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-7-18
# Description: 白茅岭对象库
# *****************************************************************

from instance.zyjk.BI.config.config import *
from PO.WebPO import *
from PO.ListPO import *
from PO.TimePO import *


class BiPO(object):

    def __init__(self):
        self.Web_PO = WebPO("chrome")
        # self.Web_PO = WebPO("firefox")
        self.Web_PO.openURL(varURL)
        # self.Web_PO.driver.maximize_window()  # 全屏
        self.List_PO = ListPO()
        self.Time_PO = TimePO()

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
        # print(n)
        self.Web_PO.driver.switch_to_window(n[1])

    # 一级菜单
    def menu1(self, varMenuName):
        self.Web_PO.clickXpathsTextContain("//li[@role='menuitem']/div/span", varMenuName, 2)

    # 二级菜单
    def menu2ByHref(self, varTitle,varHref):
        print(varTitle + " -" * 100)
        self.Web_PO.clickXpaths("//a[contains(@href,'" + varHref +"')]", 2)

    def getContent(self, varPath):
        return self.Web_PO.getXpathsText(varPath)

    # 模块菜单
    def winByP(self, varName=""):

        ''' 模块之窗口
        输入名称，返回其他3个值'''

        try:
            tmpList1 = self.List_PO.listSplitSubList(self.getContent("//p"), 4)
            if varName == "":
                for i in range(len(tmpList1)):
                    print(tmpList1[i])
            else:
                for i in range(len(tmpList1)):
                    if varName == tmpList1[i][1]:
                        return tmpList1[i][0], tmpList1[i][2], tmpList1[i][3]
                return None
        except:
            return None

    def winByDiv(self, varListName1, varListName2, varName):

        try:
            tmpList = self.getContent("//div")
            if varListName2 != "":
                if varName == "":
                    print(self.List_PO.listBorderDict(tmpList[0].split(varListName1)[1].split(varListName2)[0].split("\n")))
                    return None
                else:
                    tmpDict = self.List_PO.listBorderDict(tmpList[0].split(varListName1)[1].split(varListName2)[0].split("\n"))
                    return (tmpDict[varName])
            else:
                if varName == "":
                    print(self.List_PO.listBorderDict(tmpList[0].split(varListName1)[1].split("\n")))
                    return None
                else:
                    tmpDict = self.List_PO.listBorderDict(tmpList[0].split(varListName1)[1].split("\n"))
                    return (tmpDict[varName])
        except:
            return None

    def monitor(self, varName, varSql, *varDate):

        # 获取模块4个值（当前值，模块名，昨日，同比），并检查与库值是否一致
        # 如：今日运营分析 ，医院总收入的当前值，昨日，同比。
        # 备注：同比未处理？
        # checkValue("今日门急诊量", 'select sum(outPCount) from bi_outpatient_yard where statisticsDate ="%s" ', varDate)

        a, b, c = self.winByP(varName)
        if "昨日" in b:
            varY = str(b).split("昨日：")[1]
        varCount1 = 0
        varCount2 = 0

        if len(varDate) == 2:
            Mysql_PO.cur.execute(varSql % (varDate[0], varDate[1]))
        else:
            Mysql_PO.cur.execute(varSql % (varDate))
        tmpTuple1 = Mysql_PO.cur.fetchall()

        if "(万" in varName:
            if tmpTuple1[0][0] == None or tmpTuple1[0][0] == 0:
                varDatabase = 0
            else:
                varDatabase = ('%.2f' % (float(tmpTuple1[0][0]) / 10000))
            varCount1 = self.Web_PO.assertEqualgetValue(str(a), str(varDatabase))
        else:
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
        if "(万" in varName:
            if tmpTuple2[0][0] == None or tmpTuple2[0][0] == 0:
                varDatabase = 0
            else:
                varDatabase = ('%.2f' % (float(tmpTuple2[0][0]) / 10000))
            varCount2 = self.Web_PO.assertEqualgetValue(str(varY), str(varDatabase))
        else:
            if tmpTuple2[0][0] == None or tmpTuple2[0][0] == 0:
                varCount2 = self.Web_PO.assertEqualgetValue(str(a), str(0))
            else:
                varCount2 = self.Web_PO.assertEqualgetValue(str(varY), str(tmpTuple2[0][0]))

        # 合并后输出结果
        if varCount1 == 1 and varCount2 == 1:
            self.Web_PO.assertEqual(varCount1, varCount2, "[ok], " + varName + "（" + str(a) + "）,（" + str(b) + "）", "")
        else:
            if varCount1 == 0:
                self.Web_PO.assertEqual(1, 0, "", "[errorrrrrrrrrr], " + varName + "（" + str(a) + "）, 库值：" + str(tmpTuple1[0][0]))
            if varCount2 == 0:
                self.Web_PO.assertEqual(1, 2, "", "[errorrrrrrrrrr], " + varName + "（" + str(b) + "）, 库值：" + str(tmpTuple2[0][0]))

    def tongqi(self, varName, varSql, *varDate):

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
        else:
            Mysql_PO.cur.execute(varSql % (varDate))
        tmpTuple1 = Mysql_PO.cur.fetchall()
        if "(万" in varName or "(日" in varName:
            if tmpTuple1[0][0] == None or tmpTuple1[0][0] == 0 or tmpTuple1[0][0] == 0.00:
                varDatabase = 0
            else:
                varDatabase = tmpTuple1[0][0]
            varCount1 = self.Web_PO.assertEqualgetValue(str(a), str(varDatabase))
        else:
            if "%" in str(a):  # 门急诊退号率
                if tmpTuple1[0][0] == 0:
                    varDatabase = "0%"
                else:
                    varDatabase = ('%.2f' % (float(tmpTuple1[0][0]))) + "%"
                varCount1 = self.Web_PO.assertEqualgetValue(str(a), str(varDatabase))
            else:
                if "." in str(tmpTuple1[0][0]):
                    x = str(tmpTuple1[0][0]).split(".")[1]
                    if x == "0":
                        varDatabase = str(tmpTuple1[0][0]).split(".")[0]
                    else:
                        if str(tmpTuple1[0][0])  =="0.00":
                            varDatabase = 0
                        else:
                            varDatabase = tmpTuple1[0][0]
                else:
                    varDatabase = tmpTuple1[0][0]
                varCount1 = self.Web_PO.assertEqualgetValue(str(a), str(varDatabase))


        self.Web_PO.assertEqual(varCount1, 1, "[ok], " + varName + "（" + str(a) + "）", "[errorrrrrrrrrr], " + varName + "（" + str(a) + "）, 库值：" + str(varDatabase))

        # 同期，没有逻辑？

        # # 合并后输出结果
        # if varCount1 == 1 and varCount2 == 1:
        #     self.Web_PO.assertEqual(varCount1, varCount2, "[ok], " + varName + "（" + str(a) + "）,（" + str(b) + "）", "")
        # else:
        #     if varCount1 == 0:
        #         self.Web_PO.assertEqual(1, 0, "", "[errorrrrrrrrrr], " + varName + "（" + str(a) + "）, 库值：" + str(tmpTuple1[0][0]))
        #     if varCount2 == 0:
        #         self.Web_PO.assertEqual(1, 2, "", "[errorrrrrrrrrr], " + varName + "（" + str(b) + "）, 库值：" + str(tmpTuple2[0][0]))


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