# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-6-4
# Description: OA 对象库
# *****************************************************************

import os, sys
sys.path.append("..")

from config.config import *

import string, numpy
from string import digits
from PO.HtmlPO import *
from PO.ListPO import *
from PO.TimePO import *
from PO.ColorPO import *
from PO.LogPO import *
from PO.NetPO import *
from PO.DataPO import *
from PO.FilePO import *
from PO.StrPO import *
from PO.WebPO import *

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
        # self.Log_PO = LogPO(logFile, fmt='%(levelname)s - %(message)s - %(asctime)s')  # 输出日志

    '''打开浏览器'''
    def open(self, varURL):
        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(varURL)
        self.Web_PO.driver.maximize_window()  # 全屏
        # self.Web_PO.driver.set_window_size(1366,768)  # 按分辨率1366*768打开

    '''登录'''
    def login(self, varUser, varPass):
        self.Web_PO.inputId("name", varUser)
        self.Web_PO.inputId("password", varPass)
        self.Web_PO.clickXpath(u"//button[@id='submit']", 2)

    '''左侧菜单选择模块及浮层模块（无标题）'''
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
                for k in range(len(list4)):
                    if list4[k] == varSubName:
                        self.Web_PO.clickXpath("//ul[@id='first_menu']/li[" + str(j+1) + "]/div[2]/ul/li[" + str(k+1) + "]/a", 2)


    def memuERP(self, menu1, menu2):

        # 盛蕴ERP管理平台 之菜单树

        l_menu1 = self.Web_PO.getXpathsText("//li")
        l_menu1_tmp = self.List_PO.delRepeatElem(l_menu1)
        for i in range(len(l_menu1_tmp)):
            if menu1 in l_menu1_tmp[i]:
                self.Web_PO.clickXpath('//*[@id="app"]/section/section/aside/section/main/div/div[1]/div/ul/li[' + str(i + 1) + ']/div', 2)
                l_menu2_a = self.Web_PO.getXpathsText('//*[@id="app"]/section/section/aside/section/main/div/div[1]/div/ul/li[' + str(i + 1) + ']/ul/li/ul/a')
                # print(l_menu2_a)  # ['拜访分析报表', '会议分析表', '投入产出分析表', '协访分析表', '重点客户投入有效性分析', '开发计划总揽']
                for j in range(len(l_menu2_a)):
                    if menu2 == l_menu2_a[j]:
                        self.Web_PO.clickXpath('//*[@id="app"]/section/section/aside/section/main/div/div[1]/div/ul/li[' + str(i + 1) + ']/ul/li/ul/a[' + str(j + 1) + ']', 2)

        self.Web_PO.inputXpathClear('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/div[2]/div/div[1]/input', "1234测试")

    def maxBrowser(self, varWhichWindows):
        # 对当前browse全屏
        # Oa_Po.maxBrowser(1)
        self.Web_PO.switchLabel(varWhichWindows)
        self.Web_PO.driver.maximize_window()  # 全屏
        sleep(2)


    '''左侧菜单选择模块及浮层模块（有标题）'''
    def memu2(self, varMemuName, varSubName):
        # 标题，如人力资源模块中的薪酬管理标题
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
                for i in range(len(str(list3[0]).split("\n"))):
                    if str(list3[0]).split("\n")[i] != varMemuName and Str_PO.isContainChinese(str(list3[0]).split("\n")[i]) == True:
                        list4.append(str(list3[0]).split("\n")[i])
                for k in range(len(list4)):
                    if list4[k] == varSubName:
                        self.Web_PO.clickXpath("//ul[@id='first_menu']/li[" + str(j+1) + "]/div[2]/ul/li[1]/ul/li[" + str(k) + "]/a", 2)


    '''检查 常用工作中表单数量'''
    def getWorkQty(self):
        list1 = self.Web_PO.getXpathsText("//li")
        list2=[]
        for i in list1:
            if "快速新建" in i:
                list2.append(str(i).replace("快速新建\n", ""))
        print("工作流 - 新建工作 - 常用工作 :" + str(list2))
        # print(list2)


    '''项目立项'''
    def flowScheme(self, varTitle, l_content):

        self.open()
        if l_content[0] == "王磊":
            self.login(Char_PO.chinese2pinyin("wanglei01"))
        else:
            self.login(Char_PO.chinese2pinyin(l_content[0]))

        if varTitle == "项目基础信息":
            self.memu("工作流", "新建工作")
            self.Web_PO.iframeId("tabs_130_iframe", 2)
            self.Web_PO.clickLinktext("全部工作", 1)
            list1 = self.Web_PO.getXpathsText("//h4/span")
            for i in range(len(list1)):
                if "项目立项申请" in list1[i]:
                    self.Web_PO.clickXpath("//ul[@id='panel-inbox']/li[" + str(i + 1) + "]/div[2]", 1)
                    break
            self.Web_PO.iframeQuit(1)
            # 项目立项申请详情页
            self.Web_PO.iframeId("tabs_w10000_iframe", 1)
            varNo = self.Web_PO.getXpathText("//div[@id='run_id_block']")  # 获取当前项目的编号，如 No.7465
            self.Web_PO.iframeId("work_form_data", 2)
            self.Web_PO.inputXpath("//input[@name='DATA_2']", l_content[1])  # 项目名称
            self.Web_PO.inputXpath("//input[@name='DATA_121']", l_content[2])  # 启动日期
            self.Web_PO.inputXpath("//input[@name='DATA_122']", l_content[3])  # 预计完成
            self.Web_PO.iframeSwitch(1)
            self.Web_PO.clickId("next", 2)  # 提交
            # 弹框选择审核人
            self.Web_PO.clickId("chose_user2", 2)  # 选择人员
            self.Web_PO.switchBrowser(1)  # 切换到弹框浏览器
            self.Web_PO.iframeId("user", 1)
            d = self.Web_PO.getXpathsDictTextAttr(u"//td[@name='"+ l_content[4] + "']", u"id")
            self.Web_PO.clickId("opbox_" + d[l_content[4]], 2)  # 勾选主办人
            self.Web_PO.iframeSwitch(1)
            self.Web_PO.iframeId("control", 1)
            self.Web_PO.clickXpath("//input[@onclick='top.close();']", 1)  # 确定
            self.Web_PO.switchBrowser(0)  # 切回原浏览器
            self.Web_PO.iframeId("tabs_w10000_iframe", 1)
            self.Web_PO.clickId("work_run_submit", 2)  # 确定
            self.Web_PO.iframeQuit(2)
            self.Web_PO.quitURL()
            print("[done]，" + varTitle + "，项目名称：" + l_content[1] + "，发起人：" + l_content[0] + "，流水号：" + str(varNo))
            return varNo
        else:
            self.memu("工作流", "我的工作")
            # 选择流水号
            self.Web_PO.iframeXpath("//iframe[@src='/general/workflow/list/']", 2)  # 第一层
            self.Web_PO.iframeId("workflow-data-list", 2)  # 第二层
            varNoRow = self.Web_PO.getXpathsTextPlace("//table[@id='gridTable']/tbody/tr/td[3]/div", l_content[6])
            self.Web_PO.clickXpaths("//table[@id='gridTable']/tbody/tr[" + str(varNoRow + 1) + "]/td[8]/a", 2)
            self.Web_PO.iframeQuit(1)
            # 项目立项申请详情页
            self.Web_PO.iframeId("tabs_5_iframe", 1)
            self.Web_PO.iframeId("workflow-form-frame", 1)
            self.Web_PO.iframeId("work_form_data", 2)
            if varTitle == "需求分析":
                self.Web_PO.inputXpathClear("//input[@name='DATA_54']", l_content[1])  # 责任人
                self.Web_PO.inputXpathClear("//input[@name='DATA_55']", l_content[2])  # 时间节点
                self.Web_PO.inputXpathClear("//textarea[@name='DATA_128']", l_content[3])  # 产出结果文档
            elif varTitle == "产品调研":
                self.Web_PO.inputXpathClear("//input[@name='DATA_83']", l_content[1])  # 责任人
                self.Web_PO.inputXpathClear("//input[@name='DATA_66']", l_content[2])  # 时间节点
                self.Web_PO.inputXpathClear("//textarea[@name='DATA_132']", l_content[3])  # 产出结果文档
            elif varTitle == "竞品分析":
                self.Web_PO.inputXpathClear("//input[@name='DATA_72']", l_content[1])  # 责任人
                self.Web_PO.inputXpathClear("//input[@name='DATA_73']", l_content[2])  # 时间节点
                self.Web_PO.inputXpathClear("//textarea[@name='DATA_130']", l_content[3])  # 产出结果文档
            elif varTitle == "产品设计":
                self.Web_PO.inputXpathClear("//input[@name='DATA_78']", l_content[1])  # 责任人
                self.Web_PO.inputXpathClear("//input[@name='DATA_79']", l_content[2])  # 时间节点
                self.Web_PO.inputXpathClear("//textarea[@name='DATA_137']", l_content[3])  # 产出结果文档
            elif varTitle == "研发":
                self.Web_PO.inputXpathClear("//input[@name='DATA_92']", l_content[1])  # 责任人
                self.Web_PO.inputXpathClear("//input[@name='DATA_93']", l_content[2])  # 时间节点
                self.Web_PO.inputXpathClear("//textarea[@name='DATA_139']", l_content[3])  # 产出结果文档
            elif varTitle == "测试":
                self.Web_PO.inputXpathClear("//input[@name='DATA_100']", l_content[1])  # 责任人
                self.Web_PO.inputXpathClear("//input[@name='DATA_101']", l_content[2])  # 时间节点
                self.Web_PO.inputXpathClear("//textarea[@name='DATA_141']", l_content[3])  # 产出结果文档
            elif varTitle == "实施":
                self.Web_PO.inputXpathClear("//input[@name='DATA_104']", l_content[1])  # 责任人
                self.Web_PO.inputXpathClear("//input[@name='DATA_105']", l_content[2])  # 时间节点
                self.Web_PO.inputXpathClear("//textarea[@name='DATA_143']", l_content[3])  # 产出结果文档
            elif varTitle == "交付":
                self.Web_PO.inputXpath("//input[@name='DATA_109']", l_content[1])  # 责任人
                self.Web_PO.inputXpath("//input[@name='DATA_110']", l_content[2])  # 时间节点
                self.Web_PO.inputXpath("//textarea[@name='DATA_145']", l_content[3])  # 产出结果文档
            else:
                print("[errorrrrrrrrrr], " + varTitle)
                exit()
            self.Web_PO.iframeSwitch(1)
            if self.Web_PO.isElementXpath("//input[@id='onekey_next' and @type='button']") == True:
                self.Web_PO.clickXpath("//input[@id='onekey_next']", 2)  # 提交
                self.Web_PO.alertAccept()
            elif self.Web_PO.isElementXpath("//input[@id='next' and @type='button']") == True:
                self.Web_PO.clickId("next", 2)  # 提交
                self.Web_PO.clickId("work_run_submit", 2)  # 确定
            self.Web_PO.iframeQuit(2)
            self.Web_PO.quitURL()

            # 责任人 登录后直接提交
            self.open()
            self.login(Char_PO.chinese2pinyin(l_content[1]))

            self.memu("工作流", "我的工作")
            # 选择流水号
            self.Web_PO.iframeXpath("//iframe[@src='/general/workflow/list/']", 2)  # 第一层
            self.Web_PO.iframeId("workflow-data-list", 2)  # 第二层
            varNoRow = self.Web_PO.getXpathsTextPlace("//table[@id='gridTable']/tbody/tr/td[3]/div", l_content[6])
            self.Web_PO.clickXpaths("//table[@id='gridTable']/tbody/tr[" + str(varNoRow + 1) + "]/td[8]/a", 2)
            self.Web_PO.iframeQuit(1)
            # 项目立项申请详情页
            self.Web_PO.iframeId("tabs_5_iframe", 1)
            self.Web_PO.iframeId("workflow-form-frame", 1)
            self.Web_PO.clickId("onekey_next", 2)  # 提交
            self.Web_PO.alertAccept()
            self.Web_PO.iframeQuit(2)
            self.Web_PO.quitURL()

            # 审核人填写完成日期
            self.open()
            if l_content[5] == "李晨曦":
                self.login(Char_PO.chinese2pinyin(l_content[5]))

            else:
                if l_content[0] == "王磊":
                    self.login(Char_PO.chinese2pinyin("wanglei01"))
                else:
                    self.login(Char_PO.chinese2pinyin(l_content[0]))

            self.memu("工作流", "我的工作")
            # 选择流水号
            self.Web_PO.iframeXpath("//iframe[@src='/general/workflow/list/']", 2)  # 第一层
            self.Web_PO.iframeId("workflow-data-list", 2)  # 第二层
            varNoRow = self.Web_PO.getXpathsTextPlace("//table[@id='gridTable']/tbody/tr/td[3]/div", l_content[6])
            self.Web_PO.clickXpaths("//table[@id='gridTable']/tbody/tr[" + str(varNoRow + 1) + "]/td[8]/a", 2)
            self.Web_PO.iframeQuit(1)
            # 项目立项申请详情页
            self.Web_PO.iframeId("tabs_5_iframe", 1)
            self.Web_PO.iframeId("workflow-form-frame", 1)

            if varTitle == "交付":
                self.Web_PO.clickId("handle_end", 2)  # 提交
                self.Web_PO.alertAccept()
                self.Web_PO.iframeQuit(2)
                self.Web_PO.quitURL()
            else:
                self.Web_PO.clickId("next", 2)  # 提交
                # 弹框选择审核人
                if varTitle == "需求分析":
                    self.Web_PO.clickId("chose_user5", 2)  # 选择人员
                if varTitle == "产品调研":
                    self.Web_PO.clickId("chose_user8", 2)  # 选择人员
                if varTitle == "竞品分析":
                    self.Web_PO.clickId("chose_user11", 2)  # 选择人员
                if varTitle == "产品设计":
                    self.Web_PO.clickId("chose_user14", 2)  # 选择人员
                if varTitle == "研发":
                    self.Web_PO.clickId("chose_user17", 2)  # 选择人员
                if varTitle == "测试":
                    self.Web_PO.clickId("chose_user20", 2)  # 选择人员
                if varTitle == "实施":
                    self.Web_PO.clickId("chose_user23", 2)  # 选择人员

                self.Web_PO.switchBrowser(1)  # 切换到弹框浏览器
                self.Web_PO.iframeId("user", 1)
                d = self.Web_PO.getXpathsDictTextAttr(u"//td[@name='" + l_content[5] + "']", u"id")
                self.Web_PO.clickId("opbox_" + d[l_content[5]], 2)  # 勾选主办人
                self.Web_PO.iframeSwitch(1)
                self.Web_PO.iframeId("control", 1)
                self.Web_PO.clickXpath("//input[@onclick='top.close();']", 1)  # 确定
                self.Web_PO.switchBrowser(0)  # 切回原浏览器
                self.Web_PO.iframeId("tabs_5_iframe", 1)
                self.Web_PO.iframeId("workflow-form-frame", 1)
                self.Web_PO.clickId("work_run_submit", 2)  # 确定
                self.Web_PO.iframeQuit(2)
                self.Web_PO.quitURL()
            print("[done]，" + varTitle)




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
    def egressionApply(self, varSerial, varApplicationName, varUser, varOutDate, varToObject, varOutAddress, varOutReason ):
        self.open()
        self.login(Char_PO.chinese2pinyin1(varUser))
        self.memu("工作流", "新建工作")
        # 外出申请单页面
        self.Web_PO.iframeId("tabs_130_iframe", 2)
        self.Web_PO.clickLinktext("全部工作", 1)
        list1 = self.Web_PO.getXpathsText("//h4/span")
        for i in range(len(list1)):
            if varApplicationName in list1[i]:
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
        Color_PO.consoleColor("31", "33", "[" + varUser + "] " + varApplicationName + "（No." + str(varNo) + "）" + "- - " * 10, "")
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
    def evectionApply(self, varSerial, varApplicationName, varUser, varToFollow, varDay, varFromDate, varToDate, varFromCity, varToCity, varTraffic, varWork, varFee):
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
            if varApplicationName in list1[i]:
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
        Color_PO.consoleColor("31", "36", "[" + varUser + "] " + varApplicationName + str(varDay) + "天（No." + str(varNo) + "）" + "- - " * 10, "")
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



    '''借款申请单 - 申请'''
    def loanApply(self, varSerial, varApplicationName, varUser, varDescription, varMoney, varFromDate, varPay, varBankName, varCompany, varAccountName, varAccount,varProjectName, varRelatedApply):
        self.open()
        self.login(Char_PO.chinese2pinyin1(varUser))
        self.memu("工作流", "新建工作")
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
        self.Web_PO.inputXpath("//td[@id='LV_208_r1_c1']/textarea", varDescription)  # 情况说明
        self.Web_PO.inputXpath("//td[@id='LV_208_r1_c2']/input", varMoney)  # 单项金额
        self.Web_PO.jsNameReadonly("DATA_186")
        self.Web_PO.inputXpath("//input[@name='DATA_186']", varFromDate)  # 预计核销日期
        self.Web_PO.clickXpath("//input[@name='DATA_187' and @value='" + varPay + "']", 1)  # 付款方式
        self.Web_PO.inputXpath("//input[@name='DATA_188']", varBankName)  # 收款银行名称
        self.Web_PO.selectXpathText("//select[@name='DATA_277']", varCompany)  # 费用支付公司
        self.Web_PO.inputXpath("//input[@name='DATA_164']", varAccountName)  # 收款账户名称
        self.Web_PO.inputXpath("//input[@name='DATA_166']", varAccount)  # 收款账号
        self.Web_PO.inputXpath("//input[@name='DATA_319']", varProjectName)  # 项目名称
        self.Web_PO.selectXpathText("//select[@name='DATA_321']", varRelatedApply)  # 相关申请单
        self.Web_PO.iframeSwitch(1)
        if self.Web_PO.isElementXpath("//input[@id='onekey_next' and @type='button']") == True:
            self.Web_PO.clickXpath("//input[@id='onekey_next']", 2)  # 提交
            self.Web_PO.alertAccept()
        elif self.Web_PO.isElementXpath("//input[@id='next' and @type='button']") == True:
            self.Web_PO.clickId("next", 2)  # 提交
            self.Web_PO.clickId("work_run_submit", 2)  # 确定
        self.Web_PO.iframeQuit(1)
        self.Web_PO.quitURL()
        Color_PO.consoleColor("31", "36", "[" + varUser + "] " + varApplicationName + "（No." + str(varNo) + "）" + "- - " * 10, "")
        print(varSerial + "申请 已提交")
        return varNo

    '''借款申请单 - 审核'''
    def loanAudit(self, varSerial, varNo, varRole, varAudit, varIsAgree, varOpinion, varPresidentIsAgree, varAdminIsAgree, varCashier):
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
        elif varRole == "财务主管":
            self.Web_PO.inputXpath("//textarea[@name='DATA_115']", varOpinion)  # 审批意见
            self.Web_PO.clickXpath("//input[@name='DATA_211' and @value='" + varIsAgree + "']", 1)  # 同意/不同意
            self.Web_PO.locElement("//input[@name='DATA_313' and @value='" + varAdminIsAgree + "']")
            self.Web_PO.clickXpath("//input[@name='DATA_313' and @value='" + varAdminIsAgree + "']", 1)  # 行政审批 是/否
            self.Web_PO.clickXpath("//input[@name='DATA_227' and @value='" + varPresidentIsAgree + "']", 1)  # 总经理审批 是/否
            self.Web_PO.selectXpathText("//select[@name='DATA_230']", varCashier)  # 出纳人
            self.Web_PO.iframeSwitch(1)
            self.Web_PO.clickId("next", 1)  # 提交
            self.Web_PO.clickId("work_run_submit", 2)  # 确定
            self.Web_PO.iframeQuit(1)
            self.Web_PO.quitURL()
        elif varRole == "行政":
            self.Web_PO.inputXpath("//textarea[@name='DATA_314']", varOpinion)  # 审批意见
            self.Web_PO.clickXpath("//input[@name='DATA_316' and @value='" + varIsAgree + "']", 1)  # 同意/不同意
            self.Web_PO.iframeSwitch(1)
            self.Web_PO.clickId("next", 1)  # 提交
            self.Web_PO.clickId("work_run_submit", 2)  # 确定
            self.Web_PO.iframeQuit(1)
            self.Web_PO.quitURL()
        elif varRole == "财务经理":
            self.Web_PO.inputXpath("//textarea[@name='DATA_17']", varOpinion)  # 审批意见
            self.Web_PO.clickXpath("//input[@name='DATA_212' and @value='" + varIsAgree + "']", 1)  # 同意/不同意
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
            self.Web_PO.inputXpath("//textarea[@name='DATA_19']", varOpinion)  # 审批意见
            self.Web_PO.clickXpath("//input[@name='DATA_213' and @value='" + varIsAgree + "']", 1)  # 同意/不同意
            self.Web_PO.iframeSwitch(1)
            if self.Web_PO.isElementXpath("//input[@id='onekey_next' and @type='button']") == True:
                self.Web_PO.clickXpath("//input[@id='onekey_next']", 2)  # 提交
                self.Web_PO.alertAccept()
            elif self.Web_PO.isElementXpath("//input[@id='next' and @type='button']") == True:
                self.Web_PO.clickId("next", 2)  # 提交
                self.Web_PO.clickId("work_run_submit", 2)  # 确定
                # # 判断是否有弹框
                # if EC.alert_is_present()(self.Web_PO.driver):
                #     self.Web_PO.alertAccept()
            self.Web_PO.iframeQuit(1)
            self.Web_PO.quitURL()
        elif varRole == "总经理":
            self.Web_PO.inputXpath("//textarea[@name='DATA_21']", varOpinion)  # 审批意见
            self.Web_PO.clickXpath("//input[@name='DATA_214' and @value='" + varIsAgree + "']", 1)  # 同意/不同意
            self.Web_PO.iframeSwitch(1)
            self.Web_PO.clickId("next", 2)  # 提交
            self.Web_PO.clickId("work_run_submit", 2)  # 确定
            self.Web_PO.iframeQuit(1)
            self.Web_PO.quitURL()
        elif varRole == "出纳":
            self.Web_PO.locElement("//input[@name='DATA_216' and @value='" + varIsAgree + "']")
            self.Web_PO.clickXpath("//input[@name='DATA_216' and @value='" + varIsAgree + "']", 1)  # 同意/不同意
            self.Web_PO.iframeSwitch(1)
            self.Web_PO.clickId("handle_end", 1)  # 提交
            self.Web_PO.alertAccept()
            self.Web_PO.iframeQuit(1)
            self.Web_PO.quitURL()
        if varAudit == "wanglei01":
            varAudit = "王磊"
        if varAudit == "zangye":
            varAudit = "臧晔"
        print(varSerial + varRole + varAudit + " 已审批")



    '''付款申请单 - 申请'''
    def payApply(self, varSerial, varApplicationName, varUser, varSubject, varDescription, varMoney, varFromDate, varPay, varBankName, varCompany, varAccountName, varAccount,varProjectName, varRelatedApply, varContract):
        self.open()
        self.login(Char_PO.chinese2pinyin1(varUser))
        self.memu("工作流", "新建工作")
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
        self.Web_PO.selectXpathText("//td[@id='LV_208_r1_c1']/select", varSubject)  # 费用科目
        self.Web_PO.inputXpath("//td[@id='LV_208_r1_c2']/textarea", varDescription)  # 情况说明
        self.Web_PO.inputXpath("//td[@id='LV_208_r1_c3']/input", varMoney)  # 单项金额
        self.Web_PO.jsNameReadonly("DATA_186")
        self.Web_PO.inputXpath("//input[@name='DATA_186']", varFromDate)  # 预计核销日期
        self.Web_PO.clickXpath("//input[@name='DATA_187' and @value='" + varPay + "']", 1)  # 付款方式
        self.Web_PO.inputXpath("//input[@name='DATA_188']", varBankName)  # 收款银行名称
        self.Web_PO.selectXpathText("//select[@name='DATA_277']", varCompany)  # 费用支付公司
        self.Web_PO.inputXpath("//input[@name='DATA_164']", varAccountName)  # 收款账户名称
        self.Web_PO.inputXpath("//input[@name='DATA_166']", varAccount)  # 收款账号
        self.Web_PO.inputXpath("//input[@name='DATA_319']", varProjectName)  # 项目名称
        self.Web_PO.selectXpathText("//select[@name='DATA_321']", varRelatedApply)  # 相关申请单
        self.Web_PO.clickXpath("//input[@name='DATA_322' and @value='" + varContract + "']", 1)  # 合同
        self.Web_PO.iframeSwitch(1)
        if self.Web_PO.isElementXpath("//input[@id='onekey_next' and @type='button']") == True:
            self.Web_PO.clickXpath("//input[@id='onekey_next']", 2)  # 提交
            self.Web_PO.alertAccept()
        elif self.Web_PO.isElementXpath("//input[@id='next' and @type='button']") == True:
            self.Web_PO.clickId("next", 2)  # 提交
            self.Web_PO.clickId("work_run_submit", 2)  # 确定
        self.Web_PO.iframeQuit(1)
        self.Web_PO.quitURL()
        Color_PO.consoleColor("31", "36", "[" + varUser + "] " + varApplicationName + "（No." + str(varNo) + "）" + "- - " * 10, "")
        print(varSerial + "申请 已提交")
        return varNo

    '''付款申请单 - 审核'''
    def payAudit(self, varSerial, varNo, varRole, varAudit, varIsAgree, varOpinion, varPresidentIsAgree, varAdminIsAgree, varCashier):
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
        elif varRole == "财务主管":
            self.Web_PO.inputXpath("//textarea[@name='DATA_115']", varOpinion)  # 审批意见
            self.Web_PO.clickXpath("//input[@name='DATA_211' and @value='" + varIsAgree + "']", 1)  # 同意/不同意
            self.Web_PO.locElement("//input[@name='DATA_313' and @value='" + varAdminIsAgree + "']")
            self.Web_PO.clickXpath("//input[@name='DATA_313' and @value='" + varAdminIsAgree + "']", 1)  # 行政审批 是/否
            self.Web_PO.clickXpath("//input[@name='DATA_227' and @value='" + varPresidentIsAgree + "']", 1)  # 总经理审批 是/否
            self.Web_PO.selectXpathText("//select[@name='DATA_230']", varCashier)  # 出纳人
            self.Web_PO.iframeSwitch(1)
            self.Web_PO.clickId("next", 1)  # 提交
            self.Web_PO.clickId("work_run_submit", 2)  # 确定
            self.Web_PO.iframeQuit(1)
            self.Web_PO.quitURL()
        elif varRole == "行政":
            self.Web_PO.inputXpath("//textarea[@name='DATA_314']", varOpinion)  # 审批意见
            self.Web_PO.clickXpath("//input[@name='DATA_316' and @value='" + varIsAgree + "']", 1)  # 同意/不同意
            self.Web_PO.iframeSwitch(1)
            self.Web_PO.clickId("next", 1)  # 提交
            self.Web_PO.clickId("work_run_submit", 2)  # 确定
            self.Web_PO.iframeQuit(1)
            self.Web_PO.quitURL()
        elif varRole == "财务经理":
            self.Web_PO.inputXpath("//textarea[@name='DATA_17']", varOpinion)  # 审批意见
            self.Web_PO.clickXpath("//input[@name='DATA_212' and @value='" + varIsAgree + "']", 1)  # 同意/不同意
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
            self.Web_PO.inputXpath("//textarea[@name='DATA_19']", varOpinion)  # 审批意见
            self.Web_PO.clickXpath("//input[@name='DATA_213' and @value='" + varIsAgree + "']", 1)  # 同意/不同意
            self.Web_PO.iframeSwitch(1)
            if self.Web_PO.isElementXpath("//input[@id='onekey_next' and @type='button']") == True:
                self.Web_PO.clickXpath("//input[@id='onekey_next']", 2)  # 提交
                self.Web_PO.alertAccept()
            elif self.Web_PO.isElementXpath("//input[@id='next' and @type='button']") == True:
                self.Web_PO.clickId("next", 2)  # 提交
                self.Web_PO.clickId("work_run_submit", 2)  # 确定
                # # 判断是否有弹框
                # if EC.alert_is_present()(self.Web_PO.driver):
                #     self.Web_PO.alertAccept()
            self.Web_PO.iframeQuit(1)
            self.Web_PO.quitURL()
        elif varRole == "总经理":
            self.Web_PO.inputXpath("//textarea[@name='DATA_21']", varOpinion)  # 审批意见
            self.Web_PO.clickXpath("//input[@name='DATA_214' and @value='" + varIsAgree + "']", 1)  # 同意/不同意
            self.Web_PO.iframeSwitch(1)
            self.Web_PO.clickId("next", 2)  # 提交
            self.Web_PO.clickId("work_run_submit", 2)  # 确定
            self.Web_PO.iframeQuit(1)
            self.Web_PO.quitURL()
        elif varRole == "出纳":
            self.Web_PO.locElement("//input[@name='DATA_216' and @value='" + varIsAgree + "']")
            self.Web_PO.clickXpath("//input[@name='DATA_216' and @value='" + varIsAgree + "']", 1)  # 同意/不同意
            self.Web_PO.iframeSwitch(1)
            self.Web_PO.clickId("handle_end", 1)  # 提交
            self.Web_PO.alertAccept()
            self.Web_PO.iframeQuit(1)
            self.Web_PO.quitURL()
        if varAudit == "wanglei01":
            varAudit = "王磊"
        if varAudit == "zangye":
            varAudit = "臧晔"
        print(varSerial + varRole + varAudit + " 已审批")



    '''固定资产采购 - 申请'''
    def equipmentApply(self, varSerial, varApplicationName, varUser, varCompany):
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
        self.Web_PO.inputXpath("//table[@id='LV_208']/tbody/tr[2]/td[4]/input", Time_PO.getDatetimeEditHour(12))  # 期望到货时间
        self.Web_PO.inputXpath("//table[@id='LV_208']/tbody/tr[2]/td[5]/input", "50001")  # 预计总价
        self.Web_PO.inputXpath("//table[@id='LV_208']/tbody/tr[2]/td[6]/input", "HP")  # 准购厂商
        self.Web_PO.inputXpath("//table[@id='LV_208']/tbody/tr[2]/td[7]/input", "PIM项目")  # 项目名称

        self.Web_PO.selectXpathText("//select[@name='DATA_1003']", varCompany)

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
        Color_PO.consoleColor("31", "36", "[" + varUser + "] " + varApplicationName + "（No." + str(varNo) + "）" + "- - " * 10, "")

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
        varNo = self.egressionApply("1/4, ", varApplicationName, varUser, Time_PO.getDatetimeEditHour(24), '医院领导', '上海宝山华亭路1000号交通大学复数医院', '驻场测试')
        self.egressionAudit("2/4, ", varNo, "部门领导", varLeader, "同意", "快去快回")
        self.egressionRevise("3/4, ", varNo, varUser, Time_PO.getDatetimeEditHour(48))
        self.egressionAudit("4/4, ", varNo, "行政", varAdmin, "确认", "谢谢")
        Excel_PO.writeXlsx(excelFile, varApplicationName, i, 5, "ok")
    '''出差申请流程'''
    def evectionFlow(self, excelFile, varApplicationName, i, varUser, varLeader, varVicepresident, varPersonnel, varfinancialAffairs, varDay):
        if varDay > 3:
            if varLeader == "wanglei01":
                varNo = self.evectionApply("1/4, ", varApplicationName, varUser, "无", varDay, Time_PO.getDatetimeEditHour(12), Time_PO.getDatetimeEditHour(24), '上海', '北京', '飞机', '测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试1', 100)
                self.evectionAudit("2/4, ", varNo, "部门领导", varLeader, "同意", "快去快回")
                self.evectionAudit("3/4, ", varNo, "行政总监", varPersonnel, "确认", "谢谢")
                self.evectionAudit("4/4, ", varNo, "财务总监", varfinancialAffairs, "确认", "可预支费用！")
            else:
                varNo = self.evectionApply("1/5, ", varApplicationName, varUser, "无", varDay, Time_PO.getDatetimeEditHour(12), Time_PO.getDatetimeEditHour(24), '上海', '北京', '飞机', '测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试1', 100)
                self.evectionAudit("2/5, ", varNo, "部门领导", varLeader, "同意", "快去快回")
                self.evectionAudit("3/5, ", varNo, "副总", varVicepresident, "同意", "注意安全")
                self.evectionAudit("4/5, ", varNo, "行政总监", varPersonnel, "确认", "谢谢")
                self.evectionAudit("5/5, ", varNo, "财务总监", varfinancialAffairs, "确认", "可预支费用！")
            Excel_PO.writeXlsx(excelFile, varApplicationName, i, 8, "ok")
        else:
            varNo = self.evectionApply("1/4, ", varApplicationName, varUser, "无", varDay, Time_PO.getDatetimeEditHour(12), Time_PO.getDatetimeEditHour(24), '上海', '北京', '飞机', '测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试1', 100)
            self.evectionAudit("2/4, ", varNo, "部门领导", varLeader, "同意", "快去快回")
            self.evectionAudit("3/4, ", varNo, "行政总监", varPersonnel, "确认", "谢谢")
            self.evectionAudit("4/4, ", varNo, "财务总监", varfinancialAffairs, "确认", "可预支费用！")
            Excel_PO.writeXlsx(excelFile, varApplicationName, i, 7, "ok")
    '''借款申请流程'''
    def loanFlow(self, excelFile, varApplicationName, i, varUser, varLeader, varFinanceOfficer, varAdmin, varFinanceManager, varVicepresident, varPresident, varCashier):
        if varLeader == "wanglei01":
            varNo = self.loanApply("1/6, ", varApplicationName, varUser, "路途费用", "500", str(Time_PO.getBeforeAfterDate(Time_PO.getDate_minus(), 2)), "现金", '上海银行', '上海智赢健康科技有限公司', 'jinhao','6220115210231025', '电子健康档案', '无')
            self.loanAudit("2/6, ", varNo, "财务主管", varFinanceOfficer, "同意", "财务主管点评", "是", "是", varCashier)
            self.loanAudit("3/6, ", varNo, "行政", varAdmin, "同意", "yanlibei点评", "", "", "")
            self.loanAudit("3/6, ", varNo, "财务经理", varFinanceManager, "同意", "zangye点评", "", "", "")
            self.loanAudit("4/6, ", varNo, "副总", varVicepresident, "同意", "wanglei点评", "", "", "")
            self.loanAudit("5/6, ", varNo, "总经理", varPresident, "同意", "yuanyongtao点评", "", "", "")
            self.loanAudit("6/6, ", varNo, "出纳", varCashier, "同意", "", "", "", "")
        else:
            varNo = self.loanApply("1/8, ", varApplicationName, varUser, "路途费用", "500", str(Time_PO.getBeforeAfterDate(Time_PO.getDate_minus(), 2)), "现金", '上海银行', '上海智赢健康科技有限公司', 'jinhao','6220115210231025', '电子健康档案', '无')
            self.loanAudit("2/8, ", varNo, "部门领导", varLeader, "同意", "部门领导点评", "", "", "")
            self.loanAudit("3/8, ", varNo, "财务主管", varFinanceOfficer, "同意", "财务主管点评", "是", "是", varCashier)
            self.loanAudit("4/8, ", varNo, "行政", varAdmin, "同意", "yanlibei点评", "", "", "")
            self.loanAudit("5/8, ", varNo, "财务经理", varFinanceManager, "同意", "zangye点评", "", "", "")
            self.loanAudit("6/8, ", varNo, "副总", varVicepresident, "同意", "wanglei点评", "", "", "")
            self.loanAudit("7/8, ", varNo, "总经理", varPresident, "同意", "yuanyongtao点评", "", "", "")
            self.loanAudit("8/8, ", varNo, "出纳", varCashier, "同意", "", "", "", "")
        Excel_PO.writeXlsx(excelFile, varApplicationName, i, 10, "ok")
    '''付款申请流程'''
    def payFlow(self, excelFile, varApplicationName, i, varUser, varLeader, varFinanceOfficer, varAdmin, varFinanceManager, varVicepresident, varPresident, varCashier):
        if varLeader == "wanglei01":
            varNo = self.payApply("1/6, ", varApplicationName, varUser, "租赁费", "2019办公场地", "500", str(Time_PO.getBeforeAfterDate(Time_PO.getDate_minus(), 2)), "现金", '上海银行', '上海智赢健康科技有限公司', 'jinhao', '6220115210231025', '电子健康档案', '无',"有")
            self.payAudit("2/6, ", varNo, "财务主管", varFinanceOfficer, "同意", "财务主管点评", "是", "是", varCashier)
            self.payAudit("3/6, ", varNo, "行政", varAdmin, "同意", "yanlibei点评", "", "", "")
            self.payAudit("3/6, ", varNo, "财务经理", varFinanceManager, "同意", "zangye点评", "", "", "")
            self.payAudit("4/6, ", varNo, "副总", varVicepresident, "同意", "wanglei点评", "", "", "")
            self.payAudit("5/6, ", varNo, "总经理", varPresident, "同意", "yuanyongtao点评", "", "", "")
            self.payAudit("6/6, ", varNo, "出纳", varCashier, "同意", "", "", "", "")
        else:
            varNo = self.payApply("1/8, ", varApplicationName, varUser, "租赁费", "2019办公场地", "500", str(Time_PO.getBeforeAfterDate(Time_PO.getDate_minus(), 2)), "现金", '上海银行', '上海智赢健康科技有限公司', 'jinhao', '6220115210231025', '电子健康档案', '无',"有")
            self.payAudit("2/8, ", varNo, "部门领导", varLeader, "同意", "部门领导点评", "", "", "")
            self.payAudit("3/8, ", varNo, "财务主管", varFinanceOfficer, "同意", "财务主管点评", "是", "是", varCashier)
            self.payAudit("4/8, ", varNo, "行政", varAdmin, "同意", "yanlibei点评", "", "", "")
            self.payAudit("5/8, ", varNo, "财务经理", varFinanceManager, "同意", "zangye点评", "", "", "")
            self.payAudit("6/8, ", varNo, "副总", varVicepresident, "同意", "wanglei点评", "", "", "")
            self.payAudit("7/8, ", varNo, "总经理", varPresident, "同意", "yuanyongtao点评", "", "", "")
            self.payAudit("8/8, ", varNo, "出纳", varCashier, "同意", "", "", "", "")
        Excel_PO.writeXlsx(excelFile, varApplicationName, i, 10, "ok")
    '''固定资产申请流程'''
    def equipmentFlow(self, excelFile, varApplicationName, i, varUser, varLeader, varVicepresident, varPresident, varCompany):
        if varLeader == "wanglei01":
            varNo = self.equipmentApply("1/3, ", varApplicationName, varUser, varCompany)
            self.equipmentAudit("2/3, ", varNo, "副总", varVicepresident, "同意", "副总点评")
            self.equipmentAudit("3/3, ", varNo, "总经理", varPresident, "同意", "总经理点评")
        else:
            varNo = self.equipmentApply("1/4, ", varApplicationName, varUser, varCompany)
            self.equipmentAudit("2/4, ", varNo, "部门领导", varLeader, "同意", "部门领导点评")
            self.equipmentAudit("3/4, ", varNo, "副总", varVicepresident, "同意", "副总点评")
            self.equipmentAudit("4/4, ", varNo, "总经理", varPresident, "同意", "总经理点评")
        Excel_PO.writeXlsx(excelFile, varApplicationName, i, 7, "ok")


    # 申请单
    def application(self, varApplicationName, varStaffList, varDay=0):
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
            elif varApplicationName == "借款申请单":
                recordList = Excel_PO.getRowValue(excelFile, i, varApplicationName)
                import time
                time_start = time.time()
                if varStaffList == "所有人":
                    self.loanFlow(excelFile, varApplicationName, i,  recordList[1], recordList[2], recordList[3], recordList[4], recordList[5], recordList[6], recordList[7], recordList[8])
                elif varStaffList == "空" and recordList[9] == "":
                    self.loanFlow(excelFile, varApplicationName, i,  recordList[1], recordList[2], recordList[3], recordList[4], recordList[5], recordList[6], recordList[7], recordList[8])
                elif recordList[1] in varStaffList:
                    self.loanFlow(excelFile, varApplicationName, i,  recordList[1], recordList[2], recordList[3], recordList[4], recordList[5], recordList[6], recordList[7], recordList[8])
                time_end = time.time()
                time = time_end - time_start
                Color_PO.consoleColor("31", "33", "耗时 " + str(round(time, 0)) + " 秒", "")
            elif varApplicationName == "付款申请单":
                recordList = Excel_PO.getRowValue(excelFile, i, varApplicationName)
                import time
                time_start = time.time()
                if varStaffList == "所有人":
                    self.payFlow(excelFile, varApplicationName, i,  recordList[1], recordList[2], recordList[3], recordList[4], recordList[5], recordList[6], recordList[7], recordList[8])
                elif varStaffList == "空" and recordList[9] == "":
                    self.payFlow(excelFile, varApplicationName, i,  recordList[1], recordList[2], recordList[3], recordList[4], recordList[5], recordList[6], recordList[7], recordList[8])
                elif recordList[1] in varStaffList:
                    self.payFlow(excelFile, varApplicationName, i,  recordList[1], recordList[2], recordList[3], recordList[4], recordList[5], recordList[6], recordList[7], recordList[8])
                time_end = time.time()
                time = time_end - time_start
                Color_PO.consoleColor("31", "33", "耗时 " + str(round(time, 0)) + " 秒", "")
            elif varApplicationName == "项目设备采购申请单":
                recordList = Excel_PO.getRowValue(excelFile, i, varApplicationName)
                if varStaffList == "所有人":
                    self.equipmentFlow(excelFile, varApplicationName, i,  recordList[1], recordList[2], recordList[3], recordList[4], recordList[5])
                elif varStaffList == "空" and recordList[6] == "":
                    self.equipmentFlow(excelFile, varApplicationName, i, recordList[1], recordList[2], recordList[3],recordList[4], recordList[5])
                elif recordList[1] in varStaffList:
                    self.equipmentFlow(excelFile, varApplicationName, i, recordList[1], recordList[2], recordList[3],recordList[4], recordList[5])



        if platform.system() == 'Darwin':
            os.system("open " + File_PO.getLayerPath("../config") + "\\oa.xlsx")
        if platform.system() == 'Windows':
            os.system("start " + File_PO.getLayerPath("../config") + "\\oa.xlsx")


if __name__ == '__main__':

    Oa_Po = OaPO()

    Oa_Po.open("http://192.168.0.65")
    Oa_Po.login("liuting", "")
    Oa_Po.memu("盛蕴ERP", "盛蕴ERP（演示）")
    Oa_Po.maxBrowser(1)
    # Oa_Po.memuERP("统计报表", "会议分析表")
    Oa_Po.memuERP("统计报表", "开发计划总揽")

    x = Oa_Po.Web_PO.getXpathsText("//tr")
    print(x)






