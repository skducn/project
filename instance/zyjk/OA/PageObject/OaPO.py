# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-6-4
# Description: OA 对象库
# *****************************************************************

from instance.zyjk.OA.config.config import *
from selenium.webdriver.common.action_chains import ActionChains


class OaPO(object):

    def __init__(self):
        self.List_PO = ListPO()
        self.Time_PO = TimePO()
        self.Color_PO = ColorPO()
        self.List_PO = ListPO()
        self.Str_PO = StrPO()
        self.Log_PO = LogPO(logFile, fmt='%(levelname)s - %(message)s - %(asctime)s')  # 输出日志


    def open(self):
        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(varURL)
        self.Web_PO.driver.maximize_window()  # 全屏
        # self.Web_PO.driver.set_window_size(1366,768)  # 按分辨率1366*768打开

    '''1、登录'''
    def login(self, varUser):
        ''' 登录 '''

        self.Web_PO.inputId("name", varUser)
        self.Web_PO.clickXpath(u"//button[@id='submit']", 2)

    def memu(self, varMemuName, varSubName):
        '''点击左侧菜单,并选择模块'''

        # # 获取菜单列表
        x = self.Web_PO.getXpathsText("//div")
        list1 = []
        for i in x :
            if "快捷菜单" in i:
                list1.append(i)
                break
        list2 = []
        for i in range(len(str(list1[0]).split("\n"))):
            if Str_PO.isContainChinese(str(list1[0]).split("\n")[i]) == True:
                list2.append(str(list1[0]).split("\n")[i])
        # print(list2)
        for j in range(len(list2)):
            if list2[j] == varMemuName:
                self.Web_PO.clickXpath("//ul[@id='first_menu']/li[" + str(j+1) + "]", 2)
                x = self.Web_PO.getXpathsText("//li")
                list3 = []
                list4 = []
                for i in x:
                    if varMemuName in i:
                        list3.append(i)
                        break
                # print(list3)
                for i in range(len(str(list3[0]).split("\n"))):
                    if str(list3[0]).split("\n")[i] != varMemuName and Str_PO.isContainChinese(str(list3[0]).split("\n")[i]) == True:
                        list4.append(str(list3[0]).split("\n")[i])
                # print(list4)
                for k in range(len(list4)):
                    if list4[k] == varSubName:
                        self.Web_PO.clickXpath("//ul[@id='first_menu']/li[" + str(j+1) + "]/div[2]/ul/li[" + str(k+1) + "]/a", 2)

    def getWorkQty(self):
        # # 检查 常用工作中表单数量，应该3个。
        list1 = self.Web_PO.getXpathsText("//li")
        # print(list1)
        qty = len(list1) - 4
        if qty == 3:
            print("ok, 工作流 - 新建工作 - 常用工作表单数量3个。")
        else:
            print("errorrrrrrrrrr, 工作流 - 新建工作 - 常用工作表单数量" + qty + "个!")








    '''2、创建申请单'''
    def createRequisition(self, company, type, period, starttime, endtime, content):
        # 打开申请单
        self.Level_PO.inIframeXpth("//div[@id='right']/iframe", 1)
        self.Level_PO.clickXpath("//input[contains(@onclick,'quick_flow')]", 1)
        self.Level_PO.outIframe(2)
        # 填写申请单
        self.Level_PO.inIframeXpth("//iframe[@id='workflow-form-frame']", 1)
        self.Level_PO.inIframeXpth("//iframe[@id='work_form_data']", 1)
        self.Level_PO.selectXpathText(u"//select[@title='公司']", company)
        self.Level_PO.clickXpath(u"//input[@value='" + type + "']", 1)
        self.Level_PO.clickXpath(u"//input[@value='" + period + "']", 1)
        self.Level_PO.inputXpath(u"//input[@title='加班开始时间']", starttime)
        self.Level_PO.inputXpath(u"//input[@title='加班结束时间']", endtime)
        self.Level_PO.inputXpath("//textarea[@title='加班事由']", content)
        self.Level_PO.inIframeTopDivParent(1)
        self.Level_PO.clickXpath("//input[@id='next']", 2)

        # 获取申请单，编号，流水号
        information = self.Level_PO.getXpathText("//h3[@id='myModalLabel']")
        # varNo = information.split("NO.")[1].split('流水号')[0].strip()  # 获取编号，如：1194
        varSerial = information.split("流水号：")[1].split('（')[0].strip()  # 获取流水号，如：20190507090
        print(information)
        # printColor('\033[1;31;47m', 'printGreen', information)

        # 获取当前步骤
        varStep = self.Level_PO.getXpathText("//div[@id='op_user_show_info']")
        print(varStep)


        # 获取下一步经办人
        varNextPerson = self.Level_PO.getXpathText("//ul[@id='work-next-prcs-block']/li/div[2]/div[1]/div[2]")
        varNextPerson = str(varNextPerson).replace("×", "").replace(" ", "")
        print("经办人：" + varNextPerson)

        self.Level_PO.clickXpath("//button[@id='work_run_submit']", 2)
        self.Level_PO.outIframe(1)

        return varSerial, varNextPerson

    def backlog(self, varSerial, varStatus, varConfirm, varFeedback, varContent):
        # 待办工作列表，进入对于的申请单
        self.Level_PO.inIframeXpth("//iframe[@id='workflow-data-list']", 2)
        self.Level_PO.clickXpathsTextContain("//td[@aria-describedby='gridTable_run_name']/a", varSerial, 2)
        self.Level_PO.outIframe(2)

        # 申请单中进行审核
        self.Level_PO.inIframeXpth("//iframe[@id='workflow-form-frame']", 1)
        if varStatus == "on":
            self.Level_PO.inIframeXpth("//iframe[@id='work_form_data']", 1)
            self.Level_PO.clickXpath(u"//input[@title='" + varConfirm + "']", 2)
            self.Level_PO.inputXpath(u"//textarea[@title='" + varFeedback + "']", varContent)
            self.Level_PO.inIframeTopDivParent(1)
        self.Level_PO.clickXpath("//input[@id='next']", 2)

        # 获取当前步骤
        varStep = self.Level_PO.getXpathText("//div[@id='op_user_show_info']")
        print(varStep)

        # 获取下一步经办人
        if varStatus == "on":
            varNextPerson = self.Level_PO.getXpathText("//ul[@id='work-next-prcs-block']/li/div[2]/div[1]/div[2]")
            varNextPerson = str(varNextPerson).replace("×", "").replace(" ", "")
            print("经办人：" + varNextPerson)

        self.Level_PO.clickXpath("//button[@id='work_run_submit']", 2)
        # 结束流程
        if varStatus == "off":
            self.Level_PO.popupAlert("accept", 2)
        self.Level_PO.outIframe(1)
        if varStatus == "off":
            return
        else:
            return varNextPerson

    def notice(self, varSerial):
        # 待办工作列表，进入对于的申请单
        self.Level_PO.inIframeXpth("//iframe[@id='workflow-data-list']", 2)
        self.Level_PO.clickXpathsTextContain("//td[@aria-describedby='gridTable_run_name']/a", varSerial, 2)
        self.Level_PO.outIframe(2)

        # 申请单中进行审核
        self.Level_PO.inIframeXpth("//iframe[@id='workflow-form-frame']", 1)
        self.Level_PO.clickXpath("//input[@id='next']", 2)

        # 获取当前步骤
        varStep = self.Level_PO.getXpathText("//div[@id='op_user_show_info']")
        print(varStep)

        # 获取下一步经办人
        varNextPerson = self.Level_PO.getXpathText("//ul[@id='work-next-prcs-block']/li/div[2]/div[1]/div[2]")
        varNextPerson = str(varNextPerson).replace("×", "").replace(" ", "")
        print("经办人：" + varNextPerson)

        self.Level_PO.clickXpath("//button[@id='work_run_submit']", 2)
        self.Level_PO.outIframe(1)
        return varNextPerson