# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2018-3-15
# Description: 首营 对象库
#***************************************************************

import sys, os, platform
sys.path.append("..")
# from config.config import *
from zyjk.OA.web.config.config import *

class OvertimePO(object):

    def __init__(self, Level_PO):
         self.Level_PO = Level_PO

    '''1、登录'''
    def login(self, varUser):
        self.Level_PO.inputName("UNAME", varUser)
        self.Level_PO.clickXpath(u"//button[@id='submit']", 2)

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