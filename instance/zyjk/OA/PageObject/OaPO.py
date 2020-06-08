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

    '''打开浏览器'''
    def open(self):
        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(varURL)
        self.Web_PO.driver.maximize_window()  # 全屏
        # self.Web_PO.driver.set_window_size(1366,768)  # 按分辨率1366*768打开

    '''登录'''
    def login(self, varUser):
        self.Web_PO.inputId("name", varUser)
        self.Web_PO.clickXpath(u"//button[@id='submit']", 2)

    '''点击左侧菜单,选择模块'''
    def memu(self, varMemuName, varSubName):
        # # 获取菜单列表
        sleep(2)
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

    # # 检查 常用工作中表单数量。
    def getWorkQty(self):
        list1 = self.Web_PO.getXpathsText("//li")
        list2=[]
        for i in list1:
            if "快速新建" in i:
                list2.append(str(i).replace("快速新建\n", ""))
        print("工作流 - 新建工作 - 常用工作 :" + str(list2))
        # print(list2)


    '''申请'''
    def apply(self, varSerial, varUser, varModuleName, varType, varStartDate, varEndDate, varDay ):
        # self.Web_PO.apply(1, "jinhao", "工作流", "新建工作", "请假申请", 1, "2020-06-05 09:12:12", "2020-06-06 09:12:12", "2")  # 请假2天  <3
        # self.Web_PO.apply(1, "jinhao", "工作流", "新建工作", "请假申请", 1, "2020-06-05 09:12:12", "2020-06-06 09:12:12", "3")  # 请假3天  >=3

        self.open()
        self.login(varUser)  # 申请者
        self.memu("工作流", "新建工作")  # 选择菜单与模块

        # 检查 常用工作中表单数量
        self.Web_PO.iframeXpath("//iframe[@src='/general/workflow/new/']", 2)
        self.getWorkQty()

        # 请假申请单
        if varModuleName == "请假申请":
            self.Web_PO.clickXpathsContain("//button", "onclick", varModuleName, 2)
            self.Web_PO.iframeQuit(2)
            self.Web_PO.iframeId("tabs_w10000_iframe", 2)
            varNo = self.Web_PO.getXpathText("//div[@id='run_id_block']")  # 申请单编号，如 5666
            self.Web_PO.iframeId("work_form_data", 2)
            self.Web_PO.clickXpathsNum("//input[@type='radio']", varType, 2)  # 公休  请假类别，1=事假，2=调休，3=公休，4=病假，5=婚假，6=丧假，7=其他
            self.Web_PO.jsIdReadonly("DATA_4", 2)
            self.Web_PO.inputXpath("//input[@name='DATA_4']", varStartDate)  # 请假开始时间
            self.Web_PO.jsIdReadonly("DATA_5", 2)
            self.Web_PO.inputXpath("//input[@name='DATA_5']", varEndDate)  # 请假结束时间
            self.Web_PO.inputXpath("//input[@name='DATA_67']", varDay)  # 申请天数
            self.Web_PO.inputXpath("//textarea[@name='DATA_7']", varStartDate)  # 事由
            self.Web_PO.inputXpath("//textarea[@name='DATA_44']", varEndDate)  # 待变事项
            self.Web_PO.iframeSwitch(1)
            self.Web_PO.clickXpath("//input[@id='onekey_next']", 2)  # 提交
            self.Web_PO.alertAccept()
            self.Web_PO.iframeQuit(5)
            self.Web_PO.quitURL()

            print(str(varSerial) + varUser + " 请假申请" + str(varDay) + "天 已提交（流水号：" + str(varNo) + "）")
            return varNo

        elif varModuleName == "外出申请":
            pass
        elif varModuleName == "费用报销申请":
            pass
        elif varModuleName == "借款申请":
            pass


    '''审核'''
    def audit(self, varSerial, varNo, varRole, varAudit, varIsAgree, varOpinion):
        # Oa_PO.audit("2/6, ", varNo, "部门领导", "wanglei01", "同意", "部门领导批准")
        # 不同意 没写？

        self.open()
        self.login(varAudit)  # 审核者
        self.memu("工作流", "我的工作")  # 选择菜单与模块

        # # 选择流水号
        self.Web_PO.iframeXpath("//iframe[@src='/general/workflow/list/']", 2)  # 第一层
        self.Web_PO.iframeId("workflow-data-list", 2)  # 第二层
        varNoRow = self.Web_PO.getXpathsTextPlace("//table[@id='gridTable']/tbody/tr/td[3]/div", varNo)
        self.Web_PO.clickXpaths("//table[@id='gridTable']/tbody/tr[" + str(varNoRow + 1) + "]/td[8]/a", 2)

        # 请假申请单/费用报销申请单/借款申请单
        self.Web_PO.iframeSwitch(2)
        self.Web_PO.iframeId("workflow-form-frame", 2)  # 第二层
        self.Web_PO.iframeId("work_form_data", 2)  # 第三层
        varTitle = self.Web_PO.getXpathsText("//strong")
        if varTitle[0] == "请假申请单":
            if varRole == "部门领导":
                self.Web_PO.clickXpath("//input[@name='DATA_11' and @value='" + varIsAgree + "']", 2)  # 是否同意
                self.Web_PO.inputXpath("//textarea[@name='DATA_12']", varOpinion)  # 审批意见
                self.Web_PO.iframeSwitch(1)
                self.Web_PO.clickXpath("//input[@id='onekey_next']", 2)  # 提交
                self.Web_PO.alertAccept()
                self.Web_PO.iframeQuit(2)
                self.Web_PO.quitURL()
            elif varRole == "人事总监":
                self.Web_PO.clickXpath("//input[@name='DATA_14' and @value='" + varIsAgree + "']", 2)  # 是否同意
                self.Web_PO.inputXpath("//textarea[@name='DATA_15']", varOpinion)  # 审批意见
                self.Web_PO.iframeSwitch(1)
                self.Web_PO.clickXpath("//input[@id='onekey_next']", 2)  # 提交
                self.Web_PO.alertAccept()
                self.Web_PO.iframeQuit(2)
                self.Web_PO.quitURL()
            elif varRole == "副总":
                varDay = self.Web_PO.getXpathAttr("//input[@name='DATA_67']", "value")
                self.Web_PO.clickXpath("//input[@name='DATA_21' and @value='" + varIsAgree + "']", 2)  # 是否同意
                self.Web_PO.inputXpath("//textarea[@name='DATA_18']", varOpinion)  # 审批意见
                self.Web_PO.iframeSwitch(1)
                if int(varDay) >= 3:
                    self.Web_PO.clickXpath("//input[@id='onekey_next']", 2)  # 提交
                else:
                    self.Web_PO.clickXpath("//input[@id='handle_end']", 2)  # 提交
                    # self.Web_PO.alertAccept()
                self.Web_PO.alertAccept()
                self.Web_PO.iframeQuit(2)
                self.Web_PO.quitURL()
            elif varRole == "总经理":
                self.Web_PO.clickXpath("//input[@name='DATA_68' and @value='" + varIsAgree + "']", 2)  # 是否同意
                self.Web_PO.inputXpath("//textarea[@name='DATA_57']", varOpinion)  # 审批意见
                self.Web_PO.iframeSwitch(1)
                self.Web_PO.clickXpath("//input[@id='handle_end']", 2)  # 提交
                self.Web_PO.alertAccept()
                self.Web_PO.iframeQuit(2)
                self.Web_PO.quitURL()
            print(varSerial + varRole + " 已审批（流水号：" + str(varNo)+"）")

        elif varTitle[0] == "费用报销申请单":
            pass
        elif varTitle[0] == "借款申请单":
            pass

    '''回执查询'''
    def applyDone(self, varSerial, varNo, varUser):

        self.open()
        self.login(varUser)  # 申请人
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
        # print(number.strip(" "))  # 流水号：5597
        self.Web_PO.iframeId("print_frm", 2)
        list2 = self.Web_PO.getXpathsText("//td")
        list5 = self.List_PO.getSectionList(self.List_PO.getSectionList(list2, '审核信息', 'delbefore'), "流程开始（" + number.strip(" ") + "）", 'delafter')
        list6 = []
        for i in range(len(list5)):
            if i == 0:
                if self.Web_PO.isElementXpath("//input[@name='DATA_11' and @value='同意' and @checked]") == True:
                    list6.append("同意（副总）")
                elif self.Web_PO.isElementXpath("//input[@name='DATA_11' and @value='不同意' and @checked]") == True:
                    list6.append("不同意（副总）")
                else:
                    list6.append("未审核（副总）")
            elif i == 3:
                if self.Web_PO.isElementXpath("//input[@name='DATA_14' and @value='同意' and @checked]") == True:
                    list6.append("同意（人事总监）")
                elif self.Web_PO.isElementXpath("//input[@name='DATA_14' and @value='不同意' and @checked]") == True:
                    list6.append("不同意（人事总监）")
                else:
                    list6.append("未审核（人事总监）")
            elif i == 6:
                if self.Web_PO.isElementXpath("//input[@name='DATA_21' and @value='同意' and @checked]") == True:
                    list6.append("同意（副总）")
                elif self.Web_PO.isElementXpath("//input[@name='DATA_21' and @value='不同意' and @checked]") == True:
                    list6.append("不同意（副总）")
                else:
                    list6.append("未审核（副总）")
            elif i == 9:
                if self.Web_PO.isElementXpath("//input[@name='DATA_68' and @value='同意' and @checked]") == True:
                    list6.append("同意（总经理）")
                elif self.Web_PO.isElementXpath("//input[@name='DATA_68' and @value='不同意' and @checked]") == True:
                    list6.append("不同意（总经理）")
                else:
                    list6.append("未审核（总经理）")
            else:
                list6.append(list5[i])


        self.Web_PO.quitURL()
        print(varSerial + varUser + " 查看审核回执：")

        varArr = self.List_PO.listSplitArray(list6, 4)
        for i in range(len(varArr)):
            print(varArr[i])

