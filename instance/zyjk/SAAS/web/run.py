# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description: android自动化测试框架
#***************************************************************


import os, sys, unittest, xlwt, xlrd, MySQLdb, tempfile,shutil,chardet,random,webbrowser,platform,string,datetime,numpy
from xlutils.copy import copy
from email.mime.multipart import *
import mimetypes
import email
import subprocess,re
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
import base64
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import smtplib,pytesseract
from PIL import Image
from email.mime.text import MIMEText
from email.header import Header
from time import sleep
from xlwt.Style import *
from xlrd import open_workbook

from PIL import Image

#from jhj_v1_5_setup import *
#win32api,win32con,HTMLTestRunner
# import HTMLTestRunner

from pymongo import MongoClient
# from CJLinterfaceDriver import *
# from ssh_cmd import *
from requests.adapters import HTTPAdapter
from time import sleep

from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from PO.listPO import *

from instance.zyjk.SAAS.PageObject.SaasPO import *

class Run(unittest.TestCase):

    def runTest(self):
        pass

    @classmethod
    def setUpClass(self):
        self.Level_PO = Level_PO
        self.varExcel = os.path.abspath(r"web.xls")
        self.varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 获取当天日期时间,格式：20161020130318
        bk = xlrd.open_workbook(varExcel, formatting_info=True)
        self.newbk = copy(bk)
        self.sheetMain = bk.sheet_by_name("main")
        self.sheetTestCase = bk.sheet_by_name("testcase")
        self.styleRed = xlwt.easyxf('font: name Times New Roman, color-index red')
        self.styleBlue = xlwt.easyxf('font: name Times New Roman, color-index blue')
        self.styleGray25 = xlwt.easyxf('font: name Times New Roman, color-index gray25')

    @classmethod
    def tearDownClass(self):
        pass

    def test_Main(self):
        for i in range(1, self.sheetMain.nrows):
            if sheetMain.cell_value(i, 0) == "Y":
                self.mainModule = sheetMain.cell_value(i, 1)
                self.readTestcase()

    def readTestcase(self):
        # 遍历TestCase及调用函数模块,定位测试用例位置及数量
        caseEnd = 0
        caseFrom = 0
        for j in range(1, sheetTestCase.nrows):  # 遍历所有记录
            if sheetTestCase.cell_value(j, 2) == self.mainModule:  # 判断 module = 登录 的编号
                caseFrom = j
                break
        # print("caseFrom:" + str(caseFrom))

        for j in range(caseFrom + 1, sheetTestCase.nrows):  # 遍历从编号为登录记录到结尾的记录
            if j > sheetTestCase.nrows:
                caseEnd = j
            elif sheetTestCase.cell_value(j, 2) != "" :
                caseEnd = j
                break
        print("\ncase:" + str(caseFrom) + " - " + str(caseEnd-1))

        # 遍历 module的case
        newWs = newbk.get_sheet(1)
        for l in range(caseFrom, caseEnd):
            try :
                if sheetTestCase.cell_value(l, 1) == "N" or sheetTestCase.cell_value(l, 4) == "":
                    pass
                else:
                    exec(sheetTestCase.cell_value(l, 4))
                    newWs.write(l, 0, varTimeYMDHSM, styleBlue)
            except:
                print("[Errorrrrrrr] Excel("+str(l+1)+") , " + str(sheetTestCase.cell_value(caseFrom, 2)) + " , " + str(sheetTestCase.cell_value(l, 3)) + " , " + str(sheetTestCase.cell_value(l, 4)))
                newWs.write(l, 0, varTimeYMDHSM, styleRed)
        newbk.save(varExcel)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def login(self):

        ''' 登录 '''

        self.Level_PO.inputXpath("//input[@type='text']", "admin")
        self.Level_PO.inputXpath("//input[@type='password']", dimPassword)
        self.Level_PO.clickXpath("//button[@type='button']", 2)


    def qcAnalysis_optRuleType(self, varExcelNum, *varRules):

        # 档案数据质控分析
        # 查询档案，操作问题档案
        Level_PO.clickXpath("//input[@placeholder='请选择']", 2)  # 定位第一下拉框
        #
        # x= Level_PO.getXpathsText("//li/span")
        # for i in range(len(x)):
        #     if "-" not in x[i]:
        #         x.pop(0)
        # print(x)

        Level_PO.clickXpath("//body/div[@class='el-select-dropdown el-popper is-multiple']/div[1]/div[1]/ul/li[1]", 2)  # 选择第1个  li[1]
        Level_PO.clickXpath("//button[@class='el-button el-button--primary']", 2)  # 查找
        Level_PO.clickXpath("//button[@class='el-button el-button--text el-button--small']", 2)  # 操作详情
        # 问题档案列表之 规则类型勾选
        for i in range(len(varRules)):
            Level_PO.clickXpathsNum("//span[@aria-checked='mixed']", varRules[i], 2)  # 勾选第？个
        sleep(4)

        # 勾选规则后，页面自动匹配显示符合条件的问题档案列表，并点击第一条记录
        l_data = Level_PO.getXpathsText("//div[@class='tableTemplate']/div[2]/div[1]/div/div/div/div/div/div")
        x = int(len(l_data) / 9)
        l_record = numpy.array_split(l_data, x)
        l_title = ['操作:', '档案编号:', '姓名:', '社区医院:', '表单名称:', '字段名称:', '规则类型:', '错误描述:']
        l_merge = [i + j for i, j in zip(l_title, l_record[0])]
        # print(l_merge)
        c = list_PO.alignmentKey(l_merge, ":")
        newWs = newbk.get_sheet(1)
        newWs.write(varExcelNum, 5, c, styleBlue)
        newbk.save(varExcel)

        Level_PO.clickXpathsNum("//div[@class='tableTemplate']/div[2]/div[1]/div/div/div/div/div/div", 1, 2)  # 点击 第一条记录
        # Level_PO.clickXpathsNum("//div[@class='tableTemplate']/div[2]/div[1]/div/div/div/div/div/div", 10, 2)  #  点击 第二条记录
        # Level_PO.clickXpathsNum("//div[@class='tableTemplate']/div[2]/div[1]/div/div/div/div/div/div", 19, 2)  # 点击 第三条记录

    def qcAnalysis_cover(self, varExcelNum):
        print("【健康档案封面】")
        Level_PO.clickId("tab-0", 2)  # 健康档案封面
        l_data = Level_PO.getXpathsText("//div[@id='pane-0']/div/div/div/div[1]/div/div/div")
        l_data.pop(0)
        c = list_PO.alignmentKey(l_data, ":\n")  # 将记录信息保存到excel
        newWs = newbk.get_sheet(1)
        newWs.write(varExcelNum, 5, c, styleBlue)
        newbk.save(varExcel)

    def qcAnalysis_person(self, varExcelNum, varTitle, varSplit):
        print(varTitle)
        l_data = []
        c = []
        Level_PO.clickId("tab-1", 2)  # 个人基本信息表
        l_data = Level_PO.getXpathsText("//div[@id='pane-1']/div/div/div/div[1]/div/div/div")
        l_data.pop(0)
        if varTitle == "\n【个人基本信息表 - 生活环境】":
            c = list_PO.alignmentKey(l_data, ":\n")
        else:
            # 合并
            l_temp = []
            for i in range(0, len(l_data)):
                if varSplit != l_data[i]:
                    l_temp.append(l_data[i])
                else:
                    for j in range(i):
                        l_data.pop(0)
                    l_data.pop(0)
                    break
            l_temp.pop()
            if varSplit == "家族史" or varSplit == "遗传病史" or varSplit == "残疾情况" or varSplit == "生活环境" or varSplit == "反面":
                c = list_PO.alignmentKey(l_temp, ":\n")
            else:
                l_temp = list_PO.elementMerge(l_temp, 3)
                c = list_PO.alignmentKey(l_temp, ":")
        newWs = newbk.get_sheet(1)
        newWs.write(varExcelNum, 5, c, styleBlue)
        newbk.save(varExcel)

    def qcAnalysis_arichive(self ,varExcelNum):
        print("【档案信息卡 - 正面反面】")
        Level_PO.clickId("tab-3", 2)  # 档案信息卡
        list1 = Level_PO.getXpathsText("//div[@id='pane-3']/form/div/div[1]/div/div/div")
        l11 = []
        l22 = []
        l33 = []
        for i in range(len(list1)):
            if list1[i].count(":\n") > 0:
                l11.append(list1[i].split("\n"))
        for i in range(len(l11)):
            l22 = list_PO.elementMerge(l11[i], 2)
            l33 = l33 + l22
        c = list_PO.alignmentKey(l33, ":")
        newWs = newbk.get_sheet(1)
        newWs.write(varExcelNum, 5, c, styleBlue)
        newbk.save(varExcel)

    def qcAnalysis_project(self,varExcelNum):
        print("【质控项目汇总 - 个人基本信息表】")
        l_person1 = Level_PO.getXpathText("//div[@class='main']/div[1]/div[2]/div[1]")
        l_person1Value = Level_PO.getXpathText("//div[@class='main']/div[1]/div[2]/div[2]")
        # print(l_person1)
        # print(l_person1Value)
        newWs = newbk.get_sheet(1)
        newWs.write(varExcelNum, 5, l_person1Value, styleBlue)
        newbk.save(varExcel)

if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(Web1)  # 构造测试集
    unittest.TextTestRunner(verbosity=2).run(suite1)  # 执行测试
    os.system("start explorer D:\\51\python\project\instance\zyjk\EHR\web")


