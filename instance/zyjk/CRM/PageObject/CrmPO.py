# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-7-18
# Description: CRM对象库
# *****************************************************************

from PO.webdriverPO import *
from instance.zyjk.CRM.config.config import *
webdriver_PO = WebdriverPO("chrome")
webdriver_PO.open(varURL)
webdriver_PO.driver.maximize_window()  # 全屏
Level_PO = LevelPO(webdriver_PO.driver)

import string,numpy
from string import digits

class CrmPO(object):

    def __init__(self):
        self.Level_PO = Level_PO

    # 登录
    def login(self):

        ''' 登录 '''

        self.Level_PO.inputId("name", varUser)
        self.Level_PO.inputId("password", varPass)
        self.Level_PO.clickId("submit", 2)

    # 销售分析列表页
    def saleAnalysisReport(self, varReportName, varProduct):

        ''' 获取 销售分析报表列表页数据 '''

        Level_PO.inIframe("tabs_15884_iframe", 2)
        if varReportName == "净销售分析报表":
            Level_PO.inIframe("net-sale", 2)
        elif varReportName == "产品销售分析报表":
            Level_PO.inIframe("product-sale", 2)
            Level_PO.selectIdText("product", varProduct)
            sleep(2)
        else:
            exit()
        l_net = Level_PO.getXpathsText("//tr/td")
        l_net = [''.join([i.strip() for i in price.strip().replace('代表 医院', '')]) for price in l_net]
        l_net1 = []
        l_quyu = []
        for i in range(len(l_net)):
            if l_net[i] != '':
                l_net1.append(l_net[i])
        for i in range(0, len(l_net1), 12):
            l_quyu.append(l_net1[i])
        l_quyu.remove("东区（廖荣平）")
        l_productList = numpy.array_split(l_net, len(l_net1) / 12)
        # for i in range(len(l_dest)):
        #     print(l_dest[i])
        return l_productList, l_quyu

    # 操作代表
    def optRepresentative(self, l_representativeName, varReportName, varQuyu, varDaibiao):

        ''' 销售分析报表 之 操作代表'''
        varTemp = 0
        print("--------------------------------------  " + varReportName + " 代表（" + varQuyu + "） 下 " + varDaibiao + " --------------------------------------  ")
        for i in range(len(l_representativeName)):
            if l_representativeName[i] == varQuyu:
                Level_PO.clickXpathsNum("//tr/td/a[1]", i + 1, 2)  # 点击代表
                Level_PO.inIframe("tabs_15884_iframe", 2)
                l_netRepresentative = Level_PO.getXpathsText("//tr/td")
                l_netRepresentative2 = numpy.array_split(l_netRepresentative, len(l_netRepresentative) / 12)
                for j in range(len(l_netRepresentative2)):
                    if l_netRepresentative2[j][0] == varDaibiao:
                        varTemp = j
                Level_PO.clickLinktext("返回", 2)
                if varReportName == "净销售分析报表":
                    Level_PO.inIframe("net-sale", 2)
                elif varReportName == "产品销售分析报表":
                    Level_PO.inIframe("product-sale", 2)

                return (l_netRepresentative2, varTemp)

    # 操作医院
    def optHospital(self, l_representativeName, varReportName, varQuyu, varYiyuan):

        ''' 销售分析报表 之 操作医院'''
        varTemp = 0
        print("--------------------------------------  " + varReportName + " 医院（" + varQuyu + "） 下 " + varYiyuan + " --------------------------------------  ")
        for i in range(len(l_representativeName)):
            if l_representativeName[i] == varQuyu:
                # 医院
                Level_PO.clickXpathsNum("//tr/td/a[2]", i + 1, 6)  # 点击医院
                Level_PO.inIframe("tabs_15884_iframe", 2)
                l_netHospital = Level_PO.getXpathsText("//tr/td")
                l_netHospital2 = numpy.array_split(l_netHospital, len(l_netHospital) / 12)
                for j in range(len(l_netHospital2)):
                    if l_netHospital2[j][0] == varYiyuan:
                        varTemp = j
                    # print(l_netHospital2[j])
                Level_PO.clickLinktext("返回", 2)
                if varReportName == "净销售分析报表":
                    Level_PO.inIframe("net-sale", 2)
                elif varReportName == "产品销售分析报表":
                    Level_PO.inIframe("product-sale", 2)

                return (l_netHospital2, varTemp)

