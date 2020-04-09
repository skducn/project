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
        self.Web_PO.openURL(varURL)
        self.Web_PO.driver.maximize_window()  # 全屏
        self.List_PO = ListPO()
        self.Time_PO = TimePO()

    # 登录 运营决策系统
    def login(self):

        ''' 登录 '''

        self.Web_PO.clickId("details-button", 2)
        self.Web_PO.clickId("proceed-link", 2)

        self.Web_PO.inputXpath("//input[@placeholder='用户名']", varUser)
        self.Web_PO.inputXpath("//input[@placeholder='密码']", varPass)
        self.Web_PO.clickXpath("//button[@type='button']", 3)

        # 运营决策系统
        self.Web_PO.clickXpath("//*[@id='app']/section/section/aside/div[1]/div[2]/div[2]/div[2]/div[1]", 4)
        n = self.Web_PO.driver.window_handles
        # print(n)
        self.Web_PO.driver.switch_to_window(n[1])

    # 一级菜单
    def menu1(self, varMenuName):
        self.Web_PO.clickXpathsTextContain("//li[@role='menuitem']/div/span", varMenuName, 2)

    # 二级菜单
    def menu2ByHref(self, varHref):
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

    def checkValue(self, varName, varSql, *varDate):

        # 检查 今日运营分析各名称的值与库值是否一致，如 更新日期值，昨日值，同比值
        # checkValue("今日门急诊量", 'select sum(outPCount) from bi_outpatient_yard where statisticsDate ="%s" ', varDate)

        a, b, c = self.winByP(varName)
        if "昨日" in b:
            bb = str(b).split("昨日：")[1]
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
        if "(万" in varName:
            # 0 不做处理
            if tmpTuple1[0][0] != 0 :
                varDatabase = ('%.2f' % (float(tmpTuple1[0][0]) / 10000))
            else:
                varDatabase = 0
            varCount1 = self.Web_PO.assertEqualgetValue(str(a), str(varDatabase))
        else:
            if "%" in str(a):
                varDatabase = ('%.2f' % (float(tmpTuple1[0][0])))
                varDatabase = str(varDatabase) + "%"
                varCount1 = self.Web_PO.assertEqualgetValue(str(a), str(varDatabase))
            else:
                varCount1 = self.Web_PO.assertEqualgetValue(str(a), str(tmpTuple1[0][0]))

        # 今日门急诊量（昨日值）
        varLastDate = (self.Time_PO.getBeforeAfterDate(varDate[0], -1))
        if len(varDate) == 2:
            Mysql_PO.cur.execute(varSql % (varLastDate, varLastDate))
        else:
            Mysql_PO.cur.execute(varSql % (varLastDate))
        tmpTuple2 = Mysql_PO.cur.fetchall()
        if "(万" in varName:
            varDatabase = ('%.2f' % (float(tmpTuple2[0][0]) / 10000))
            varCount2 = self.Web_PO.assertEqualgetValue(str(bb), str(varDatabase))
        else:
            if "%" in str(b):
                varDatabase = ('%.2f' % (float(tmpTuple2[0][0])))
                varCount2 = self.Web_PO.assertEqualgetValue(str(bb), str(varDatabase))
            else:
                varCount2 = self.Web_PO.assertEqualgetValue(str(bb), str(tmpTuple2[0][0]))


        # 合并后输出结果
        if varCount1 == 1 and varCount2 == 1:
            self.Web_PO.assertEqual(varCount1, varCount2, "[ok], " + varName + "（" + str(a) + "）,（" + str(b) + "）", "")
        else:
            if varCount1 == 0:
                self.Web_PO.assertEqual(1, 0, "", "[errorrrrrrrrrr], " + varName + "（" + str(a) + "）, 库值：" + str(tmpTuple1[0][0]))
            if varCount2 == 0:
                self.Web_PO.assertEqual(1, 2, "", "[errorrrrrrrrrr], " + varName + "（" + str(b) + "）, 库值：" + str(tmpTuple2[0][0]))


