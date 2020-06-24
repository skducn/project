# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-6-4
# Description: OA 对象库
# *****************************************************************

from instance.zyjk.OA.config.config import *
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OaPO(object):

    def __init__(self):
        self.List_PO = ListPO()
        self.Time_PO = TimePO()
        self.Color_PO = ColorPO()
        self.List_PO = ListPO()
        self.Str_PO = StrPO()
        self.Char_PO = CharPO()
        self.Log_PO = LogPO(logFile, fmt='%(levelname)s - %(message)s - %(asctime)s')  # 输出日志

    def open(self):
        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(varURL)
        self.Web_PO.driver.maximize_window()  # 全屏
        # self.Web_PO.driver.set_window_size(1366,768)  # 按分辨率1366*768打开
    def login(self, varUser):
        self.Web_PO.inputId("name", varUser)
        self.Web_PO.clickXpath(u"//button[@id='submit']", 2)

    '''点击左侧菜单,选择模块'''
    def memu(self, varMemuName, varSubName):
        # # 获取菜单列表
        sleep(3)
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

    '''检查 常用工作中表单数量'''
    def getWorkQty(self):
        list1 = self.Web_PO.getXpathsText("//li")
        list2=[]
        for i in list1:
            if "快速新建" in i:
                list2.append(str(i).replace("快速新建\n", ""))
        print("工作流 - 新建工作 - 常用工作 :" + str(list2))
        # print(list2)



    '''请假 - 申请'''
    def askOffApply(self, varSerial, varApplicationName, varUser, varType, varStartDate, varEndDate, varDay):
        self.open()
        self.login(Char_PO.chinese2pinyin1(varUser))  # 申请者
        self.memu("工作流", "新建工作")  # 选择菜单与模块
        # 请假申请单页面
        self.Web_PO.iframeId("tabs_130_iframe", 2)
        self.Web_PO.clickLinktext("全部工作", 1)
        list1 = self.Web_PO.getXpathsText("//h4/span")
        for i in range(len(list1)):
            if varApplicationName in list1[i]:
                self.Web_PO.clickXpath("//ul[@id='panel-inbox']/li[" + str(i + 1) + "]/div[2]", 1)
                break
        self.Web_PO.iframeQuit(1)
        self.Web_PO.iframeId("tabs_w10000_iframe", 1)
        varNo = self.Web_PO.getXpathText("//div[@id='run_id_block']")  # 申请单编号，如 5666
        Color_PO.consoleColor("31", "36", "[" + varUser + "] " + "请假申请" + str(varDay) + "天（No." + str(varNo) + "）" + "- - " * 10,"")
        self.Web_PO.iframeId("work_form_data", 2)
        self.Web_PO.clickXpathsNum("//input[@type='radio']", varType, 2)  # 公休  请假类别，1=事假，2=调休，3=公休，4=病假，5=婚假，6=丧假，7=其他
        self.Web_PO.jsIdReadonly("DATA_4", 2)
        self.Web_PO.inputXpath("//input[@name='DATA_4']", varStartDate)  # 请假开始时间
        self.Web_PO.jsIdReadonly("DATA_5", 2)
        self.Web_PO.inputXpath("//input[@name='DATA_5']", varEndDate)  # 请假结束时间
        self.Web_PO.inputXpath("//input[@name='DATA_67']", varDay)  # 申请天数
        self.Web_PO.inputXpath("//textarea[@name='DATA_7']", varStartDate)  # 事由
        self.Web_PO.inputXpath("//textarea[@name='DATA_44']", varEndDate)  # 请代办事项
        self.Web_PO.iframeSwitch(1)
        if self.Web_PO.isElementXpath("//input[@id='onekey_next' and @type='button']") == True:
            self.Web_PO.clickXpath("//input[@id='onekey_next']", 2)  # 提交
            self.Web_PO.alertAccept()
        elif self.Web_PO.isElementXpath("//input[@id='next' and @type='button']") == True:
            self.Web_PO.clickId("next", 2)  # 提交
            self.Web_PO.clickId("work_run_submit", 2)  # 确定
            # 判断是否有弹框
            if EC.alert_is_present()(self.Web_PO.driver):
                self.Web_PO.alertAccept()
        self.Web_PO.iframeQuit(5)
        self.Web_PO.quitURL()
        print(varSerial + "申请 已提交")
        return varNo
    '''请假 - 审核'''
    def askOffAudit(self, varSerial, varApplicationName, varNo, varRole, varAudit, varIsAgree, varOpinion):
        # Oa_PO.audit("2/6, ", varNo, "部门领导", "wanglei01", "同意", "部门领导批准")
        # 不同意 没写？

        self.open()
        self.login(Char_PO.chinese2pinyin1(varAudit))  # 审核者
        self.memu("工作流", "我的工作")  # 选择菜单与模块

        # # 选择流水号
        self.Web_PO.iframeXpath("//iframe[@src='/general/workflow/list/']", 2)  # 第一层
        self.Web_PO.iframeId("workflow-data-list", 2)  # 第二层
        varNoRow = self.Web_PO.getXpathsTextPlace("//table[@id='gridTable']/tbody/tr/td[3]/div", varNo)
        self.Web_PO.clickXpaths("//table[@id='gridTable']/tbody/tr[" + str(varNoRow + 1) + "]/td[8]/a", 2)

        # 请假申请单页面
        self.Web_PO.iframeSwitch(2)
        self.Web_PO.iframeId("workflow-form-frame", 2)  # 第二层
        self.Web_PO.iframeId("work_form_data", 2)  # 第三层
        varTitle = self.Web_PO.getXpathsText("//strong")
        if varTitle[0] == varApplicationName:
            if varRole == "部门领导":
                self.Web_PO.inputXpath("//textarea[@name='DATA_12']", varOpinion)  # 审批意见
                self.Web_PO.clickXpath("//input[@name='DATA_11' and @value='" + varIsAgree + "']", 2)  # 是否同意
                self.Web_PO.iframeSwitch(1)
                if self.Web_PO.isElementXpath("//input[@id='onekey_next' and @type='button']") == True:
                    self.Web_PO.clickXpath("//input[@id='onekey_next']", 2)  # 提交
                    self.Web_PO.alertAccept()
                elif self.Web_PO.isElementXpath("//input[@id='next' and @type='button']") == True:
                    self.Web_PO.clickId("next", 2)  # 提交
                    self.Web_PO.clickId("work_run_submit", 2)  # 确定
                    # 判断是否有弹框
                    if EC.alert_is_present()(self.Web_PO.driver):
                        self.Web_PO.alertAccept()
                self.Web_PO.iframeQuit(2)
                self.Web_PO.quitURL()
            elif varRole == "人事总监":
                self.Web_PO.clickXpath("//input[@name='DATA_14' and @value='" + varIsAgree + "']", 2)  # 是否同意
                self.Web_PO.inputXpath("//textarea[@name='DATA_15']", varOpinion)  # 审批意见
                self.Web_PO.iframeSwitch(1)
                if self.Web_PO.isElementXpath("//input[@id='onekey_next' and @type='button']") == True:
                    self.Web_PO.clickXpath("//input[@id='onekey_next']", 2)  # 提交
                    self.Web_PO.alertAccept()
                elif self.Web_PO.isElementXpath("//input[@id='next' and @type='button']") == True:
                    self.Web_PO.clickId("next", 2)  # 提交
                    self.Web_PO.clickId("work_run_submit", 2)  # 确定
                    # 判断是否有弹框
                    if EC.alert_is_present()(self.Web_PO.driver):
                        self.Web_PO.alertAccept()
                self.Web_PO.iframeQuit(2)
                self.Web_PO.quitURL()
            elif varRole == "副总":
                varDay = self.Web_PO.getXpathAttr("//input[@name='DATA_67']", "value")
                self.Web_PO.inputXpath("//textarea[@name='DATA_18']", varOpinion)  # 审批意见
                self.Web_PO.clickXpath("//input[@name='DATA_21' and @value='" + varIsAgree + "']", 2)  # 是否同意
                self.Web_PO.clickXpath("//input[@name='DATA_21' and @value='" + varIsAgree + "']", 2)  # 是否同意
                self.Web_PO.iframeSwitch(1)
                if int(varDay) >= 3:
                    if self.Web_PO.isElementXpath("//input[@id='onekey_next' and @type='button']") == True:
                        self.Web_PO.clickXpath("//input[@id='onekey_next']", 2)  # 提交
                        self.Web_PO.alertAccept()
                    elif self.Web_PO.isElementXpath("//input[@id='next' and @type='button']") == True:
                        self.Web_PO.clickId("next", 2)  # 提交
                        self.Web_PO.clickId("work_run_submit", 2)  # 确定
                        # 判断是否有弹框
                        if EC.alert_is_present()(self.Web_PO.driver):
                            self.Web_PO.alertAccept()
                else:
                    if self.Web_PO.isElementId("handle_end") == True:
                        self.Web_PO.clickXpath("//input[@id='handle_end']", 2)  # 提交
                        self.Web_PO.alertAccept()
                    elif self.Web_PO.isElementId("next") == True:
                        self.Web_PO.clickId("next", 2)  # 提交
                        self.Web_PO.clickId("work_run_submit", 2)  # 确定
                self.Web_PO.iframeQuit(2)
                self.Web_PO.quitURL()
            elif varRole == "总经理":
                self.Web_PO.inputXpath("//textarea[@name='DATA_57']", varOpinion)  # 审批意见
                self.Web_PO.clickXpath("//input[@name='DATA_68' and @value='" + varIsAgree + "']", 2)  # 是否同意
                self.Web_PO.iframeSwitch(1)
                self.Web_PO.clickXpath("//input[@id='handle_end']", 2)  # 提交
                self.Web_PO.alertAccept()
                self.Web_PO.iframeQuit(2)
                self.Web_PO.quitURL()
            if varAudit == "wanglei01":
                varAudit = "王磊"
            print(varSerial + varRole + varAudit + " 已审批")
    '''请假 - 回执查询'''
    def askOffDone(self, varNo, varUser, varDay):
        self.open()
        self.login(Char_PO.chinese2pinyin1(varUser))  # 申请人
        self.memu("工作流", "我的工作")

        # 选择流水号
        self.Web_PO.iframeXpath("//iframe[@src='/general/workflow/list/']", 2)  # 第一层
        self.Web_PO.clickLinktext("办结工作", 2)
        self.Web_PO.iframeId("workflow-data-list", 2)  # 第二层
        varNoRow = self.Web_PO.getXpathsAttrPlace("//td[9]/a", "href", varNo)
        self.Web_PO.clickXpaths("//table[@id='gridTable']/tbody/tr[" + str(varNoRow + 1) + "]/td[9]/a", 2)
        self.Web_PO.iframeQuit(2)

        # 表单打印（弹出窗口）
        all_handles = self.Web_PO.driver.window_handles
        self.Web_PO.driver.switch_to.window(all_handles[1])
        x = self.Web_PO.getXpathsText("//td")
        number = str(x[0]).split("表单")[0]
        # print(number.strip(" "))  # No. 5597
        self.Web_PO.iframeId("print_frm", 2)
        list2 = self.Web_PO.getXpathsText("//td")
        list5 = self.List_PO.getSectionList(self.List_PO.getSectionList(list2, '审核信息', 'delbefore'), "流程开始（" + number.strip(" ") + "）", 'delafter')
        list6 = []
        x = 0
        for i in range(len(list5)):
            if i == 0:
                if self.Web_PO.isElementXpath("//input[@name='DATA_11' and @value='同意' and @checked]") == True:
                    list6.append("同意（部门领导）")
                    x = x + 1
                elif self.Web_PO.isElementXpath("//input[@name='DATA_11' and @value='不同意' and @checked]") == True:
                    list6.append("不同意（部门领导）")
                else:
                    list6.append("未审核（部门领导）")
            elif i == 3:
                if self.Web_PO.isElementXpath("//input[@name='DATA_14' and @value='同意' and @checked]") == True:
                    list6.append("同意（人事总监）")
                    x = x + 1
                elif self.Web_PO.isElementXpath("//input[@name='DATA_14' and @value='不同意' and @checked]") == True:
                    list6.append("不同意（人事总监）")
                else:
                    list6.append("未审核（人事总监）")
            elif i == 6:
                if self.Web_PO.isElementXpath("//input[@name='DATA_21' and @value='同意' and @checked]") == True:
                    list6.append("同意（副总）")
                    x = x + 1
                elif self.Web_PO.isElementXpath("//input[@name='DATA_21' and @value='不同意' and @checked]") == True:
                    list6.append("不同意（副总）")
                else:
                    list6.append("未审核（副总）")
            elif i == 9:
                if self.Web_PO.isElementXpath("//input[@name='DATA_68' and @value='同意' and @checked]") == True:
                    list6.append("同意（总经理）")
                    x = x + 1
                elif self.Web_PO.isElementXpath("//input[@name='DATA_68' and @value='不同意' and @checked]") == True:
                    list6.append("不同意（总经理）")
                else:
                    list6.append("未审核（总经理）")
            else:
                list6.append(list5[i])

        self.Web_PO.quitURL()
        # print(varSerial + varUser + " 查回执：")
        # list7 = []
        # # print(list6)
        # for i in list6:
        #     if "未审核（总经理）" not in i:
        #         list7.append(i)
        #     else:
        #         break
        # if len(list7) == 9:
        #     varArr = self.List_PO.listSplitArray(list7, 3)
        #     for i in range(len(varArr)):
        #         print(varArr[i])
        # elif len(list7) == 12:
        #     varArr = self.List_PO.listSplitArray(list7, 4)
        #     for i in range(len(varArr)):
        #         print(varArr[i])
        # else:
        #     print(list7)
        if varDay < 3 and x == 3:
            return "ok"
        elif varDay >= 3 and x == 4:
            return "ok"
        else:
            return list6



    '''外出 - 申请'''
    def egressionApply(self, varSerial, varUser, varOutDate, varToObject, varOutAddress, varOutReason ):

        self.open()
        self.login(Char_PO.chinese2pinyin1(varUser))
        self.memu("工作流", "新建工作")
        # 外出申请单页面
        self.Web_PO.iframeId("tabs_130_iframe", 2)
        self.Web_PO.clickLinktext("全部工作", 1)
        list1 = self.Web_PO.getXpathsText("//h4/span")
        for i in range(len(list1)):
            if "外出申请单" in list1[i]:
                self.Web_PO.clickXpath("//ul[@id='panel-inbox']/li[" + str(i+1) + "]/div[2]", 1)
                break
        self.Web_PO.iframeQuit(1)
        self.Web_PO.iframeId("tabs_w10000_iframe", 1)
        varNo = self.Web_PO.getXpathText("//div[@id='run_id_block']")  # 获取申请单编号，如 5666
        self.Web_PO.iframeId("work_form_data", 1)
        self.Web_PO.jsIdReadonly("DATA_6", 1)
        self.Web_PO.inputXpath("//input[@name='DATA_6']", varOutDate)  # 外出时间
        self.Web_PO.inputXpath("//input[@name='DATA_74']", varToObject)  # 访问对象
        self.Web_PO.inputXpath("//input[@name='DATA_72']", varOutAddress)  # 外出地点
        self.Web_PO.inputXpath("//textarea[@name='DATA_7']", varOutReason)  # 外出事由
        self.Web_PO.iframeSwitch(1)
        if self.Web_PO.isElementXpath("//input[@id='onekey_next' and @type='button']") == True:
            self.Web_PO.clickXpath("//input[@id='onekey_next']", 2)  # 提交
            self.Web_PO.alertAccept()
        elif self.Web_PO.isElementXpath("//input[@id='next' and @type='button']") == True:
            self.Web_PO.clickId("next", 2)  # 提交
            self.Web_PO.clickId("work_run_submit", 2)  # 确定
            # 判断是否有弹框
            if EC.alert_is_present()(self.Web_PO.driver):
                self.Web_PO.alertAccept()
        self.Web_PO.iframeQuit(1)
        self.Web_PO.quitURL()
        Color_PO.consoleColor("31", "33", "[" + varUser + "] " + "外出申请单" + "（No." + str(varNo) + "）" + "- - " * 10, "")
        print(varSerial + "申请 已提交")
        return varNo
    '''外出 - 审核'''
    def egressionAudit(self, varSerial, varNo, varRole, varAudit, varIsAgree, varOpinion):
        self.open()
        self.login(Char_PO.chinese2pinyin1(varAudit))  # 审核者
        self.memu("工作流", "我的工作")  # 选择菜单与模块
        # # 选择流水号
        self.Web_PO.iframeXpath("//iframe[@src='/general/workflow/list/']", 1)  # 第一层
        self.Web_PO.iframeId("workflow-data-list", 1)  # 第二层
        varNoRow = self.Web_PO.getXpathsTextPlace("//table[@id='gridTable']/tbody/tr/td[3]/div", varNo)
        self.Web_PO.clickXpaths("//table[@id='gridTable']/tbody/tr[" + str(varNoRow + 1) + "]/td[8]/a", 1)
        # 外出申请单页面
        self.Web_PO.iframeSwitch(1)
        self.Web_PO.iframeId("workflow-form-frame", 1)  # 第二层
        self.Web_PO.iframeId("work_form_data", 1)  # 第三层
        if varRole == "部门领导":
            self.Web_PO.clickXpath("//input[@name='DATA_60' and @value='" + varIsAgree + "']", 1)  # 同意/不同意
            self.Web_PO.inputXpath("//textarea[@name='DATA_61']", varOpinion)  # 审批意见
            self.Web_PO.iframeSwitch(1)
            if self.Web_PO.isElementXpath("//input[@id='onekey_next' and @type='button']") == True:
                self.Web_PO.clickXpath("//input[@id='onekey_next']", 2)  # 提交
                self.Web_PO.alertAccept()
            elif self.Web_PO.isElementXpath("//input[@id='next' and @type='button']") == True:
                self.Web_PO.clickId("next", 2)  # 提交
                self.Web_PO.clickId("work_run_submit", 2)  # 确定
                # 判断是否有弹框
                if EC.alert_is_present()(self.Web_PO.driver):
                    self.Web_PO.alertAccept()
            self.Web_PO.iframeQuit(1)
            self.Web_PO.quitURL()
        elif varRole == "行政":
            self.Web_PO.inputXpath("//textarea[@name='DATA_64']", varOpinion)  # 审批意见
            self.Web_PO.clickXpath("//input[@name='DATA_63' and @value='" + varIsAgree + "']", 1)  # 确认/有异议，备注
            self.Web_PO.iframeSwitch(1)
            self.Web_PO.clickXpath("//input[@id='handle_end']", 1)  # 提交
            self.Web_PO.alertAccept()
            self.Web_PO.iframeQuit(1)
            self.Web_PO.quitURL()
        if varAudit == "wanglei01":
            varAudit = "王磊"
        print(varSerial + varRole + varAudit + " 已审批")
    '''外出 - 申请之填写返回时间'''
    def egressionRevise(self, varSerial, varNo, varUser, varReturnDate):
        self.open()
        self.login(Char_PO.chinese2pinyin1(varUser))  # 审核者
        self.memu("工作流", "我的工作")  # 选择菜单与模块
        # # 选择流水号
        self.Web_PO.iframeXpath("//iframe[@src='/general/workflow/list/']", 1)  # 第一层
        self.Web_PO.iframeId("workflow-data-list", 1)  # 第二层
        varNoRow = self.Web_PO.getXpathsTextPlace("//table[@id='gridTable']/tbody/tr/td[3]/div", varNo)
        self.Web_PO.clickXpaths("//table[@id='gridTable']/tbody/tr[" + str(varNoRow + 1) + "]/td[8]/a", 1)
        # 外出申请单页面
        self.Web_PO.iframeSwitch(1)
        self.Web_PO.iframeId("workflow-form-frame", 1)  # 第二层
        self.Web_PO.iframeId("work_form_data", 1)  # 第三层
        self.Web_PO.jsIdReadonly("DATA_5", 1)
        self.Web_PO.inputXpath("//input[@name='DATA_5']", varReturnDate)  # 返回时间
        self.Web_PO.iframeSwitch(1)
        self.Web_PO.clickXpath("//input[@id='onekey_next']", 1)  # 提交
        self.Web_PO.alertAccept()
        self.Web_PO.iframeQuit(1)
        self.Web_PO.quitURL()
        print(varSerial + "返回时间 已填写")



    '''出差 - 申请'''
    def evectionApply(self, varSerial, varUser, varToFollow, varDay, varFromDate, varToDate, varFromCity, varToCity, varTraffic, varWork, varFee):
        '''出差申请单'''
        self.open()
        # print(Char_PO.chinese2pinyin1(varUser))
        self.login(Char_PO.chinese2pinyin1(varUser))
        self.memu("工作流", "新建工作")
        # 外出申请单页面
        self.Web_PO.iframeId("tabs_130_iframe", 2)
        self.Web_PO.clickLinktext("全部工作", 1)
        list1 = self.Web_PO.getXpathsText("//h4/span")
        for i in range(len(list1)):
            if "出差申请单" in list1[i]:
                self.Web_PO.clickXpath("//ul[@id='panel-inbox']/li[" + str(i + 1) + "]/div[2]", 1)
                break
        self.Web_PO.iframeQuit(1)
        self.Web_PO.iframeId("tabs_w10000_iframe", 1)
        varNo = self.Web_PO.getXpathText("//div[@id='run_id_block']")  # 获取申请单编号，如 5666
        self.Web_PO.iframeId("work_form_data", 1)
        self.Web_PO.inputXpath("//input[@name='DATA_76']", varToFollow)  # 随行人员
        self.Web_PO.clickXpath("//input[@value='当日出差']", 1)  # 出差性质
        self.Web_PO.inputXpath("//input[@name='DATA_80']", varDay)  # 出差天数
        self.Web_PO.inputXpath("//tr[@id='LV_79_r1']/td[2]/input", varFromDate)  # 自
        self.Web_PO.inputXpath("//tr[@id='LV_79_r1']/td[3]/input", varToDate)  # 至
        self.Web_PO.inputXpath("//tr[@id='LV_79_r1']/td[4]/input", varFromCity)  # 从城市
        self.Web_PO.inputXpath("//tr[@id='LV_79_r1']/td[5]/input", varToCity)  # 到城市
        self.Web_PO.inputXpath("//tr[@id='LV_79_r1']/td[6]/input", varTraffic)  # 交通方式
        self.Web_PO.inputXpath("//tr[@id='LV_79_r1']/td[7]/textarea", varWork)  # 工作内容
        self.Web_PO.inputXpath("//tr[@id='LV_79_r1']/td[8]/input", varFee)  # 费用预算
        self.Web_PO.iframeSwitch(1)
        if self.Web_PO.isElementXpath("//input[@id='onekey_next' and @type='button']") == True:
            self.Web_PO.clickXpath("//input[@id='onekey_next']", 2)  # 提交
            self.Web_PO.alertAccept()
        elif self.Web_PO.isElementXpath("//input[@id='next' and @type='button']") == True:
            self.Web_PO.clickId("next", 2)  # 提交
            self.Web_PO.clickId("work_run_submit", 2)  # 确定
            # 判断是否有弹框
            if EC.alert_is_present()(self.Web_PO.driver):
                self.Web_PO.alertAccept()
        self.Web_PO.iframeQuit(1)
        self.Web_PO.quitURL()
        Color_PO.consoleColor("31", "36", "[" + varUser + "] " + "出差申请" + str(varDay) + "天（No." + str(varNo) + "）" + "- - " * 10, "")
        print(varSerial + "申请 已提交")
        return varNo
    '''出差 - 审核'''
    def evectionAudit(self,varSerial, varNo, varRole, varAudit, varIsAgree, varOpinion):
        self.open()
        self.login(Char_PO.chinese2pinyin1(varAudit))
        self.memu("工作流", "我的工作")
        # # 选择流水号
        self.Web_PO.iframeXpath("//iframe[@src='/general/workflow/list/']", 1)  # 第一层
        self.Web_PO.iframeId("workflow-data-list", 1)  # 第二层
        varNoRow = self.Web_PO.getXpathsTextPlace("//table[@id='gridTable']/tbody/tr/td[3]/div", varNo)
        self.Web_PO.clickXpaths("//table[@id='gridTable']/tbody/tr[" + str(varNoRow + 1) + "]/td[8]/a", 1)
        self.Web_PO.iframeSwitch(1)
        self.Web_PO.iframeId("workflow-form-frame", 1)  # 第二层
        self.Web_PO.iframeId("work_form_data", 1)  # 第三层
        if varRole == "部门领导":
            self.Web_PO.clickXpath("//input[@name='DATA_60' and @value='" + varIsAgree + "']", 1)  # 同意/不同意
            self.Web_PO.inputXpath("//textarea[@name='DATA_61']", varOpinion)  # 审批意见
            self.Web_PO.iframeSwitch(1)
            if self.Web_PO.isElementXpath("//input[@id='onekey_next' and @type='button']") == True:
                self.Web_PO.clickXpath("//input[@id='onekey_next']", 2)  # 提交
                self.Web_PO.alertAccept()
            elif self.Web_PO.isElementXpath("//input[@id='next' and @type='button']") == True:
                self.Web_PO.clickId("next", 2)  # 提交
                self.Web_PO.clickId("work_run_submit", 2)  # 确定
                # 判断是否有弹框
                if EC.alert_is_present()(self.Web_PO.driver):
                    self.Web_PO.alertAccept()
            self.Web_PO.iframeQuit(1)
            self.Web_PO.quitURL()
        elif varRole == "副总":
            self.Web_PO.clickXpath("//input[@name='DATA_63' and @value='" + varIsAgree + "']", 1)  # 同意/不同意
            self.Web_PO.inputXpath("//textarea[@name='DATA_64']", varOpinion)  # 审批意见
            self.Web_PO.iframeSwitch(1)
            self.Web_PO.clickId("next", 1)  # 提交
            self.Web_PO.clickId("work_run_submit", 1)  # 确定
            # 判断是否有弹框
            if EC.alert_is_present()(self.Web_PO.driver):
                self.Web_PO.alertAccept()
            self.Web_PO.iframeQuit(1)
            self.Web_PO.quitURL()
        elif varRole == "行政总监":
            self.Web_PO.inputXpath("//textarea[@name='DATA_67']", varOpinion)  # 审批意见
            self.Web_PO.clickXpath("//input[@name='DATA_66' and @value='" + varIsAgree + "']", 1)  # 确认/有异议，备注
            self.Web_PO.iframeSwitch(1)
            self.Web_PO.clickId("onekey_next", 1)  # 提交
            self.Web_PO.alertAccept()
            self.Web_PO.iframeQuit(1)
            self.Web_PO.quitURL()
        elif varRole == "财务总监":
            self.Web_PO.inputXpath("//textarea[@name='DATA_70']", varOpinion)  # 审批意见
            self.Web_PO.clickXpath("//input[@name='DATA_69' and @value='" + varIsAgree + "']", 1)  # 确认/有异议，备注
            self.Web_PO.iframeSwitch(1)
            self.Web_PO.clickId("handle_end", 1)  # 提交
            self.Web_PO.alertAccept()
            self.Web_PO.iframeQuit(1)
            self.Web_PO.quitURL()
        if varAudit == "wanglei01":
            varAudit = "王磊"
        print(varSerial + varRole + varAudit + " 已审批")



    '''固定资产采购 - 申请'''
    def equipmentApply(self, varSerial, varApplicationName, varUser, varFromDate):
        '''固定资产采购'''
        self.open()
        self.login(Char_PO.chinese2pinyin1(varUser))
        self.memu("工作流", "新建工作")
        # 外出申请单页面
        self.Web_PO.iframeId("tabs_130_iframe", 2)
        self.Web_PO.clickLinktext("全部工作", 1)
        list1 = self.Web_PO.getXpathsText("//h4/span")
        for i in range(len(list1)):
            if varApplicationName in list1[i]:
                self.Web_PO.clickXpath("//ul[@id='panel-inbox']/li[" + str(i + 1) + "]/div[2]", 1)
                break
        self.Web_PO.iframeQuit(1)
        self.Web_PO.iframeId("tabs_w10000_iframe", 1)
        varNo = self.Web_PO.getXpathText("//div[@id='run_id_block']")  # 获取申请单编号，如 5666
        self.Web_PO.iframeId("work_form_data", 1)
        self.Web_PO.inputXpath("//table[@id='LV_208']/tbody/tr[2]/td[2]/input", "服务器1")  # 名称
        self.Web_PO.inputXpath("//table[@id='LV_208']/tbody/tr[2]/td[3]/input", "10")  # 数量
        self.Web_PO.inputXpath("//table[@id='LV_208']/tbody/tr[2]/td[4]/input", varFromDate)  # 期望到货时间
        self.Web_PO.inputXpath("//table[@id='LV_208']/tbody/tr[2]/td[5]/input", "50001")  # 预计总价
        self.Web_PO.inputXpath("//table[@id='LV_208']/tbody/tr[2]/td[6]/input", "HP")  # 准购厂商
        self.Web_PO.inputXpath("//table[@id='LV_208']/tbody/tr[2]/td[7]/input", "PIM项目")  # 项目名称
        self.Web_PO.inputXpath("//textarea[@name='DATA_328']", "HP123")  # 规格要求
        self.Web_PO.inputXpath("//textarea[@name='DATA_322']", "扩容需要")  # 申请购买理由
        self.Web_PO.inputXpath("//td[@id='LV_323_r1_c1']/input", "hp专卖店")  # 厂商1
        self.Web_PO.inputXpath("//td[@id='LV_323_r1_c2']/input", "hp")  # 厂牌2
        self.Web_PO.inputXpath("//td[@id='LV_323_r1_c3']/input", "50521456")  # 联系方式1
        self.Web_PO.inputXpath("//td[@id='LV_323_r1_c4']/input", "5000")  # 单价1
        self.Web_PO.inputXpath("//td[@id='LV_323_r1_c5']/input", "50000")  # 总价1
        self.Web_PO.inputXpath("//td[@id='LV_323_r2_c1']/input", "IBM直营店")  # 厂商2
        self.Web_PO.inputXpath("//td[@id='LV_323_r2_c2']/input", "IBM")  # 厂牌2
        self.Web_PO.inputXpath("//td[@id='LV_323_r2_c3']/input", "13816109050")  # 联系方式2
        self.Web_PO.inputXpath("//td[@id='LV_323_r2_c4']/input", "5001")  # 单价2
        self.Web_PO.inputXpath("//td[@id='LV_323_r2_c5']/input", "50010")  # 总价2
        self.Web_PO.inputXpath("//td[@id='LV_323_r3_c1']/input", "taobao网点")  # 厂商3
        self.Web_PO.inputXpath("//td[@id='LV_323_r3_c2']/input", "taobao")  # 厂牌3
        self.Web_PO.inputXpath("//td[@id='LV_323_r3_c3']/input", "58771632")  # 联系方式3
        self.Web_PO.inputXpath("//td[@id='LV_323_r3_c4']/input", "5002")  # 单价3
        self.Web_PO.inputXpath("//td[@id='LV_323_r3_c5']/input", "50020")  # 总价3
        self.Web_PO.iframeSwitch(1)
        self.Web_PO.clickId("next", 2)  # 提交
        self.Web_PO.clickId("work_run_submit", 2)  # 确定
        self.Web_PO.iframeQuit(1)
        self.Web_PO.quitURL()
        Color_PO.consoleColor("31", "36", varUser + "，" + varApplicationName + "（" + str(varNo) + "）" + "- - " * 10, "")
        print(varSerial + "申请 已提交")
        return varNo
    '''固定资产采购 - 审核'''
    def equipmentAudit(self,varSerial, varNo, varRole, varAudit, varIsAgree, varOpinion):
        self.open()
        self.login(Char_PO.chinese2pinyin1(varAudit))
        self.memu("工作流", "我的工作")
        # # 选择流水号
        self.Web_PO.iframeXpath("//iframe[@src='/general/workflow/list/']", 1)  # 第一层
        self.Web_PO.iframeId("workflow-data-list", 1)  # 第二层
        varNoRow = self.Web_PO.getXpathsTextPlace("//table[@id='gridTable']/tbody/tr/td[3]/div", varNo)
        self.Web_PO.clickXpaths("//table[@id='gridTable']/tbody/tr[" + str(varNoRow + 1) + "]/td[8]/a", 1)
        self.Web_PO.iframeSwitch(1)
        self.Web_PO.iframeId("workflow-form-frame", 1)  # 第二层
        self.Web_PO.iframeId("work_form_data", 1)  # 第三层
        if varRole == "部门领导":
            self.Web_PO.inputXpath("//textarea[@name='DATA_196']", varOpinion)  # 审批意见
            self.Web_PO.clickXpath("//input[@name='DATA_209' and @value='" + varIsAgree + "']", 1)  # 同意/不同意
            self.Web_PO.iframeSwitch(1)
            self.Web_PO.clickId("next", 1)  # 提交
            self.Web_PO.clickId("work_run_submit", 1)  # 确定
            # 判断是否有弹框
            if EC.alert_is_present()(self.Web_PO.driver):
                self.Web_PO.alertAccept()
            self.Web_PO.iframeQuit(1)
            self.Web_PO.quitURL()
        elif varRole == "财务主管":
            self.Web_PO.inputXpath("//textarea[@name='DATA_115']", varOpinion)  # 审批意见
            self.Web_PO.clickXpath("//input[@name='DATA_211' and @value='" + varIsAgree + "']", 1)  # 同意/不同意
            self.Web_PO.iframeSwitch(1)
            self.Web_PO.clickId("onekey_next", 1)  # 提交
            self.Web_PO.alertAccept()
            self.Web_PO.iframeQuit(1)
            self.Web_PO.quitURL()
        elif varRole == "财务经理":
            self.Web_PO.inputXpath("//textarea[@name='DATA_17']", varOpinion)  # 审批意见
            self.Web_PO.clickXpath("//input[@name='DATA_312' and @value='" + varIsAgree + "']", 1)  # 同意/不同意
            self.Web_PO.iframeSwitch(1)
            self.Web_PO.clickId("onekey_next", 1)  # 提交
            self.Web_PO.alertAccept()
            self.Web_PO.iframeQuit(1)
            self.Web_PO.quitURL()
        elif varRole == "副总":
            self.Web_PO.inputXpath("//textarea[@name='DATA_19']", varOpinion)  # 审批意见
            self.Web_PO.clickXpath("//input[@name='DATA_213' and @value='" + varIsAgree + "']", 1)  # 同意/不同意
            self.Web_PO.iframeSwitch(1)
            self.Web_PO.clickId("onekey_next", 1)  # 提交
            self.Web_PO.alertAccept()
            self.Web_PO.iframeQuit(1)
            self.Web_PO.quitURL()
        elif varRole == "总经理":
            self.Web_PO.inputXpath("//textarea[@name='DATA_21']", varOpinion)  # 审批意见
            self.Web_PO.clickXpath("//input[@name='DATA_214' and @value='" + varIsAgree + "']", 1)  # 同意/不同意
            self.Web_PO.iframeSwitch(1)
            self.Web_PO.clickId("handle_end", 1)  # 提交
            self.Web_PO.alertAccept()
            self.Web_PO.iframeQuit(1)
            self.Web_PO.quitURL()
        if varAudit == "wanglei01":
            varAudit = "王磊"
        print(varSerial + varRole + varAudit + " 已审批")
    '''固定资产采购 - 查询'''
    def equipmentDone(self, varSerial, varNo, varUser):
        # 判断审批人的状态，返回全同意或 某某不同意
        self.open()
        self.login(Char_PO.chinese2pinyin1(varUser))  # 申请人
        self.memu("工作流", "我的工作")
        # # 选择流水号
        self.Web_PO.iframeXpath("//iframe[@src='/general/workflow/list/']", 2)  # 第一层
        self.Web_PO.clickLinktext("办结工作", 2)
        self.Web_PO.iframeId("workflow-data-list", 2)  # 第二层
        varNoRow = self.Web_PO.getXpathsAttrPlace("//td[9]/a", "href", varNo)
        self.Web_PO.clickXpaths("//table[@id='gridTable']/tbody/tr[" + str(varNoRow + 1) + "]/td[9]/a", 2)
        self.Web_PO.iframeQuit(2)
        # 表单打印（弹出窗口）
        all_handles = self.Web_PO.driver.window_handles
        self.Web_PO.driver.switch_to.window(all_handles[1])
        x = self.Web_PO.getXpathsText("//td")
        number = str(x[0]).split("表单")[0]
        # print(number.strip(" "))  # No. 5597
        self.Web_PO.iframeId("print_frm", 2)
        list2 = self.Web_PO.getXpathsText("//td")
        # print(list2)

        list6 = []
        x = 0
        if self.Web_PO.isElementXpath("//input[@name='DATA_209' and @value='同意' and @checked]") == True:
            list6.append("同意（部门领导）")
            x = x + 1
        elif self.Web_PO.isElementXpath("//input[@name='DATA_209' and @value='不同意' and @checked]") == True:
            list6.append("不同意（部门领导）")
        else:
            list6.append("未审核（部门领导）")
        if self.Web_PO.isElementXpath("//input[@name='DATA_211' and @value='同意' and @checked]") == True:
            list6.append("同意（财务主管）")
            x = x + 1
        elif self.Web_PO.isElementXpath("//input[@name='DATA_211' and @value='不同意' and @checked]") == True:
            list6.append("不同意（财务主）")
        else:
            list6.append("未审核（财务主）")
        if self.Web_PO.isElementXpath("//input[@name='DATA_312' and @value='同意' and @checked]") == True:
            list6.append("同意（财务经理）")
            x = x + 1
        elif self.Web_PO.isElementXpath("//input[@name='DATA_312' and @value='不同意' and @checked]") == True:
            list6.append("不同意（财务经理）")
        else:
            list6.append("未审核（财务经理）")
        if self.Web_PO.isElementXpath("//input[@name='DATA_213' and @value='同意' and @checked]") == True:
            list6.append("同意（副总）")
            x = x + 1
        elif self.Web_PO.isElementXpath("//input[@name='DATA_213' and @value='不同意' and @checked]") == True:
            list6.append("不同意（副总）")
        else:
            list6.append("未审核（副总）")
        if self.Web_PO.isElementXpath("//input[@name='DATA_214' and @value='同意' and @checked]") == True:
            list6.append("同意（总经理）")
            x = x + 1
        elif self.Web_PO.isElementXpath("//input[@name='DATA_214' and @value='不同意' and @checked]") == True:
            list6.append("不同意（总经理）")
        else:
            list6.append("未审核（总经理）")
        print(list6)
        if x == 5 :
            return "ok"
        else:
            return (list6)



    '''借款申请单 - 申请'''
    def loanApply(self, varSerial, varApplicationName, varUser, varFromDate):
        '''借款申请单'''
        self.open()
        self.login(Char_PO.chinese2pinyin1(varUser))
        self.memu("工作流", "新建工作")
        # 外出申请单页面
        self.Web_PO.iframeId("tabs_130_iframe", 2)
        self.Web_PO.clickLinktext("全部工作", 1)
        list1 = self.Web_PO.getXpathsText("//h4/span")
        for i in range(len(list1)):
            if varApplicationName in list1[i]:
                self.Web_PO.clickXpath("//ul[@id='panel-inbox']/li[" + str(i + 1) + "]/div[2]", 1)
                break
        self.Web_PO.iframeQuit(1)
        self.Web_PO.iframeId("tabs_w10000_iframe", 1)
        varNo = self.Web_PO.getXpathText("//div[@id='run_id_block']")  # 获取申请单编号，如 5666
        self.Web_PO.iframeId("work_form_data", 1)

        self.Web_PO.inputXpath("//tr[@id='LV_208_r1_c1']/textarea", "我缺钱")  # 情况说明
        self.Web_PO.inputXpath("//tr[@id='LV_208_r1_c2']/input", "500")  # 单项金额
        self.Web_PO.jsNameReadonly("DATA_186")
        self.Web_PO.inputXpath("//input[@name='DATA_186']",varFromDate)  # 预计核销日期


        self.Web_PO.inputXpath("//table[@id='LV_208']/tbody/tr[2]/td[3]/input", "10")  # 数量
        self.Web_PO.inputXpath("//table[@id='LV_208']/tbody/tr[2]/td[4]/input", varFromDate)  # 期望到货时间
        self.Web_PO.inputXpath("//table[@id='LV_208']/tbody/tr[2]/td[5]/input", "50001")  # 预计总价
        self.Web_PO.inputXpath("//table[@id='LV_208']/tbody/tr[2]/td[6]/input", "HP")  # 准购厂商
        self.Web_PO.inputXpath("//table[@id='LV_208']/tbody/tr[2]/td[7]/input", "PIM项目")  # 项目名称
        self.Web_PO.inputXpath("//textarea[@name='DATA_328']", "HP123")  # 规格要求
        self.Web_PO.inputXpath("//textarea[@name='DATA_322']", "扩容需要")  # 申请购买理由
        self.Web_PO.inputXpath("//td[@id='LV_323_r1_c1']/input", "hp专卖店")  # 厂商1
        self.Web_PO.inputXpath("//td[@id='LV_323_r1_c2']/input", "hp")  # 厂牌2
        self.Web_PO.inputXpath("//td[@id='LV_323_r1_c3']/input", "50521456")  # 联系方式1
        self.Web_PO.inputXpath("//td[@id='LV_323_r1_c4']/input", "5000")  # 单价1
        self.Web_PO.inputXpath("//td[@id='LV_323_r1_c5']/input", "50000")  # 总价1
        self.Web_PO.inputXpath("//td[@id='LV_323_r2_c1']/input", "IBM直营店")  # 厂商2
        self.Web_PO.inputXpath("//td[@id='LV_323_r2_c2']/input", "IBM")  # 厂牌2
        self.Web_PO.inputXpath("//td[@id='LV_323_r2_c3']/input", "13816109050")  # 联系方式2
        self.Web_PO.inputXpath("//td[@id='LV_323_r2_c4']/input", "5001")  # 单价2
        self.Web_PO.inputXpath("//td[@id='LV_323_r2_c5']/input", "50010")  # 总价2
        self.Web_PO.inputXpath("//td[@id='LV_323_r3_c1']/input", "taobao网点")  # 厂商3
        self.Web_PO.inputXpath("//td[@id='LV_323_r3_c2']/input", "taobao")  # 厂牌3
        self.Web_PO.inputXpath("//td[@id='LV_323_r3_c3']/input", "58771632")  # 联系方式3
        self.Web_PO.inputXpath("//td[@id='LV_323_r3_c4']/input", "5002")  # 单价3
        self.Web_PO.inputXpath("//td[@id='LV_323_r3_c5']/input", "50020")  # 总价3
        self.Web_PO.iframeSwitch(1)
        self.Web_PO.clickId("next", 2)  # 提交
        self.Web_PO.clickId("work_run_submit", 2)  # 确定
        self.Web_PO.iframeQuit(1)
        self.Web_PO.quitURL()
        Color_PO.consoleColor("31", "36", varUser + "，" + varApplicationName + "（" + str(varNo) + "）" + "- - " * 10, "")
        print(varSerial + "申请 已提交")
        return varNo



    '''请假申请流程'''
    def askOffFlow(self, excelFile, varApplicationName, i, varUser, varLeader, varPersonnel, varVicepresident, varPresident, varDay):
        if varDay < 3 :
            varNo = self.askOffApply("1/4, ", varApplicationName, varUser, 1, Time_PO.getDatetimeEditHour(0),Time_PO.getDatetimeEditHour(24), str(varDay))
            self.askOffAudit("2/4, ", varApplicationName, varNo, "部门领导", varLeader, "同意", "批准")
            self.askOffAudit("3/4, ", varApplicationName, varNo, "人事总监", varPersonnel, "同意", "好的")
            self.askOffAudit("4/4, ", varApplicationName, varNo, "副总", varVicepresident, "同意", "谢谢")
            Excel_PO.writeXlsx(excelFile, varApplicationName, i, 7, str(self.askOffDone(varNo, varUser, varDay)))
        else:
            varNo = self.askOffApply("1/5, ", varApplicationName, varUser, 1, Time_PO.getDatetimeEditHour(0),Time_PO.getDatetimeEditHour(24), str(varDay))
            self.askOffAudit("2/5, ", varApplicationName, varNo, "部门领导", varLeader, "同意", "批准")
            self.askOffAudit("3/5, ", varApplicationName, varNo, "人事总监", varPersonnel, "同意", "好的")
            self.askOffAudit("4/5, ", varApplicationName, varNo, "副总", varVicepresident, "同意", "谢谢")
            self.askOffAudit("5/5, ", varApplicationName, varNo, "总经理", varPresident, "同意", "yuanyongtao批准")
            Excel_PO.writeXlsx(excelFile, varApplicationName, i, 8, str(self.askOffDone(varNo, varUser, varDay)))
    '''外出申请流程'''
    def egressionFlow(self, excelFile, varApplicationName, i, varUser, varLeader, varAdmin):
        varNo = self.egressionApply("1/4, ", varUser, Time_PO.getDatetimeEditHour(24), '医院领导', '上海宝山华亭路1000号交通大学复数医院', '驻场测试')
        self.egressionAudit("2/4, ", varNo, "部门领导", varLeader, "同意", "快去快回")
        self.egressionRevise("3/4, ", varNo, varUser, Time_PO.getDatetimeEditHour(48))
        self.egressionAudit("4/4, ", varNo, "行政", varAdmin, "确认", "谢谢")
        Excel_PO.writeXlsx(excelFile, varApplicationName, i, 5, "ok")
    '''出差申请流程'''
    def evectionFlow(self, excelFile, varApplicationName, i, varUser, varLeader, varVicepresident, varPersonnel, varfinancialAffairs, varDay):
        if varDay > 3:
            if varLeader == "wanglei01":
                varNo = self.evectionApply("1/4, ", varUser, "无", varDay, Time_PO.getDatetimeEditHour(12), Time_PO.getDatetimeEditHour(24), '上海', '北京', '飞机', '测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试1', 100)
                self.evectionAudit("2/4, ", varNo, "部门领导", varLeader, "同意", "快去快回")
                self.evectionAudit("3/4, ", varNo, "行政总监", varPersonnel, "确认", "谢谢")
                self.evectionAudit("4/4, ", varNo, "财务总监", varfinancialAffairs, "确认", "可预支费用！")
            else:
                varNo = self.evectionApply("1/5, ", varUser, "无", varDay, Time_PO.getDatetimeEditHour(12), Time_PO.getDatetimeEditHour(24), '上海', '北京', '飞机', '测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试1', 100)
                self.evectionAudit("2/5, ", varNo, "部门领导", varLeader, "同意", "快去快回")
                self.evectionAudit("3/5, ", varNo, "副总", varVicepresident, "同意", "注意安全")
                self.evectionAudit("4/5, ", varNo, "行政总监", varPersonnel, "确认", "谢谢")
                self.evectionAudit("5/5, ", varNo, "财务总监", varfinancialAffairs, "确认", "可预支费用！")
            Excel_PO.writeXlsx(excelFile, varApplicationName, i, 8, "ok")
        else:
            varNo = self.evectionApply("1/4, ", varUser, "无", varDay, Time_PO.getDatetimeEditHour(12), Time_PO.getDatetimeEditHour(24), '上海', '北京', '飞机', '测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试1', 100)
            self.evectionAudit("2/4, ", varNo, "部门领导", varLeader, "同意", "快去快回")
            self.evectionAudit("3/4, ", varNo, "行政总监", varPersonnel, "确认", "谢谢")
            self.evectionAudit("4/4, ", varNo, "财务总监", varfinancialAffairs, "确认", "可预支费用！")
            Excel_PO.writeXlsx(excelFile, varApplicationName, i, 7, "ok")

    # 申请单
    def application(self, varApplicationName, varStaffList, varDay):
        import time
        excelFile = File_PO.getLayerPath("../config") + "\\oa.xlsx"
        row, col = Excel_PO.getRowCol(excelFile, varApplicationName)
        for i in range(2, row + 1):
            if varApplicationName == "请假申请单":
                recordList = Excel_PO.getRowValue(excelFile, i, varApplicationName)
                if varStaffList == "所有人":
                    self.askOffFlow(excelFile, varApplicationName, i, recordList[1], recordList[2], recordList[3], recordList[4], recordList[5], varDay)
                elif varStaffList == "空" :
                    if varDay < 3 and recordList[6] == "":
                        self.askOffFlow(excelFile, varApplicationName, i, recordList[1], recordList[2], recordList[3],recordList[4], recordList[5], varDay)
                    elif varDay >= 3 and recordList[7] == "":
                        self.askOffFlow(excelFile, varApplicationName, i, recordList[1], recordList[2], recordList[3],recordList[4], recordList[5], varDay)
                elif recordList[1] in varStaffList:
                    self.askOffFlow(excelFile, varApplicationName, i, recordList[1], recordList[2], recordList[3], recordList[4], recordList[5], varDay)
            elif varApplicationName == "外出申请单":
                recordList = Excel_PO.getRowValue(excelFile, i, varApplicationName)
                if varStaffList == "所有人":
                    self.egressionFlow(excelFile, varApplicationName, i, recordList[1], recordList[2], recordList[3])
                elif varStaffList == "空" and recordList[4] == "":
                    self.egressionFlow(excelFile, varApplicationName, i, recordList[1], recordList[2], recordList[3])
                elif recordList[1] in varStaffList:
                    self.egressionFlow(excelFile, varApplicationName, i, recordList[1], recordList[2], recordList[3])
            elif varApplicationName == "出差申请单":
                recordList = Excel_PO.getRowValue(excelFile, i, varApplicationName)
                if varStaffList == "所有人":
                    self.evectionFlow(excelFile, varApplicationName, i, recordList[1], recordList[2], recordList[3], recordList[4], recordList[5], varDay)
                elif varStaffList == "空" :
                    if varDay > 3 and recordList[7] == "":
                        self.evectionFlow(excelFile, varApplicationName, i, recordList[1], recordList[2], recordList[3], recordList[4], recordList[5], varDay)
                    elif varDay <=3 and recordList[6] == "":
                        self.evectionFlow(excelFile, varApplicationName, i, recordList[1], recordList[2], recordList[3], recordList[4], recordList[5], varDay)
                elif recordList[1] in varStaffList:
                    self.evectionFlow(excelFile, varApplicationName, i, recordList[1], recordList[2], recordList[3], recordList[4], recordList[5], varDay)
            elif varApplicationName == "固定资产采购申请单":
                if varStaffList == "所有人":
                    recordList = Excel_PO.getRowValue(excelFile, i, varApplicationName)
                    time_start = time.time()
                    varNo = self.equipmentApply("1/7, ", varApplicationName, recordList[1], Time_PO.getDatetimeEditHour(12))
                    self.equipmentAudit("2/7, ", varNo, "部门领导", recordList[2], "同意", "快去快回")
                    self.equipmentAudit("3/7, ", varNo, "财务主管", recordList[3], "同意", "注意安全")
                    self.equipmentAudit("4/7, ", varNo, "财务经理", recordList[4], "同意", "谢谢")
                    self.equipmentAudit("5/7, ", varNo, "副总", recordList[5], "同意", "不客气")
                    self.equipmentAudit("6/7, ", varNo, "总经理", recordList[6], "同意", "批准了")
                    Excel_PO.writeXlsx(excelFile, varApplicationName, i, 8, self.equipmentDone("7/7, ", varNo, recordList[1]))
                    time_end = time.time()
                    time = time_end - time_start
                    Color_PO.consoleColor("31", "33", "耗时 " + str(round(time, 0)) + " 秒", "")
            elif varApplicationName == "借款申请单":
                if varStaffList == "所有人":
                    recordList = Excel_PO.getRowValue(excelFile, i, varApplicationName)
                    time_start = time.time()
                    varNo = self.equipmentApply("1/7, ", varApplicationName, recordList[1],Time_PO.getDatetimeEditHour(12))
                    self.equipmentAudit("2/7, ", varNo, "部门领导", recordList[2], "同意", "快去快回")
                    self.equipmentAudit("3/7, ", varNo, "财务主管", recordList[3], "同意", "注意安全")
                    self.equipmentAudit("4/7, ", varNo, "财务经理", recordList[4], "同意", "谢谢")
                    self.equipmentAudit("5/7, ", varNo, "副总", recordList[5], "同意", "不客气")
                    self.equipmentAudit("6/7, ", varNo, "总经理", recordList[6], "同意", "批准了")
                    Excel_PO.writeXlsx(excelFile, varApplicationName, i, 8, self.equipmentDone("7/7, ", varNo, recordList[1]))
                    time_end = time.time()
                    time = time_end - time_start
                    Color_PO.consoleColor("31", "33", "耗时 " + str(round(time, 0)) + " 秒", "")


        if platform.system() == 'Darwin':
            os.system("open " + File_PO.getLayerPath("../config") + "\\oa.xlsx")
        if platform.system() == 'Windows':
            os.system("start " + File_PO.getLayerPath("../config") + "\\oa.xlsx")



