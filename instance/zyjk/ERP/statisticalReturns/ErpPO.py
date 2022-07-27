# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2022-7-19
# Description: ERP 对象库
# *****************************************************************


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

class ErpPO(object):

    def __init__(self):
        self.List_PO = ListPO()
        self.Time_PO = TimePO()
        self.Color_PO = ColorPO()
        self.List_PO = ListPO()
        self.Str_PO = StrPO()
        self.Char_PO = CharPO()


    def getToken(self):

        # 获取token
        url = "http://192.168.0.65/logincheck.php"
        header = {"content-type": "application/x-www-form-urlencoded"}
        d_iParam = {'USERNAME': "niuxuebin"}
        r = requests.post(url, headers=header, data=d_iParam, verify=False)
        a = r.cookies.get_dict()
        url = "http://192.168.0.65/general/appbuilder/web/business/product/crm"
        r = requests.get(url, headers={"Cookie": "PHPSESSID=" + a["PHPSESSID"]}, verify=False)
        token = str(r.url).split("token=")[1]
        # print(token)
        return token

    def login(self, varURL, varUser, varPass):
        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(varURL)
        self.Web_PO.driver.maximize_window()  # 全屏
        # self.Web_PO.driver.set_window_size(1366,768)  # 按分辨率1366*768打开
        self.Web_PO.inputId("name", varUser)
        self.Web_PO.inputId("password", varPass)
        self.Web_PO.clickXpath(u"//button[@id='submit']", 2)

    def clickMemuOA(self, varMemuName, varSubName):

        '''左侧菜单选择模块及浮层模块（无标题）'''

        sleep(2)
        x = self.Web_PO.getXpathsText("//div")
        list1 = []
        for i in x:
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
                self.Web_PO.clickXpath("//ul[@id='first_menu']/li[" + str(j + 1) + "]", 2)
                x = self.Web_PO.getXpathsText("//li")
                list3 = []
                list4 = []
                for i in x:
                    if varMemuName in i:
                        list3.append(i)
                        break
                # print(list3)
                for i in range(len(str(list3[0]).split("\n"))):
                    if str(list3[0]).split("\n")[i] != varMemuName and Str_PO.isContainChinese(
                            str(list3[0]).split("\n")[i]) == True:
                        list4.append(str(list3[0]).split("\n")[i])
                for k in range(len(list4)):
                    if list4[k] == varSubName:
                        self.Web_PO.clickXpath(
                            "//ul[@id='first_menu']/li[" + str(j + 1) + "]/div[2]/ul/li[" + str(k + 1) + "]/a", 2)

    def clickMemuERP(self, menu1, menu2):

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

    def zoom(self, percent):

        # 缩放比率

        # js = "document.body.style.zoom='70%'"
        js = "document.body.style.zoom='" + str(percent) + "%'"
        self.Web_PO.driver.execute_script(js)

    def quit(self):
        self.Web_PO.quit()

    def close(self):
        self.Web_PO.close()


