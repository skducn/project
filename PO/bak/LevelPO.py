# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2016-7-29
# Description: LevelPO对象层，定义元素与封装对象
# selenium expected_conditions使用实例 https://blog.csdn.net/yzl11/article/details/52901946?locationNum=2&fps=1
# 顺序：1input，2click，3get，4print，5checkbox，6select，7iframe，8js，9color，10exist
#***************************************************************

import platform
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from PO.BasePage import BasePage

class LevelPO(BasePage):

    '''[ INPUT ]'''

    def inputId(self, dimId, dimContent):
        try:
            self.find_element(*(By.ID, dimId)).send_keys(dimContent)
        except:
            return u"error"

    def inputName(self, varName, dimContent):
        try:
            self.find_element(*(By.NAME, varName)).send_keys(dimContent)
        except:
            return u"error"

    def inputNameClear(self, varName, dimContent):
        try:
            self.find_element(*(By.NAME, varName)).clear()
            self.find_element(*(By.NAME, varName)).send_keys(dimContent)
        except:
            return u"error"

    def inputXpath(self, varXPath, dimContent):
        try:
            self.find_element(*(By.XPATH, varXPath)).send_keys(dimContent)
        except:
            return u"error"

    def inputXpathEnter(self, varXPath, dimContent):
        try:
            self.find_element(*(By.XPATH, varXPath)).send_keys(dimContent)
            self.find_element(*(By.XPATH, varXPath)).send_keys(Keys.ENTER)
        except:
            return u"error"

    def inputXpathClear(self, varXPath, dimContent):
        try:
            self.find_element(*(By.XPATH, varXPath)).clear()
            self.find_element(*(By.XPATH, varXPath)).send_keys(dimContent)
        except:
            return u"error"

    def inputXpathClearEnter(self, varXPath, dimContent):
        try:
            self.find_element(*(By.XPATH, varXPath)).clear()
            self.find_element(*(By.XPATH, varXPath)).send_keys(dimContent)
            self.find_element(*(By.XPATH, varXPath)).send_keys(Keys.ENTER)
            sleep(2)
        except:
            return u"error"

    def inputIdClear(self, dimId, dimContent):
        try:
            self.find_element(*(By.ID, dimId)).clear()
            self.find_element(*(By.ID, dimId)).send_keys(dimContent)
        except:
            return u"error"


    '''[ 2click ]'''

    def clickId(self, dimId, t):
        try:
            self.find_element(*(By.ID, dimId)).click()
            sleep(t)
        except:
            return u"error"

    def clickLinktext(self, dimContent, t):
        try:
            self.find_element(*(By.LINK_TEXT, dimContent)).click()
            sleep(t)
        except:
            return u"error"

    def clickLinkstext(self, dimContent, t):
        try:
            for a in self.find_elements(*(By.LINK_TEXT, dimContent)):
                a.click()
            sleep(t)
        except:
            return u"error"

    def clickTagname(self, dimContent, t):
        # Level_PO.clickTagname(u"test", 2)
        try:
            self.find_element(*(By.TAG_NAME, dimContent)).click()
            sleep(t)
        except:
            return u"error"

    def clickXpath(self, dimPath, t):
        # Level_PO.clickXpath(u"//button[@ng-click='action.callback()']", 2)
        try:
            self.find_element(*(By.XPATH, dimPath)).click()
            sleep(t)
        except:
            return u"error"

    def clickXpathEnter(self, dimPath, t):
        try:
            self.find_element(*(By.XPATH, dimPath)).send_keys(Keys.ENTER)
            sleep(t)
        except:
            return u"error"


    def clickXpaths(self, dimPath, t):
        # 遍历dimPath
        # self.Level_PO.clickXpaths("//a[contains(@href,'1194')]", 2)  , 表示遍历所有a 中href属性内容包含1194字符串的连接。
        try:
            for a in self.find_elements(*(By.XPATH, dimPath)):
                a.click()
                sleep(t)
        except:
            return u"error"

    def clickXpathsNum(self, dimPath, dimNum, t):
        # 遍历同一属性的多个click，点击第varNum个。
        # Level_PO.clickXpathsNum(u"//button[@ng-click='action.callback()']", 5, 2)  ，表示遍历后点击第五个连接。
        try:
            c = 0
            for a in self.find_elements(*(By.XPATH, dimPath)):
                c = c + 1
                if c == dimNum:
                    a.click()
                    break
            sleep(t)
        except:
            return u"error"

    def clickXpathsTextContain(self, dimPath, dimContain, t):
        # 遍历dimPath，点击text中包含某内容的连接。
        # self.Level_PO.clickXpathsTextContain("//td[@aria-describedby='gridTable_run_name']/a", '20190506059', 2)
        try:
            for a in self.find_elements(*(By.XPATH, dimPath)):
                if dimContain in a.text:
                    a.click()
                    break
            sleep(t)
        except:
            return u"error"

    def clickXpathsContain(self, dimPath, dimAttr, dimContain, t):
        # 遍历dimPath，点击属性dimAttr中包含某内容的连接。
        # self.Level_PO.clickXpathsContain("//a", "href", '1194', 2)
        try:
            for a in self.find_elements(*(By.XPATH, dimPath)):
                # print(a.get_attribute(dimAttr))
                if dimContain in a.get_attribute(dimAttr):
                    a.click()
                    break
            sleep(t)
        except:
            return u"error"

    def clickXpathsConfirm(self, dimPath, dimPath2, t):
        # 遍历链接click后二次确认
        try:
            for a in self.find_elements(*(By.XPATH, dimPath)):
                a.click()
                sleep(t)
                self.find_element(*(By.XPATH, dimPath2)).click()
                sleep(t)
        except:
            return u"error"

    def floatXpath(self, dimPath,dimPath2,t):
        try:
            elements = self.find_element(*(By.XPATH, dimPath))
            actions = ActionChains(self.driver)
            actions.move_to_element(elements).perform()
            yy = self.find_element(*(By.XPATH, dimPath2))
            yy.click()
            sleep(t)
        except:
            return u"error"

    def clickXpathRight(self, dimPath, varId):
        try:
            xx = self.find_element(*(By.XPATH, dimPath))
            yy = self.find_element(*(By.ID, varId))
            ActionChains(self.driver).drag_and_drop(xx,yy).perform()
            # ActionChains(self.driver).dra
            # print "end"
            ActionChains(self.driver).click_and_hold(xx).perform()
            # perform()
            # ActionChains(self.driver).click
            ActionChains(self.driver).move_to_element(self.find_element(*(By.ID, varId)))
        except:
            return u"error"

    def clickXpathsXpath(self, dimPaths, dimContain, dimPath2, t):
        # 遍历后，点击同一个xpath
        try:
            for a in self.find_elements(*(By.XPATH, dimPaths)):
                a.find_element(*(By.XPATH, dimPath2))
                if dimContain in a.text:
                    break
                # self.find_element(*(By.XPATH, dimPath2)).click()
                sleep(t)
        except:
            return u"error"

    '''[ 3get ]'''

    def getXpathText(self, dimPath):
        # Level_PO.getXpathText(u"//input[@class='123']")
        try:
            return self.find_element(*(By.XPATH, dimPath)).text
        except:
            return u"error"

    def getXpathsText(self, dimPaths):
        # Level_PO.getXpathsText(u"//tr")
        try:
            l = []
            for a in self.find_elements(*(By.XPATH, dimPaths)):
                l.append(a.text)
            return l
        except:
            return []

    def getXpathsTextRow(self, dimPaths, dimContent):
        # 遍历获取text在第几行
        # Level_PO.getXpathsRow(u"//tr", u"test") ， 如 3 ，表示test在第3个tr里 ， 如未找到返回 -1
        r = 0
        try:
            for a in self.find_elements(*(By.XPATH, dimPaths)):
                r = r + 1
                if a.text == dimContent:
                    return r
            return -1
        except:
            return u"error"

    def getXpathsPartTextRow(self, dimPaths, dimPartContent):
        # 遍历获取 模糊text在第几行
        # Level_PO.getXpathsPartTextRow(u"//tr", u"test")
        r = 0
        try:
            for a in self.find_elements(*(By.XPATH, dimPaths)):
                r = r + 1
                if dimPartContent in a.text:
                    return r
            return -1
        except:
            return u"error"

    def getXpathAttr(self, dimPath, dimAttr):
        # 获取属性
        # Level_PO.getXpathAttr(u"//input[@class='123']",u"value")
        try:
            return self.find_element(*(By.XPATH, dimPath)).get_attribute(dimAttr)
        except:
            return u"error"

    def getXpathsNums(self, dimPaths):
        # 遍历获取数量。
        # Level_PO.getXpathsNums("//tr")
        s = 0
        try:
            for a in self.find_elements(*(By.XPATH, dimPaths)):
                s = s + 1
            return s
        except:
            return u"error"

    def getXpathsAttr(self, dimPaths, dimAttr):
        # 遍历获取属性，如获取表格里数据数量。
        # Level_PO.getXpathsAttr(u"//tr", u"id")
        l = []
        try:
            for a in self.find_elements(*(By.XPATH, dimPaths)):
                l.append(a.get_attribute(dimAttr))
            return l
        except:
            return u"error"

    def getXpathsTextAttr(self, dimPaths, dimAttr):
        # 遍历获取文本与属性对应字典
        # Level_PO.getXpathsTextAttr(u"//input[@name='office_id']",u"value")
        dict1 = {}
        list1 = []
        list2 = []
        try:
            for a in self.find_elements(*(By.XPATH, dimPaths)):
                list1.append(a.text)
                list2.append(a.get_attribute(dimAttr))
            dict1 = dict(zip(list1, list2))
            return dict1
        except:
            return u"error"

    def getLinktextAttr(self, dimContent, dimAttr):
        # 功能： 获取超链接的某个属性
        # Level_PO.getLinktextAttr(u"超链接",u"href")
        try:
            return self.find_element(*(By.LINK_TEXT, dimContent)).get_attribute(dimAttr)
        except:
            return u"error"


    '''[ 4print ]'''

    def printXpathText(self, dimPath):
        # Level_PO.printXpathText("//h5")
        try:
            print(self.find_element(*(By.XPATH, dimPath)).text)
        except:
            return u"error"

    def printXpathsText(self, dimPaths):
        # Level_PO.printXpathsText("//tr")
        try:
            for a in self.find_elements(*(By.XPATH, dimPaths)):
                print (a.text)
        except:
            return u"error"

    def printIdTagnameText(self, dimId, dimTagname):
        # Level_PO.printIdTagnameText('navbar', "button")
        try:
            print (self.find_element(*(By.ID, dimId)).a.find_element_by_tag_name(dimTagname).text)
        except:
            return u"error"

    def printIdTagnamesText(self, dimId, dimTagname):
        # Level_PO.printIdTagnamesText('navbar', "dl")
        try:
            a = self.find_element(*(By.ID, dimId))
            varContents = a.find_elements_by_tag_name(dimTagname)
            for i in varContents:
                print (i.text)
        except:
            return u"error"

    def printXpathAttr(self, dimPath, dimAttr):
        # Level_PO.printXpathAttr(u"//input[@class="123"]",u"value")
        try:
            print (self.find_element(*(By.XPATH, dimPath)).get_attribute(dimAttr))
        except:
            return u"error"

    def printXpathsAttr(self, dimPaths, dimAttr):
        # Level_PO.printXpathsAttr(u"//tr",u"value")
        try:
            for a in self.find_elements(*(By.XPATH, dimPaths)):
                print (a.get_attribute(dimAttr))
        except:
            return u"error"

    def printLinktextAttr(self, dimContent, dimAttr):
        # Level_PO.printLinktextAttr(u"测试",u"href")
        try:
            return self.find_element(*(By.LINK_TEXT, dimContent)).get_attribute(dimAttr)
        except:
            return u"error"

    '''[ 5checkbox ]'''

    def isXpathCheckbox(self, dimPath):
        # 判断是否选中复选框 ，返回 True 或 False
        # Level_PO.getXpathCheckbox(u"//input[@class='123']")
        try:
            return self.find_element(*(By.XPATH, dimPath)).is_selected()
        except:
            return u"error"

    def clearXpathsCheckbox(self, dimPath):
        # 清空所有复选框 （不勾选）
        # Level_PO.clearXpathsCheckbox(u"//input[@type='checkbox']")
        try:
            for a in self.find_elements(*(By.XPATH, dimPath)):
                if a.is_selected() == True:
                    a.click()
        except:
            return u"error"

    '''[ 6select ]'''

    def selectNameText(self, dimName, dimText):
        # 如：Level_PO.selectNameText(u"isAvilable", u"10")
        try:
            Select(self.driver.find_element_by_name(dimName)).select_by_visible_text(dimText)
        except:
            print( u"页面中未找到'%s'选项" %(dimText))
    def selectNameValue(self, dimName, dimValue):
        # 如：Level_PO.selectNameValue(u"isAvilable", u"启动")
        try:
            Select(self.driver.find_element_by_name(dimName)).select_by_value(dimValue)
        except:
            print (u"页面中未找到'%s'选项" % (dimValue))
    def selectXpathText(self, varXpath, varText):
         # 遍历Xpath下的Option,
         # self.selectXpathText(u"//select[@regionlevel='1']", u'启用'), （一般情况 value=1 , Text=启用）
         s1 = self.driver.find_element_by_xpath(varXpath)
         l_content1 = []
         l_value1 = []
         # varContents = self.driver.find_elements_by_xpath(varByXpath + "/option")
         varContents = self.driver.find_elements_by_xpath(varXpath + "/option")
         for a in varContents:
             l_content1.append(a.text)
             l_value1.append(a.get_attribute('value'))
         d_total1 = dict(zip(l_content1, l_value1))
         for i in range(len(d_total1)):
             if sorted(d_total1.items())[i][0] == varText:
                 Select(s1).select_by_value(sorted(d_total1.items())[i][1])
                 break
    def selectIdValue(self, dimId, dimValue):
         # self.selectIdValue(u"id", u'10')  ，（一般情况 value=10 , Text=启用）
         try:
             Select(self.driver.find_element_by_id(dimId)).select_by_value(dimValue)
         except:
             print (u"页面中未找到'%s'选项" % (dimValue))
    def selectIdText(self, dimId, dimText):
         # self.selectIdText(u"id", u'启用')  ，（一般情况 value=1 , Text=启用）
         try:
             Select(self.driver.find_element_by_id(dimId)).select_by_visible_text(dimText)
         except:
             print (u"页面中未找到'%s'选项" % (dimText))
         #
         # l_content1 = []
         # l_value1 = []
         # varCount = 0
         # s1 = self.driver.find_element_by_id(varByID)
         # varContents = s1.find_elements_by_tag_name("option")
         # for a in varContents:
         #     l_content1.append(a.text)
         #     l_value1.append(a.get_attribute('value'))
         #     if a.text == varText:
         #         varCount = 1
         # if varCount == 1:
         #     d_total1 = dict(zip(l_content1, l_value1))
         #
         #     # for key in d_total1:
         #     #     print key + ":" + d_total1[key]
         #
         #     for i in range(len(d_total1)):
         #         if sorted(d_total1.items())[i][0] == varText:
         #             Select(s1).select_by_value(sorted(d_total1.items())[i][1])
         #             break
         # else:
         #     return u"error"
    def selectIdStyle(self, varByID, varText):
        # 遍历某ID的下的option (不包含 隐藏的属性，如style=display:none），获取varText对应的值
        # self.selectIdStyle(u"id", u'启用')  # （一般情况 value=1 , Text=启用）
        l_content1 = []
        l_value1 = []
        varCount = 0
        s1 = self.driver.find_element_by_id(varByID)
        varContents = s1.find_elements_by_tag_name("option")
        for a in varContents:
            if a.get_attribute('style') == "" and a.text == varText:
                l_content1.append(a.text)
                l_value1.append(a.get_attribute('value'))
                varCount = 1
        if varCount == 1:
            d_total1 = dict(zip(l_content1, l_value1))
            for i in range(len(d_total1)):
                if sorted(d_total1.items())[i][0] == varText:
                    Select(s1).select_by_value(sorted(d_total1.items())[i][1])
                    break
        else:
            return u"error"
    def selectXpathsMenu1Menu2(self, varPaths1, varMenu, varPaths2, varMenu2, t):
        # 功能：遍历级联菜单（选择一级菜单后再选择二级菜单）
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
            return u"error"
    def get_selectNAMEvalue(self, varByname, varContent):
        # 获取某select下text的value值。（下拉框，定位ByName，选择内容，text != value ）
        s1 = self.driver.find_element_by_name(varByname)
        l_content1 = []
        l_value1 = []
        varContents = self.driver.find_elements_by_xpath("//select[@name='" + varByname + "']/option")
        for a in varContents:
            l_content1.append(a.text)
            l_value1.append(a.get_attribute('value'))
        d_total1 = dict(zip(l_content1, l_value1))
        for i in range(len(d_total1)):
            if sorted(d_total1.items())[i][0] == varContent:
                value = sorted(d_total1.items())[i][1]
                return value
    def get_selectOptionValue(self, varByname, varNum):
        # 获取某个select中text的value值。
        varValue = self.driver.find_element_by_xpath(
            "//select[@name='" + varByname + "']/option[" + varNum + "]").get_attribute('value')
        return varValue

    '''[ 7iframe ]'''

    def inIframe(self, dimId, t):
        # 定位iframe的id，进入iframe
        # self.Level_PO.inIframe("layui-layer-iframe1", 1)
        self.driver.switch_to_frame(self.driver.find_element_by_id(dimId))
        sleep(t)
    def inIframeXpth(self, dimXpath, t):
        # 定位iframe的Xpath，进入iframe
        # self.Level_PO.inIframeXpth("//body[@class='gray-bg top-navigation']/div[4]/iframe", 1)
        self.driver.switch_to_frame(self.driver.find_element_by_xpath(dimXpath))
        sleep(t)
    # def inIframeTopDiv(self, varXpath, t):
    #     # 功能：定位iframe的div路径
    #     # evel_PO.inIframeDiv("[@id='showRealtime']", 2)
    #     # Home_PO.inIframeDiv("[@class='cetc-popup-content']/div", 2)
    #     iframe = self.driver.find_element_by_xpath("//div" + varXpath + "/iframe")
    #     # print iframe.get_attribute("src")
    #     self.driver.switch_to_frame(iframe)
    #     sleep(t)
    def inIframeTopDivParent(self, t):
        # 多个iframe之间切换
        # 如第一层iframe1，第二层iframe2，两者之间切换
        # self.Level_PO.inIframeTopDivParent(1)
        self.driver.switch_to.parent_frame()
        sleep(t)
    def outIframe(self, t):
        # 退出 iframe
        # self.Level_PO.outIframe(1)
        self.driver.switch_to_default_content()
        sleep(t)

    '''[ 8js ]'''

    def script(self, js, t):
        # js方式处理
        # js = 'document.querySelector("input[type=number]").value="";    //清除input输入框内哦那个
        # js = 'document.getElementById("filePath").style.display="block"'
        self.driver.execute_script(js)
        sleep(t)

    def jsRemoveReadonlyId(self, varId):
        # 定位ID，去掉js控件只读属性，一般第三方控件日期
        js = 'document.getElementById("' + varId + '").removeAttribute("readonly")'
        self.script(js, 2)

    def jsRemoveReadonlyName(self, varName):
        # 定位Name，去掉js控件只读属性，一般第三方控件日期
        # document没有getElementByName方法，只有document.getElementsByName 得到的是标签的数组；
        # 可以通过数组第一个元素获取，如 array[0]
        js = 'document.getElementsByName("' + varName + '")[0].removeAttribute("readonly")'
        self.script(js, 2)

    def jsHiddenName(self, varName):
        # 去掉js控件只读属性，一般第三方控件日期
        js = 'document.getElementsByName("' + varName + '")[0].style.display=""'
        self.script(js, 2)

    def displayBlockID(self, varID):
        # 未验证？
        return self.driver.find_element_by_id(varID).style.display


    '''[ 9color ]'''

    def printColor(self, macColor, winColor, varContent):
        if platform.system() == 'Darwin':
            print(macColor) + varContent + '\033[0m'
        if platform.system() == 'Windows':
            (eval(winColor))(varContent.encode('gb2312') + "\n")

    '''[ 10exist ]'''

    def isElementXpath(self, dimPath):
        # 通过Xpath方式检查元素是否存在
        flag = False
        try:
            self.driver.find_element_by_xpath(dimPath)
            flag = True
        except:
            flag = False
        return flag
    def isElementLinkText(self, dimText):
        # 通过超链接方式检查文本是否存在
        flag = False
        try:
            self.driver.find_element_by_link_text(dimText)
            flag = True
        except:
            flag = False
        return flag
    def isElementText(self, dimPath, dimText):
        # 通过文本比对检查文本是否存在
        flag = False
        try:
            if self.driver.find_element_by_xpath(dimPath).text == dimText:
                flag = True
        except:
            flag = False
        return flag
    def isElementId(self, dimId):
        # 通过Id方式检查元素是否存在
        flag = False
        try:
            self.driver.find_element_by_id(dimId)
            flag = True
        except:
            flag = False
        return flag
    def isElementName(self, dimName):
        # 通过Name方式检查元素是否存在
        flag = False
        try:
            self.driver.find_element_by_name(dimName)
            flag = True
        except:
            flag = False
        return flag

    def isElementPartialText(self, dimPartText):
        # 通过超链接方式检查文本是否包含varText
        flag = False
        try:
            self.driver.find_element_by_partial_link_text(dimPartText)
            flag = True
        except:
            flag = False
        return flag
    def isElementVisibleXpath(self, element):
        # 未验证？？？
        driver = self.driver
        try:
            the_element = EC.visibility_of_element_located(driver.find_element_by_partial_link_text(element))
            assert the_element(driver)
            flag = True
        except:
            flag = False
        return flag