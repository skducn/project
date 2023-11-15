# coding: utf-8
# ***************************************************************
# Author     : John
# Created on : 2020-3-20
# Description: 通过DOM来操作页面中各种元素，例如添加元素、删除元素、替换元素等
# # 重新定义 find_element, find_elements, send_keys,
# set, click, get, checkbox, select, iframe, js, True or False, alert
# ***************************************************************
# Set
# setTextById
# appendTextById
# setByName
# appendTextByName
# setText
# appendText
# setTextEnter
# appendTextEnter
#
# clk
# 通过Xpath点击 clk(varXpath)
# 通过Xpaths点击所有 clks(varXpaths)
# 通过Xpath按回车键 clkEnter(varXpath)
# 多个click点击第N个 clkSeats(varXpaths)
# 点击所有text中包含某内容的连接 clkTextsContain(varXpaths,varContain)
# 点击所有属性varAttr中包含某内容的连接 clkAttrsContain(varXpaths, varAttr,varContain)
# 遍历路径之路径, 一般用于，click后二次确认  clkClks(varXpaths, varXpaths2)
# 通过id点击 clkById(varId)
# 通过超链接点击 clkByLinktext(varText)
# 点击所有超链接 clkByLinkstext(varText)
# 通过标签点击 clkByTagname(varText)
#
# Get
# 获取文本 getText(varXpath)
# 获取所有文本 getTexts(varXpaths)
# 获取指定文本之前的文本 getTextBeforeTexts(varXpaths, varText)
# 获取文本所在的位置 getSeatByText(varXpaths, varText)
# 获取部分文本所在位置 getSeatByPartialText(varXpaths, varText)
# 获取某属性值所在的位置 getSeatByAttrValue(varXpaths, varAttr, varValue)
# 获取某属性部分值所在的位置 getSeatByAttrPortialValue(varXpaths, varAttr, varValue)
# 获取元素数量 getElementQty(varXpaths)
# 获取属性的值 getValueByAttr(varXpaths, varAttr)
# 获取所有相同属性的值 getValuesByAttr(varXpaths, varAttr)
# 获取所有文本对应的属性值，如 {文本：属性值} getTextsAndAttrs
# (varXpaths, varAttr)
# 获取超链接文本的属性值 getHyperlinkByAttr(varXpaths, varAttr)
#
# Checkbox
# 是否选中复选框 isSelected(varXpath)
# 取消所有已勾选的复选框clsSelected(varXpaths)
#
# Select
# 通过Id属性选择文本 sltTextById(varId, varText)
# 通过Id属性选择值 sltValueById(varId, varValue)
# 通过Name属性选择文本 sltTextByName(varName, varText)
# 通过Name属性选择值 sltValueByName(varName, varValue)
#
# Iframe
# 通过Xpath定位iframe iframe(varXpath,0)
# 通过id定位iframe   iframeById(varId,0)
# 通过遍历属性中包含指定值定位iframe  iframeByAttrs(varXpaths,varAttr,varValue,2)
# 多个iframe之间切换  iframeSwitch(0)
# 退出iframe  iframeQuit(0)
#
# Js
# 清除input输入框内容 jsExecute()
# 清除readonly属性，是元素可见  jsReadonly(varXpath)
# 通过id去掉控件只读属性 jsReadonlyById(varId)
# 通过Name去掉控件只读属性 jsReadonlyByName(varName)
# 通过name去掉隐藏属性 jsDisplayByName(varName)
#
# True or False
# 通过Xpath方式检查元素是否存在 isElement(varPath)
# 通过Xpath方式检查特定属性的元素是否存在 isElementByAttr(varXpath, varAttr,varValue)
# 通过Id方式检查元素是否存在 isElementById(varId)
# 通过Name方式检查元素是否存在 isElementByName(varName)
# 通过超链接方式检查文本是否包含varText  isElementByPartialText(varPartText)
# 通过超链接方式检查文本是否存在 isElementByLinkText(varText)
# 通过文本比对检查文本是否存在  isElementText(varPath, varText)
#
# alert(system)
# 点击弹框中的确认 alertAccept()
# 点击弹框中的取消 alertDismiss()
# 获取弹框中的文案 alertText()


import sys, os, platform, psutil, pyautogui, ddddocr
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
            # 注意：入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
            # WebDriverWait(self.driver,10).until(lambda driver: driver.find_element(*loc).is_displayed())
            # 注意：以下入参本身是元组，不需要加*
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc))
            return self.driver.find_element(*loc)
        except:
            # print u"%s 页面中未能找到元素 %s "%(self, loc)
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
            # print u"%s 页面中未能找到 %s 元素"%(self, loc)
            print("未找到元素 %s " % (loc))

    def sendKeysId(self, varId, dimValue):
        # 上传文件
        # Oa_PO.Web_PO.sendKeysId("impload", os.getcwd() + "\\drugTemplet.xls")  # 导入文件
        self.driver.find_element_by_id(varId).send_keys(dimValue)

    def sendKeysName(self, varName, dimValue):
        self.driver.find_element_by_name(varName).send_keys(dimValue)

    def sendKeysXpath(self, dimXpath, dimValue):
        # 上传文件
        # Oa_PO.Web_PO.sendKeysXpath("//input[@id='impload'", os.getcwd() + "\\drugTemplet.xls")  # 导入文件
        self.driver.find_element_by_xpath(dimXpath).send_keys(dimValue)


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





    # todo set

    def setTextById(self, varId, varText):

        self.find_element(*(By.ID, varId)).clear()
        self.find_element(*(By.ID, varId)).send_keys(varText)

    def appendTextById(self, varId, varText):

        self.find_element(*(By.ID, varId)).send_keys(varText)

    def setByName(self, varName, varText):

        self.find_element(*(By.ID, varName)).clear()
        self.find_element(*(By.NAME, varName)).send_keys(varText)

    def appendTextByName(self, varName, varText):

        self.find_element(*(By.NAME, varName)).send_keys(varText)

    def setText(self, varXpath, varText):

        self.find_element(*(By.XPATH, varXpath)).clear()
        self.find_element(*(By.XPATH, varXpath)).send_keys(varText)

    def appentText(self, varXpath, varText):

        self.find_element(*(By.XPATH, varXpath)).send_keys(varText)

    def setTextEnter(self, varXpath, varText):

        self.find_element(*(By.XPATH, varXpath)).clear()
        self.find_element(*(By.XPATH, varXpath)).send_keys(varText)
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.ENTER)

    def appendTextEnter(self, varXpath, varText):

        self.find_element(*(By.XPATH, varXpath)).send_keys(varText)
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.ENTER)



    # todo click

    def clk(self, varXpath, t=0):

        '''
        通过Xpath点击
        :param varPath:
        :param t:
        :return:
        '''

        self.find_element(*(By.XPATH, varXpath)).click()
        sleep(t)

    def clks(self, varXpaths, t=0):

        '''
        通过Xpaths点击所有
        :param varPaths:
        :param t:
        :return:
        '''

        for a in self.find_elements(*(By.XPATH, varXpaths)):
            a.click()
            sleep(t)

    def clkEnter(self, varXpath, t=0):

        '''
        通过Xpath按回车键
        :param varPath:
        :param t:
        :return:
        '''

        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.ENTER)
        sleep(t)

    def clkSeats(self, varPaths, varSeat, t=0):

        '''
        多个click点击第N个
        :param varPaths: u"//button[@ng-click='action.callback()']"
        :param varNum: 5
        :param t:
        :return:
        表示遍历后点击第五个连接。
        '''

        c = 0
        for a in self.find_elements(*(By.XPATH, varPaths)):
            c = c + 1
            if c == varSeat:
                a.click()
                break
        sleep(t)

    def clkTextsContain(self, varXpaths, varContain, t=0):

        '''
        点击所有text中包含某内容的连接
        :param varPaths: "//td[@aria-describedby='gridTable_run_name']/a"
        :param varContain: 20190506059
        :param t:
        :return:
        '''

        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if varContain in a.text:
                a.click()
                break
        sleep(t)

    def clkAttrsContain(self, varXpaths, varAttr, varContain, t=0):

        '''
        点击所有属性varAttr中包含某内容的连接。
        :param varXpaths:   //a
        :param varAttr:  href
        :param varContain:  1212
        :param t:
        :return:
        '''

        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if varContain in a.get_attribute(varAttr):
                a.click()
                break
        sleep(t)

    def clkClks(self, varPaths, varPaths2, t=1):

        '''
        遍历路径之路径, 一般用于，click后二次确认
        :param varPaths:
        :param varPaths2:
        :param t:
        :return:
        '''

        for a in self.find_elements(*(By.XPATH, varPaths)):
            a.click()
            sleep(t)
            self.find_element(*(By.XPATH, varPaths2)).click()
            sleep(t)

    def clkById(self, varId, t=0):

        '''
        通过id点击
        :param varId:
        :param t:
        :return:
        '''

        self.find_element(*(By.ID, varId)).click()
        sleep(t)

    def clkByLinktext(self, varText, t=0):

        '''
        通过超链接点击
        :param varText:
        :param t:
        :return:
        '''

        self.find_element(*(By.LINK_TEXT, varText)).click()
        sleep(t)

    def clkByLinkstext(self, varText, t=0):

        '''
        点击所有超链接
        :param varText:
        :param t:
        :return:
        '''

        for a in self.find_elements(*(By.LINK_TEXT, varText)):
            a.click()
        sleep(t)

    def clkByTagname(self, varText, t=0):

        '''
        通过标签点击
        :param varText: "test"
        :param t:
        :return:
        '''

        self.find_element(*(By.TAG_NAME, varText)).click()
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

    def getText(self, varXpath):

        '''
        获取文本
        :param varXpath: u"//input[@class='123']"
        :return: Text
        '''

        return self.find_element(*(By.XPATH, varXpath)).text

    def getTexts(self, varXpaths):

        '''
        获取文本列表
        :param varXpaths: "//tr"
        :return: list
        '''

        l_text = []
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            l_text.append(a.text)
        return l_text

    def getTextBeforeTexts(self, varXpaths, varText):

        '''
        获取指定文本之前的文本
        :param varXpaths: "//div"
        :param varText: "姓名"
        :return:
        '''

        l_text = []
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if varText in a.text:
                break
            else:
                l_text.append(a.text)
        return l_text

    def getSeatByText(self, varXpaths, varText):

        '''
        获取文本所在的位置
        :param varXpaths: "//tr"
        :param varText:  "测试"
        :return: 位置，如3，表示"测试"在第3个tr里，未找到返回None
        '''

        seat = 0
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            seat = seat + 1
            if a.text == varText:
                return seat
        return None

    def getSeatByPartialText(self, varXpaths, varPartialText):

        '''
        获取部分文本所在位置
        :param varXpaths: "//tr"
        :param varPartialText:  "test"
        :return: 位置
        '''

        seat = 0
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            seat = seat + 1
            if varPartialText in a.text:
                return seat

    def getSeatByAttrValue(self, varXpaths, varAttr, varValue):

        '''
        获取某属性值所在的位置
        :param varXpaths: "//td[9]/a"
        :param varAttr: "href"
        :param varValue: "http://www.baidu.com"
        :return: 位置
        '''

        seat = 0
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            seat = seat + 1
            if varValue == a.get_attribute(varAttr):
                return seat

    def getSeatByAttrPortialValue(self, varXpaths, varAttr, varValue):

        '''
        获取某属性部分值所在的位置
        :param varXpaths: "//td[9]/a"
        :param varAttr:  "href"
        :param varValue:  "123"
        :return:
        '''

        seat = 0
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            seat = seat + 1
            if varValue in a.get_attribute(varAttr):
                return seat

    def getElementQty(self, varXpaths):

        '''
        获取元素数量
        :param varXpaths: '//*[@id="app"]/tr/div'
        :return: div数量，获取tr下有多少个div标签
        '''

        qty = 0
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            qty = qty + 1
        return qty

    def getValueByAttr(self, varXpaths, varAttr):

        '''
        获取属性的值
        :param varXpaths: u"//input[@class='123']"
        :param varAttr: "href"
        :return:
        '''

        return self.find_element(*(By.XPATH, varXpaths)).get_attribute(varAttr)

    def getValuesByAttr(self, varXpaths, varAttr):

        '''
        获取所有相同属性的值
        :param varXpaths: "//tr"
        :param varAttr:  "href"
        :return: 获取所有tr标签中 href的值
        '''

        l_value = []
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            l_value.append(a.get_attribute(varAttr))
        return l_value

    def getTextsAndAttrs(self, varXpaths, varAttr):

        '''
        获取所有文本对应的属性值，如 {文本：属性值}
        :param varXpaths: u"//input[@name='office_id']"
        :param varAttr:  "href"
        :return:
        '''

        list1 = []
        list2 = []
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            list1.append(a.text)
            list2.append(a.get_attribute(varAttr))
        return dict(zip(list1, list2))

    def getHyperlinkByAttr(self, varText, varAttr):

        '''
        获取超链接文本的属性值
        :param varText: u"超链接文本"
        :param varAttr: "href"
        :return:
        '''

        return self.find_element(*(By.LINK_TEXT, varText)).get_attribute(varAttr)



    # todo checkbox

    def isSelected(self, varXpath):

        '''
        是否选中复选框
        :param varXpath: u"//input[@class='123']"
        :return: True 或 False
        '''

        return self.find_element(*(By.XPATH, varXpath)).is_selected()

    def clrSelected(self, varXpaths):

        '''
        取消所有已勾选的复选框
        :param varXpaths: u"//input[@type='checkbox']"
        :return:
        '''

        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if a.is_selected() == True:
                a.click()



    # todo select

    def sltTextById(self, varId, varText):

        '''
        通过Id属性选择文本
        :param varId: "id"
        :param varText: u'启用'
        :return:
        （一般情况 value=1 , Text=启用）
        '''

        Select(self.find_element(*(By.ID, varId))).select_by_visible_text(varText)
        # Select(self.driver.find_element_by_id(varId)).select_by_visible_text(varText)

    def sltValueById(self, varId, varValue):

        '''
        通过Id属性选择值
        :param varId: "id"
        :param dimValue: "10"
        :return:
        （一般情况 value=10 , Text=启用）
        '''

        Select(self.find_element(*(By.ID, varId))).select_by_value(varValue)
        # Select(self.driver.find_element_by_id(varId)).select_by_value(varValue)

    def sltTextByName(self, varName, varText):

        '''
        通过Name属性选择文本
        :param varName: u"isAvilable"
        :param varText: u"启动"
        :return:
        '''

        Select(self.find_element(*(By.NAME, varName))).select_by_visible_text(varText)
        # Select(self.driver.find_element_by_name(varName)).select_by_visible_text(varText)

    def sltValueByName(self, varName, varValue):

        '''
        通过Name属性选择值
        :param varName: u"isAvilable"
        :param varValue: 10
        :return:
        '''

        Select(self.find_element(*(By.NAME, varName))).select_by_value(varValue)
        # Select(self.driver.find_element_by_name(varName)).select_by_value(varValue)



    def selectXpathText(self, varPath, varText):
        # 遍历Xpath下的Option,
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
        # ？ 遍历某ID的下的option (不包含 隐藏的属性，如style=display:none），获取varText对应的值
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
        # 遍历级联菜单（选择一级菜单后再选择二级菜单）
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
        # 获取某select下text的value值。（下拉框，定位ByName，选择内容，text != value ）
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
        # 获取某个select中text的value值。
        varValue = self.driver.find_element_by_xpath(
            "//select[@name='" + varByname + "']/option[" + varNum + "]"
        ).get_attribute("value")
        return varValue



    # todo iframe

    def iframe(self, varXpaths, t=1):
        '''
        通过Xpath定位iframe
        :param varXpaths: "//body[@class='gray-bg top-navigation']/div[4]/iframe"
        :param t: 1
        :return:
        '''

        self.driver.switch_to_frame(self.find_element(*(By.XPATH, varXpaths)))
        # self.driver.switch_to_frame(self.driver.find_element_by_xpath(varXpaths))
        sleep(t)

    def iframeById(self, varId, t=1):

        '''
        通过id定位iframe
        :param varId: "layui-layer-iframe1"
        :param t: 1
        :return:
        '''

        self.driver.switch_to_frame(self.find_element(*(By.ID, varId)))
        # self.driver.switch_to_frame(self.driver.find_element_by_id(varId))
        sleep(t)

    def iframeByAttrs(self, varXpaths, varAttr, varValue, t=1):

        '''
        通过遍历属性中包含指定值定位iframe
        :param varXpaths: "//iframe"
        :param varAttr: "src"
        :param varValue: "/general/workflow/new/"
        :param t: 1
        :return:
        '''

        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if varValue in a.get_attribute(varAttr):
                self.driver.switch_to_frame(self.driver.find_element_by_xpath(varXpaths))
                break
        sleep(t)

    def iframeSwitch(self, t=1):

        '''
        多个iframe之间切换
        :param t: 1
        :return:
        如第一层iframe1，第二层iframe2，两者之间切换
        '''

        self.driver.switch_to.parent_frame()
        sleep(t)

    def iframeQuit(self, t=1):

        '''
        退出iframe
        :param t: 1
        :return:
        '''

        self.driver.switch_to_default_content()
        sleep(t)



    def inIframeTopDiv(self, varPath, t=0):
        # 定位iframe的div路径?
        # evel_PO.inIframeDiv("[@id='showRealtime']", 2)
        # Home_PO.inIframeDiv("[@class='cetc-popup-content']/div", 2)
        iframe = self.driver.find_element_by_xpath("//div" + varPath + "/iframe")
        # print iframe.get_attribute("src")
        self.driver.switch_to_frame(iframe)
        sleep(t)



    # todo js

    def jsExecute(self, t=1):

        '''
        清除input输入框内容
        :param t:
        :return:
        '''

        self.driver.execute_script('document.querySelector("input[type=number]").value=""')
        sleep(t)

    def jsReadonly(self, varXpath, t=0):

        '''
        清除readonly属性，是元素可见
        :param varXpath:
        :param t:
        :return:
        '''

        # d = self.driver.find_element_by_xpath(varXpath)
        d = self.find_element(*(By.XPATH, varXpath))
        self.driver.execute_script('arguments[0].removeAttribute("readonly")', d)
        sleep(t)

    def jsReadonlyById(self, varId, t=0):
        '''
        通过id去掉控件只读属性，一般用于第三方日期控件
        :param varId:
        :param t:
        :return:
        '''

        self.driver.execute_script('document.getElementById("' + varId + '").removeAttribute("readonly")')
        sleep(t)

    def jsReadonlyByName(self, varName, t=0):

        '''
        通过Name去掉控件只读属性，一般用于第三方日期控件
        :param varName:
        :param t:
        :return:
         # 注意：document不支持getElementByName方法，只有getElementsByName方法获取标签数组，可通过数组第一个元素获取，如 array[0]
        '''

        self.driver.execute_script('document.getElementsByName("' + varName + '")[0].removeAttribute("readonly")')
        sleep(t)

    def jsDisplayByName(self, varName, t=0):

        '''
        通过name去掉隐藏属性，显示UI
        :param varName:
        :param t:
        :return:
        '''

        self.driver.execute_script('document.getElementsByName("' + varName + '")[0].style.display=""')
        sleep(t)



    def displayBlockID(self, varID):
        # 未验证？
        # varJs = 'document.getElementById("filePath").style.display="block"'
        return self.driver.find_element_by_id(varID).style.display



    # todo True or False

    def isElement(self, varPath):

        '''
        通过Xpath方式检查元素是否存在
        :param varPath:
        :return:
        '''

        flag = False
        try:
            self.find_element(*(By.XPATH, varPath))
            # self.driver.find_element_by_xpath(varPath)
            flag = True
        except:
            flag = False
        return flag

    def isElementAttr(self, varPath, varAttr):

        '''
        通过Xpath方式判断元素属性是否存在
        :param varPath:
        :return:
        '''
        element = self.find_element(*(By.XPATH, varPath))
        if element.has_attribute(varAttr):
            return True
        else:
            return False



    def isElementByAttr(self, varPath, varAttr, varValue):

        '''
        通过Xpath方式检查特定属性的元素是否存在
        :param varPath:  //tr
        :param varAttr:  href
        :param varContain:  http://
        :return:
        '''

        flag = False
        try:
            for a in self.find_elements(*(By.XPATH, varPath)):
                if varValue == a.get_attribute(varAttr):
                    flag = True
                    break
        except:
            flag = False
        return flag

    def isElementById(self, varId):

        '''
        通过Id方式检查元素是否存在
        :param varId:
        :return:
        '''

        flag = False
        try:
            self.find_element(*(By.ID, varId))
            # self.driver.find_element_by_id(varId)
            flag = True
        except:
            flag = False
        return flag

    def isElementByName(self, varName):

        '''
        通过Name方式检查元素是否存在
        :param varName:
        :return:
        '''
        flag = False
        try:
            self.find_element(*(By.NAME, varName))
            # self.driver.find_element_by_name(varName)
            flag = True
        except:
            flag = False
        return flag

    def isElementByPartialText(self, varPartText):

        '''
        通过超链接方式检查文本是否包含varText
        :param varPartText:
        :return:
        '''

        flag = False
        try:
            self.driver.find_element_by_partial_link_text(varPartText)
            flag = True
        except:
            flag = False
        return flag

    def isElementByLinkText(self, varText):

        '''
        通过超链接方式检查文本是否存在
        :param varText:
        :return:
        '''

        flag = False
        try:
            self.driver.find_element_by_link_text(varText)
            flag = True
        except:
            flag = False
        return flag

    def isElementText(self, varPath, varText):

        '''
        通过文本比对检查文本是否存在
        :param varPath:
        :param varText:
        :return:
        '''

        flag = False
        try:
            if self.find_element(*(By.XPATH, varPath)).text == varText:
            # if self.driver.find_element_by_xpath(varPath).text == varText:
                flag = True
        except:
            flag = False
        return flag



    def isElementVisibleXpath(self, element):
        # 未验证？？？
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
        # 定位到某元素???
        try:
            elements = self.find_element(*(By.XPATH, varPath))
            actions = ActionChains(self.driver)
            actions.move_to_element(elements).perform()
            sleep(t)
        except:
            return None



    # todo alert(system)

    def alertAccept(self):

        '''
        点击弹框中的确认
        :return:
        '''

        alert = self.driver.switch_to.alert
        alert.accept()

    def alertDismiss(self):

        '''
        点击弹框中的取消
        :return:
        '''

        alert = self.driver.switch_to.alert
        alert.dismiss()

    def alertText(self):

        '''
        获取弹框中的文案
        :return:
        '''

        alert = self.driver.switch_to.alert
        return alert.text




