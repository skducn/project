# coding: utf-8
# ***************************************************************
# Author     : John
# Created on : 2020-3-20
# Description: 通过DOM来操作页面中各种元素，例如添加元素、删除元素、替换元素等
# 重新定义 find_element, find_elements, send_keys,
# clk, get, set, checkbox, select, iframe, js, boolean
# ***************************************************************
'''
重新定义
find_element
find_elements
send_keys
sendKeysByX
sendKeysById
sendKeysByname

todo clk
通过Xpath点击 clkByX(varXpath)
通过Xpaths遍历点击 clksByX(varXpaths)
通过Xpath按回车键 clkEnterByX(varXpath)
通过xpaths遍历点击第N个索引号 clkIndexByX(varXpaths)
通过xpaths遍历点击文本中包含varTPC的内容 clkTextPartialContentByX(varXpaths,varTPC)
通过xpaths遍历点击属性中包含varAPC内容 clkAttrPartialContentByX(varXpaths, varAttr,varAPC)
通过xpaths遍历二次xpath clkDoubleByX(varXpaths, varXpath)
通过id点击 clkById(varId)
通过name点击 clkByName(varText)
通过tagname点击 clkByTagname(varText)
通过linktext点击 clkByLinktext(varText)
通过linkstext点击 clkByLinkstext(varText)

todo get
通过xpaths遍历获取标签数量 getQtyByX(varXpaths)
通过xpath获取文本 getTextByX(varXpath)
通过xpaths遍历获取文本列表 getTextListByX(varXpaths)
通过xpaths遍历获取文本所在的位置 getTextIndexByX(varXpaths, varText)
通过xpaths遍历获取文本包含部分内容的位置 getTextPartialContentIndexByX(varXpaths, varText)
通过xpaths遍历获取指定文本之前的文本 getLeftTextByX(varXpaths, varText)
通过xpath获取属性值 getAttrValueByX(varXpath, varAttr)
通过xpaths遍历获取所有相同属性的值列表 getAttrValueListByX(varXpaths, varAttr)
通过xpaths遍历获取属性值所在的位置 getAttrIndexByX(varXpaths, varAttr, varValue)
通过xpaths遍历获取部分包含属性值所在的位置 getAttrPartialContentIndexByX(varXpaths, varAttr, varValue)
通过xpaths遍历获取所有文本对应的属性值字典 getTextAttrValueDictByX(varXpaths, varAttr)
通过linktext获取文本属性值 getAttrValueByH(varText, varAttr)

todo set
通过id设置文本 setTextById()
通过id追加文本 appendTextById()
通过name设置文本 setTextByName()
通过name追加文本 appendTextByName()
通过xpath设置文本 setTextByX()
通过xpath追加文本 appendTextByX()
通过xpath键盘设置文本 setTextEnterByX()
通过xpath键盘追加文本  appendTextEnterByX()

todo checkbox
是否选中复选框 isSelected(varXpath)
取消所有已勾选的复选框clsSelected(varXpaths)

todo select
通过id选择文本 sltTextById(varId, varText)
通过id选择值 sltValueById(varId, varValue)
通过name选择文本 sltTextByName(varName, varText)
通过name选择值 sltValueByName(varName, varValue)

todo iframe
通过Xpath切换到iframe switchIframeByX(varXpath)
通过id切换到iframe   switchIframeById(varId)
通过xpaths遍历遍历属性中包含指定值切换iframe  switchIframeAttrPartialContentByX(varXpaths,varAttr,varValue,2)
多个iframe之间切换  switchIframe(0)
退出iframe  quitIframe(0)

todo js
清除input输入框内容 clsTextByJs()
清除readonly属性，是元素可见  clsReadonlyByX(varXpath)
通过id去掉控件只读属性 clsReadonlyById(varId)
通过name去掉只读属性 clsReadonlyByName(varName)
通过name去掉隐藏属性 clsDisplayByName(varName)
通过tagname去掉隐藏属性 clsDisplayByTagName(varLabel, varLen)

todo boolean
通过xpath判断ture或false isBooleanByX(varPath)
通过xpath判断属性是否存在 isBooleanAttr(varXpath, varAttr)
通过xpath判断属性值是否存在 isBooleanAttrValue(varPath, varAttr, varValue)
通过Id判断ture或false isBooleanById(varId)
通过name判断ture或false isBooleanByName(varName)
通过超链接判断是否包含varText  isBooleanTextPartialContentByP(varPartText)
通过超链接判断是否存在varText isBooleanTextByL(varText)
通过xpath判断varText是否存在  isBooleanTextByX(varPath, varText)

todo alert(system)
点击弹框中的确认 alertAccept()
点击弹框中的取消 alertDismiss()
获取弹框中的文案 alertText()
'''

import sys, os, platform, platform, psutil, ddddocr, requests, bs4, subprocess
# import pyscreeze, pyautogui, cv2
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.abstract_event_listener import *
from selenium.webdriver.support.event_firing_webdriver import *
from selenium.webdriver.support.expected_conditions import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image, ImageDraw, ImageGrab
from pytesseract import *


class DomPO(object):

    def __init__(self, driver):
        self.driver = driver

    def check_contain_chinese(self, check_str):
        # 判断字符串中是否包含中文符合
        for ch in check_str.decode("utf-8"):
            if "\u4e00" <= ch <= "\u9fff":
                return True
        return False

    def find_element(self, *loc):
        """重写元素定位"""
        try:
            # Python特性，将入参放在元组里，入参loc，加*，变成元组。
            # WebDriverWait(self.driver,10).until(lambda driver: driver.find_element(*loc).is_displayed())
            # 注意：以下loc入参本身就是元组，所以不需要再加*
            WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(loc))
            return self.driver.find_element(*loc)
        except:
            print("未找到元素 %s " % (loc))

    def find_elements(self, *loc):
        """重写元素集定位"""
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc))
            return self.driver.find_elements(*loc)
        except:
            print("未找到元素集 %s " % (loc))

    def send_keys(self, loc, vaule, clear_first=True, click_first=True):
        """重写键盘方法"""
        try:
            loc = getattr(self, "_%s" % loc)  # getattr相当于实现self.loc
            if click_first:
                self.find_element(*loc).click()
            if clear_first:
                self.find_element(*loc).clear()
                self.find_element(*loc).send_keys(vaule)
        except AttributeError:
            print("未找到元素 %s " % (loc))

    def sendKeysByX(self, varXpath, varValue):
        """通过Xpath键盘发送"""
        # 如：Web_PO.sendKeysXpath("//input[@id='impload'", os.getcwd() + "\\drugTemplet.xls")  # 导入文件
        # self.driver.find_element_by_xpath(varXpath).send_keys(varValue)
        self.find_element(*(By.XPATH, varXpath)).send_keys(varValue)

    def sendKeysById(self, varId, varValue):
        """通过id键盘发送"""
        # 如：Web_PO.sendKeysId("impload", os.getcwd() + "\\drugTemplet.xls")  # 导入文件
        # self.driver.find_element_by_id(varId).send_keys(varValue)
        self.find_element(*(By.ID, varId)).send_keys(varValue)

    def sendKeysName(self, varName, varValue):
        """通过name键盘发送"""
        # self.driver.find_element_by_name(varName).send_keys(varValue)
        self.find_element(*(By.NAME, varName)).send_keys(varValue)



   # todo assert

    def assertTrue(self, testValue, errMsg):
        try:
            if testValue == True:
                return True
            else:
                print(errMsg)
                return False
        except:
            return None

    def assertEqualTrue(self, expected, actual):
        try:
            if expected == actual:
                return True
            else:
                return False
        except:
            return None

    def assertEqual(self, expected, actual, okMsg, errMsg):
        try:
            if expected == actual:
                # print(okMsg)
                return True
            else:
                # print(errMsg)
                return False
        except:
            return None

    def assertEqualValue(self, expected, actual, okMsg, errMsg):

        if expected == actual:

            return True
        else:

            return False

    def assertContain(self, one, all, okMsg, errMsg):
        try:
            if one in all:
                print(okMsg)
                return True
            else:
                print(errMsg)
                return False
        except:
            return None

    def assertEqualNotNone(self, expected, actual):
        try:
            if (expected and actual) and (expected != None and actual != None):
                return 1, expected
            else:
                return 0, 0
        except:
            return None

    def getError(self, varStatus, varErrorInfo, varErrorRow):
        # 当函数返回error时，获取当前语句行号及错误提示。
        # 因此函数必须要有返回值
        # Level_PO.getError(Level_PO.inputId(u"officebundle_tmoffice_officeName", u"自动化科室123"), u"输入框定位错误！",sys._getframe().f_lineno)
        # errorrrrrrrrrrr, 101行, '获取科室文本与对应值的字典'。
        if varStatus == "error":
            print("errorrrrrrrrrrr,", varErrorRow, "行,", varErrorInfo)
            sys.exit(0)



    # todo clk

    def clkByX(self, varXpath, t=0):
        """通过Xpath点击"""
        self.find_element(*(By.XPATH, varXpath)).click()
        sleep(t)

    def clksByX(self, varXpaths, t=0):
        """通过Xpaths遍历点击"""
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            a.click()
            sleep(t)

    def clkEnterByX(self, varXpath, t=0):
        """通过Xpath按回车键"""
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.ENTER)
        sleep(t)

    def clkIndexByX(self, varPaths, varIndex, t=0):
        """通过xpaths遍历点击第N个索引号"""
        # 如：遍历按钮点击第5个。clkIndexByX(u"//button[@ng-click='action.callback()']",5)
        index = 0
        for a in self.find_elements(*(By.XPATH, varPaths)):
            index = index + 1
            if index == varIndex:
                a.click()
                break
        sleep(t)

    def clkTextPartialContentByX(self, varXpaths, varTPC, t=0):
        """通过xpaths遍历点击文本中包含varTPC的内容"""
        # 如：遍历按钮点击所有文本中包含20190506059的内容。clkTextsContain(u"//td[@aria-describedby='gridTable_run_name']/a",u"20190506059")
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if varTPC in a.text:
                a.click()
                break
        sleep(t)

    def clkAttrPartialContentByX(self, varXpaths, varAttr, varAPC, t=0):
        """通过xpaths遍历点击属性中包含varAPC内容"""
        # 如：遍历点击a链接属性href中包含www内容， clkAttrPartialContentByX("//a","href","www")
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if varAPC in a.get_attribute(varAttr):
                a.click()
                break
        sleep(t)

    def clkDoubleByX(self, varXpaths, varXpath, t=1):
        """通过xpaths遍历二次xpath"""
        # 一般用于，click后二次确认
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            a.click()
            sleep(t)
            self.find_element(*(By.XPATH, varXpath)).click()
        sleep(t)

    def clkById(self, varId, t=0):
        """通过id点击"""
        self.find_element(*(By.ID, varId)).click()
        sleep(t)

    def clkByName(self, varName, t=0):
        """通过name点击"""
        self.find_element(*(By.NAME, varName)).click()
        sleep(t)

    def clkByTagname(self, varText, t=0):
        """通过tagname点击"""
        self.find_element(*(By.TAG_NAME, varText)).click()
        sleep(t)

    def clkByLinktext(self, varText, t=0):
        """通过linktext点击"""
        self.find_element(*(By.LINK_TEXT, varText)).click()
        sleep(t)

    def clkByLinkstext(self, varText, t=0):
        """通过linkstext点击"""
        for a in self.find_elements(*(By.LINK_TEXT, varText)):
            a.click()
        sleep(t)

    def clickXpathXpath(self, varPath, varPath2, t=0):
        # ? 未侧式
        try:
            elements = self.find_element(*(By.XPATH, varPath))
            actions = ActionChains(self.driver)
            actions.move_to_element(elements).perform()
            yy = self.find_element(*(By.XPATH, varPath2))
            yy.click()
            sleep(t)
        except:
            return None
    def clickXpathRight(self, varPath, varId):
        # ?
        try:
            xx = self.find_element(*(By.XPATH, varPath))
            yy = self.find_element(*(By.ID, varId))
            ActionChains(self.driver).drag_and_drop(xx, yy).perform()
            # ActionChains(self.driver).dra
            # print "end"
            ActionChains(self.driver).click_and_hold(xx).perform()
            # perform()
            # ActionChains(self.driver).click
            ActionChains(self.driver).move_to_element(
                self.find_element(*(By.ID, varId))
            )
        except:
            return None



    # todo get

    def getQtyByX(self, varXpaths):
        """通过xpaths遍历获取标签数量"""
        # 如：获取tr下有多少个div标签 getQtyByX('//*[@id="app"]/tr/div')
        qty = 0
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            qty = qty + 1
        return qty

    def getTextByX(self, varXpath):
        """通过xpath获取文本"""
        # 如：getTextByX(u"//input[@class='123']")
        return self.find_element(*(By.XPATH, varXpath)).text


    def getTextListByX(self, varXpaths):
        """通过Xpaths遍历获取文本列表"""
        # 如：getTextListByX("//tr")
        l_text = []
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            l_text.append(a.text)
        return l_text

    def getTextIndexByX(self, varXpaths, varText):
        """通过xpaths遍历获取文本所在的位置（索引号）"""
        # 获取test文本在tr里的位置，返回3，表示在第三个tr里，未找到返回none， 如：getTextIndexByX("//tr",'test')
        index = 0
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            index = index + 1
            if a.text == varText:
                return index
        return None

    def getTextPartialContentIndexByX(self, varXpaths, varTPC):
        """通过xpaths遍历获取文本包含部分内容的位置（索引号）"""
        # 如：getTextPartialContentIndexByX("//tr","test")
        index = 0
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            index = index + 1
            if varTPC in a.text:
                return index

    def getLeftTextByX(self, varXpaths, varText):
        """通过xpaths遍历获取指定文本之前的文本"""
        # 如文本集 a,b,c,d, getLeftTextByX("//tr",'c'), 返回列表【a,b】
        l_leftText = []
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if varText == a.text:
                break
            else:
                l_leftText.append(a.text)
        return l_leftText


    def getAttrValueByX(self, varXpath, varAttr):
        """通过xpath获取属性值"""
        # 如：getAttrValueByX(u"//input[@class='123']","href")
        return self.find_element(*(By.XPATH, varXpath)).get_attribute(varAttr)

    def getAttrValueListByX(self, varXpaths, varAttr):
        """通过xpaths遍历获取所有相同属性的值列表"""
        # 如：获取所有tr标签中 href的值 getAttrValueListByX("//tr", "href")
        l_attrValue = []
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            l_attrValue.append(a.get_attribute(varAttr))
        return l_attrValue

    def getAttrIndexByX(self, varXpaths, varAttr, varValue):
        """通过xpaths遍历获取属性值所在的位置（索引号）"""
        # 如：getAttrIndexByX("//td[9]/a","href","http://www.baidu.com")
        index = 0
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            index = index + 1
            if varValue == a.get_attribute(varAttr):
                return index

    def getAttrPartialContentIndexByX(self, varXpaths, varAttr, varValue):
        """通过xpaths遍历获取部分包含属性值所在的位置（索引号）"""
        # 如：getAttrPartialContentIndexByX("//td[9]/a","href","http://")
        index = 0
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            index = index + 1
            if varValue in a.get_attribute(varAttr):
                return index

    def getTextAttrValueDictByX(self, varXpaths, varAttr):
        """通过xpaths遍历获取文本对应的属性值字典"""
        # :如获取input下href即 {文本：属性值} getTextAttrValueDictByX(u"//input[@name='office_id']","href")
        l_text = []
        l_attrValue = []
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            l_text.append(a.text)
            l_attrValue.append(a.get_attribute(varAttr))
        return dict(zip(l_text, l_attrValue))

    def getAttrValueByH(self, varText, varAttr):
        """通过linktext获取文本属性值"""
        # 如：getAttrValueByH("超链接文本","href")
        return self.find_element(*(By.LINK_TEXT, varText)).get_attribute(varAttr)



    # todo set

    def setTextById(self, varId, varText):
        """通过id设置文本"""
        self.find_element(*(By.ID, varId)).clear()
        self.find_element(*(By.ID, varId)).send_keys(varText)

    def appendTextById(self, varId, varText):
        """通过id追加文本"""
        self.find_element(*(By.ID, varId)).send_keys(varText)

    def setTextByName(self, varName, varText):
        """通过name设置文本"""
        self.find_element(*(By.ID, varName)).clear()
        self.find_element(*(By.NAME, varName)).send_keys(varText)

    def appendTextByName(self, varName, varText):
        """通过name追加文本"""
        self.find_element(*(By.NAME, varName)).send_keys(varText)

    def setTextByX(self, varXpath, varText):
        """通过xpath设置文本"""
        self.find_element(*(By.XPATH, varXpath)).clear()
        self.find_element(*(By.XPATH, varXpath)).send_keys(varText)

    def appentTextByX(self, varXpath, varText):
        """通过xpath追加文本"""
        self.find_element(*(By.XPATH, varXpath)).send_keys(varText)

    def setTextEnterByX(self, varXpath, varText):
        """通过xpath键盘设置文本"""
        self.find_element(*(By.XPATH, varXpath)).clear()
        self.find_element(*(By.XPATH, varXpath)).send_keys(varText)
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.ENTER)

    def appendTextEnterByX(self, varXpath, varText):
        """通过xpath键盘追加文本"""
        self.find_element(*(By.XPATH, varXpath)).send_keys(varText)
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.ENTER)



    # todo checkbox

    def isSelected(self, varXpath):
        """是否选中复选框, True 或 False"""
        # isSelected(u"//input[@class='123']")
        return self.find_element(*(By.XPATH, varXpath)).is_selected()

    def clrSelected(self, varXpaths):
        """取消所有已勾选的复选框"""
        # clrSelected(u"//input[@type='checkbox']")
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if a.is_selected() == True:
                a.click()



    # todo select

    def sltTextById(self, varId, varText):
        """通过id选择文本"""
        # 如：value=1 , Text=启用 ，sltTextById("id", u'启用')
        Select(self.find_element(*(By.ID, varId))).select_by_visible_text(varText)
        # Select(self.driver.find_element_by_id(varId)).select_by_visible_text(varText)

    def sltValueById(self, varId, varValue):
        """通过id选择值"""
        # 如：value=10 , Text=启用 ，sltTextById("id", '10')
        Select(self.find_element(*(By.ID, varId))).select_by_value(varValue)
        # Select(self.driver.find_element_by_id(varId)).select_by_value(varValue)

    def sltTextByName(self, varName, varText):
        """通过name选择文本"""
        # 如：value=10 , Text=启用 ，sltTextByName("isAvilable", '启动')
        Select(self.find_element(*(By.NAME, varName))).select_by_visible_text(varText)
        # Select(self.driver.find_element_by_name(varName)).select_by_visible_text(varText)

    def sltValueByName(self, varName, varValue):
        """通过name选择值"""
        # 如：value=10 , Text=启用 ，sltValueByName("isAvilable", '10')
        Select(self.find_element(*(By.NAME, varName))).select_by_value(varValue)
        # Select(self.driver.find_element_by_name(varName)).select_by_value(varValue)

    def sltValueByX(self, varXpath, varValue):
        """通过xpath选择值"""
        # 如：value=10 , Text=启用 ，sltValueByName("isAvilable", '10')
        Select(self.find_element(*(By.XPATH, varXpath))).select_by_visible_text(varValue)
        # Select(self.driver.find_element_by_name(varName)).select_by_value(varValue)

    def selectXpathText(self, varPath, varText):
        # 遍历Xpath下的Option,(待确认)
        # self.selectXpathText(u"//select[@regionlevel='1']", u'启用'), （一般情况 value=1 , Text=启用）
        s1 = self.driver.find_element_by_xpath(varPath)
        l_content1 = []
        l_value1 = []
        # varContents = self.driver.find_elements_by_xpath(varByXpath + "/option")
        varContents = self.driver.find_elements_by_xpath(varPath + "/option")
        for a in varContents:
            l_content1.append(a.text)
            l_value1.append(a.get_attribute("value"))
        d_total1 = dict(zip(l_content1, l_value1))
        for i in range(len(d_total1)):
            if sorted(d_total1.items())[i][0] == varText:
                Select(s1).select_by_value(sorted(d_total1.items())[i][1])
                break
    def selectIdStyle(self, varByID, varText):
        # ？ 遍历某ID的下的option (不包含 隐藏的属性，如style=display:none），获取varText对应的值(待确认)
        # self.selectIdStyle(u"id", u'启用')  # （一般情况 value=1 , Text=启用）
        l_content1 = []
        l_value1 = []
        varCount = 0
        s1 = self.driver.find_element_by_id(varByID)
        varContents = s1.find_elements_by_tag_name("option")
        for a in varContents:
            if a.get_attribute("style") == "" and a.text == varText:
                l_content1.append(a.text)
                l_value1.append(a.get_attribute("value"))
                varCount = 1
        if varCount == 1:
            d_total1 = dict(zip(l_content1, l_value1))
            for i in range(len(d_total1)):
                if sorted(d_total1.items())[i][0] == varText:
                    Select(s1).select_by_value(sorted(d_total1.items())[i][1])
                    break
        else:
            return None
    def selectXpathsMenu1Menu2(self, varPaths1, varMenu, varPaths2, varMenu2, t):
        # 遍历级联菜单（选择一级菜单后再选择二级菜单）(待确认)
        # Level_PO.selectMenu("//a[@class='dropdown-toggle']", u"作业管理", "//a[@href='#']", u"作业框架管理", 3)
        try:
            for a in self.driver.find_elements_by_xpath(varPaths1):
                if varMenu == a.text:
                    a.click()
                    sleep(t)
                    for a2 in self.driver.find_elements_by_xpath(varPaths2):
                        if varMenu2 == a2.text:
                            a2.click()
                            sleep(t)
                            break
                    break
        except:
            return None
    def get_selectNAMEvalue(self, varByname, varContent):
        # 获取某select下text的value值。（下拉框，定位ByName，选择内容，text != value ）(待确认)
        s1 = self.driver.find_element_by_name(varByname)
        l_content1 = []
        l_value1 = []
        varContents = self.driver.find_elements_by_xpath(
            "//select[@name='" + varByname + "']/option"
        )
        for a in varContents:
            l_content1.append(a.text)
            l_value1.append(a.get_attribute("value"))
        d_total1 = dict(zip(l_content1, l_value1))
        for i in range(len(d_total1)):
            if sorted(d_total1.items())[i][0] == varContent:
                value = sorted(d_total1.items())[i][1]
                return value
    def get_selectOptionValue(self, varByname, varNum):
        # 获取某个select中text的value值。(待确认)
        varValue = self.driver.find_element_by_xpath(
            "//select[@name='" + varByname + "']/option[" + varNum + "]"
        ).get_attribute("value")
        return varValue



    # todo iframe

    def switchIframeByX(self, varXpath, t=1):
        """通过Xpath切换到iframe"""
        # 如：switchIframeByX("//body[@class='gray-bg top-navigation']/div[4]/iframe")
        self.driver.switch_to_frame(self.find_element(*(By.XPATH, varXpath)))
        sleep(t)

    def switchIframeById(self, varId, t=1):
        """通过id切换到iframe"""
        #如：switchIframeById（"layui-layer-iframe1"）
        self.driver.switch_to_frame(self.find_element(*(By.ID, varId)))
        sleep(t)

    def switchIframeAttrPartialContentByX(self, varXpaths, varAttr, varValue, t=1):
        """通过xpaths遍历遍历属性中包含指定值切换iframe"""
        # 如：switchIframeAttrPartialContentByX（"//iframe", "src", "/general/workflow/new/"）
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if varValue in a.get_attribute(varAttr):
                self.driver.switch_to_frame(self.driver.find_element_by_xpath(varXpaths))
                break
        sleep(t)

    def switchIframe(self, t=1):
        """多个iframe之间切换"""
        # 如：如第一层iframe1，第二层iframe2，两者之间切换
        self.driver.switch_to.parent_frame()
        sleep(t)

    def quitIframe(self, t=1):
        """退出iframe"""
        self.driver.switch_to_default_content()
        sleep(t)

    def inIframeTopDiv(self, varPath, t=0):
        # 定位iframe的div路径?(未确认)
        # evel_PO.inIframeDiv("[@id='showRealtime']", 2)
        # Home_PO.inIframeDiv("[@class='cetc-popup-content']/div", 2)
        iframe = self.driver.find_element_by_xpath("//div" + varPath + "/iframe")
        # print iframe.get_attribute("src")
        self.driver.switch_to_frame(iframe)
        sleep(t)



    # todo js

    def clsTextByJs(self, t=1):
        """清除input输入框内容"""
        self.driver.execute_script('document.querySelector("input[type=number]").value=""')
        sleep(t)

    def clsReadonlyByX(self, varXpath, t=0):
        """通过xpath去掉只读属性"""
        d = self.find_element(*(By.XPATH, varXpath))
        self.driver.execute_script('arguments[0].removeAttribute("readonly")', d)
        sleep(t)

    def clsReadonlyById(self, varId, t=0):
        """通过id去掉只读属性"""
        # 一般用于第三方日期控件
        self.driver.execute_script('document.getElementById("' + varId + '").removeAttribute("readonly")')
        sleep(t)

    def clsReadonlyByName(self, varName, t=0):
        """通过name去掉只读属性"""
        # 注意：document只支持getElementsByName方法获取标签数组，如 array[0]
        self.driver.execute_script('document.getElementsByName("' + varName + '")[0].removeAttribute("readonly")')
        sleep(t)

    def clsDisplayByName(self, varName, t=0):
        """通过name去掉隐藏属性"""
        self.driver.execute_script('document.getElementsByName("' + varName + '")[0].style.display=""')
        sleep(t)

    def clsDisplayByTagName(self, varLabel, varLen, t=1):
        """通过tagname去掉隐藏属性"""
        # 如：清除30个ul标签的display，30是ul数量，可以通过其他方式获取。 jsDisplayByTagName(30, "ul")
        for i in range(varLen):
            self.driver.execute_script('document.getElementsByTagName("' + varLabel + '")[' + str(i) + '].style.display=""')
        sleep(t)


    def displayBlockID(self, varID):
        # 未验证？(未确认)
        varJs = 'document.getElementById("filePath").style.display="block"'
        # document.getElementByPath
        return self.driver.find_element_by_id(varID).style.display



    # todo True or False

    def isBooleanByX(self, varPath):

        # 通过xpath判断ture或false

        flag = False
        try:
            self.find_element(*(By.XPATH, varPath))
            flag = True
        except:
            flag = False
        return flag

    def isBooleanAttrByX(self, varPath, varAttr):

        # 通过xpath判断属性是否存在

        flag = False
        try:
            element = self.find_element(*(By.XPATH, varPath))
            if element.get_attribute(varAttr):
                flag = True
        except:
            flag = False
        return flag

    def isBooleanAttrValueByX(self, varPath, varAttr, varValue):

        # 通过xpath判断属性值是否存在
        # 如：isBooleanAttrValueByX("//tr","href","www.badu.com")

        flag = False
        try:
            for a in self.find_elements(*(By.XPATH, varPath)):
                if varValue == a.get_attribute(varAttr):
                    flag = True
                    break
        except:
            flag = False
        return flag

    def isBooleanAttrValueListByX(self, varPath, varAttr, varValue):

        """通过xpath判断属性等于值"""
        # 如：isBooleanAttrValueListByX("//tr","href","www.badu.com")
        # .isBooleanAttrValueListByX("//div/label/span[1]", 'class', 'el-radio__input is-disabled is-checked')
        # 判断单选框是否被选中。

        l1 = []
        for a in self.find_elements(*(By.XPATH, varPath)):
            if varValue == a.get_attribute(varAttr):
                l1.append("True")
            else:
                l1.append("False")
        return l1

    def isBooleanAttrContainValueListByX(self, varPath, varAttr, varValue):

        """通过xpath判断属性包含值"""
        # .isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', 'el-radio__input is-disabled is-checked')
        # 判断单选框是否被选中。

        l1 = []
        for a in self.find_elements(*(By.XPATH, varPath)):
            if varValue in a.get_attribute(varAttr):
                l1.append("True")
            else:
                l1.append("False")
        return l1

    def isBooleanById(self, varId):

        # 通过Id判断ture或false

        flag = False
        try:
            self.find_element(*(By.ID, varId))
            flag = True
        except:
            flag = False
        return flag

    def isBooleanByName(self, varName):

        # 通过name判断ture或false

        flag = False
        try:
            self.find_element(*(By.NAME, varName))
            flag = True
        except:
            flag = False
        return flag

    def isBooleanTextPartialContentByP(self, varPartText):

        # 通过超链接判断是否包含varText

        flag = False
        try:
            self.driver.find_element_by_partial_link_text(varPartText)
            flag = True
        except:
            flag = False
        return flag

    def isBooleanTextByL(self, varText):

        # 通过超链接判断是否存在varText

        flag = False
        try:
            self.driver.find_element_by_link_text(varText)
            flag = True
        except:
            flag = False
        return flag

    def isBooleanTextByX(self, varPath, varText):

        # 通过xpath判断文本是否存在

        flag = False
        try:
            if self.find_element(*(By.XPATH, varPath)).text == varText:
                flag = True
        except:
            flag = False
        return flag


    def isElementVisibleXpath(self, element):
        # 未验证？？？（未确认）
        driver = self.driver
        try:
            the_element = EC.visibility_of_element_located(
                driver.find_element_by_partial_link_text(element)
            )
            assert the_element(driver)
            flag = True
        except:
            flag = False
        return flag
    def locElement(self, varPath, t=0):
        # 定位到某元素???（未确认）
        try:
            elements = self.find_element(*(By.XPATH, varPath))
            actions = ActionChains(self.driver)
            actions.move_to_element(elements).perform()
            sleep(t)
        except:
            return None



    # todo alert(system)

    def alertAccept(self):

        # 点击弹框中的确认

        alert = self.driver.switch_to.alert
        alert.accept()

    def alertDismiss(self):

        # 点击弹框中的取消

        alert = self.driver.switch_to.alert
        alert.dismiss()

    def alertText(self):

        # 获取弹框中的文案

        alert = self.driver.switch_to.alert
        return alert.text


    def getCount(self, varLabel):
        c = self.find_elements(*(By.TAG_NAME, varLabel))
        return len(c)

