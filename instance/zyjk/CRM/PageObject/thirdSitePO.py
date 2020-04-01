# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2018-3-15
# Description: 对象库
#***************************************************************

from PO.LevelPO import *
from PO.mysqlPO import *
mysql_PO = MysqlPO("192.168.0.39", "ceshi", "123456", "TD_APP")
from PO.webdriverPO import *
from PO.LevelPO import *
from pytesseract import *
from PIL import Image
# import cv2     //pip3 install opencv-python


class ThirdSitePO(object):

    # def __init__(self, Level_PO):
    #      self.Level_PO = Level_PO

    # 1、国药控股股份有限公司 （pass）
    def gy(self, varRow):
        webdriver_PO = WebdriverPO("chrome")
        webdriver_PO.open(varRow[3])
        level_PO = LevelPO(webdriver_PO.driver)
        level_PO.inputName("txtUser", varRow[5])
        level_PO.inputName("txtPwd", varRow[6])
        level_PO.clickXpath("//input[@name='ibtnOk']", 2)
        level_PO.clickXpath("//a[@id='tvMenut2']", 2)
        level_PO.inIframe("frameid_tab_702", 2)
        level_PO.inputIdClear("txtPageSize", 99999)
        level_PO.clickXpath("//input[@name='btnQuery']", 2)
        l = []
        s = b = 0
        l = level_PO.getXpathsAttr("//table[@id='gvQueryResult_DXMainTable']/tbody/tr", "class")
        level_PO.outIframe(2)
        webdriver_PO.close()
        for i in range(len(l)):
            if l[i] == "dxgvDataRow":
                s = s + 1
        print(str(varRow) + "，库存小计：" + str(s))
        return s, b

    # 3、雷允上医药有限公司 （pass）
    def lys(self, varRow):
        webdriver_PO = WebdriverPO("chrome")
        webdriver_PO.open(varRow[3])
        webdriver_PO.driver.maximize_window()  # 全屏
        level_PO = LevelPO(webdriver_PO.driver)
        level_PO.inputId("UserName", varRow[5])
        level_PO.inputId("PassWord", varRow[6])
        level_PO.clickXpath("//input[@id='LgoinButton']", 2)
        level_PO.clickXpath("//span[@id='ListTreeLabel']/li[2]/div", 2)
        level_PO.clickLinktext("当月库存和批号查询", 2)
        level_PO.inIframe("myFrameId", 2)
        l = []
        s = b = 0
        l = level_PO.getXpathsAttr("//table[@id='changetable']/tbody/tr", "class")
        level_PO.outIframe(2)
        webdriver_PO.close()
        for i in range(len(l)):
            if l[i] == "stock":
                s = s + 1
        print(str(varRow) + "，库存小计：" + str(s))
        return s, b

    # 4,华东医药股份有限公司(有验证码，数据量少，有待观察)
    def hdyy(self, varRow):
        webdriver_PO = WebdriverPO("chrome")
        webdriver_PO.open(varRow[3])
        webdriver_PO.driver.maximize_window()  # 全屏
        webdriver_PO.driver.get_screenshot_as_file("D://51//python//project//instance//zyjk//CRM//web//default.png")
        level_PO = LevelPO(webdriver_PO.driver)
        img = cv2.imread('D://51//python//project//instance//zyjk//CRM//web//default.png')
        cropImg = img[(366):(391), (800):(875)]
        cv2.imwrite('D://51//python//project//instance//zyjk//CRM//web//code.png', cropImg)
        image = Image.open("code.png")
        code = pytesseract.image_to_string(image)
        level_PO.inputId("txtusername", varRow[5])
        level_PO.inputId("txtpassword", varRow[6])
        level_PO.inputId("txtcheck", code)
        if level_PO.isElementText("//li[@class='xians']", "验证码不正确") or level_PO.isElementText("//li[@class='xians']", "验证码不能为空"):
            for i in range(10):
                if level_PO.isElementText("//li[@class='xians']", "验证码不正确") or level_PO.isElementText("//li[@class='xians']", "验证码不能为空"):
                    img = cv2.imread('D://51//python//project//instance//zyjk//CRM//web//default.png')
                    cropImg = img[(366):(391), (800):(875)]
                    cv2.imwrite('D://51//python//project//instance//zyjk//CRM//web//code.png', cropImg)
                    image = Image.open("code.png")
                    code = pytesseract.image_to_string(image)
                    level_PO.inputId("txtcheck", code)
        level_PO.clickId("btnlogin", 2)
        level_PO.clickXpath("//a[@href='Flow_Stock.aspx']", 2)  # 库存查询
        level_PO.clickId("ContentPlaceHolder3_btnselect", 2)  # 查询
        l = []
        s = b = 0
        l = level_PO.getXpathsText("//table[@id='ContentPlaceHolder3_MyGridView']/tbody/tr")
        webdriver_PO.close()
        s = len(l) - 1
        print(str(varRow) + "，库存小计：" + str(s))
        return s, b

    # 5，杭州萧山医药有限公司(pass)
    def hzxs(self, varRow):
        webdriver_PO = WebdriverPO("chrome")
        webdriver_PO.open(varRow[3])
        webdriver_PO.driver.maximize_window()  # 全屏
        webdriver_PO.driver.get_screenshot_as_file("D://51//python//project//instance//zyjk//CRM//web//default.png")
        level_PO = LevelPO(webdriver_PO.driver)
        img = cv2.imread('D://51//python//project//instance//zyjk//CRM//web//default.png')
        cropImg = img[(458):(496), (1025):(1097)]
        cv2.imwrite('D://51//python//project//instance//zyjk//CRM//web//code.png', cropImg)
        image = Image.open("code.png")
        code = pytesseract.image_to_string(image)
        level_PO.inputId("UserName", varRow[5])
        level_PO.inputId("PassWord", varRow[6])
        level_PO.inputId("vcode", code)
        level_PO.clickId("login", 2)
        if level_PO.isElementText("//div[@id='LoginBar']/ul/span/font", "验证码错误,请重新输入"):
            for i in range(10):
                if level_PO.isElementText("//div[@id='LoginBar']/ul/span/font", "验证码错误,请重新输入"):
                    webdriver_PO.driver.get_screenshot_as_file(
                        "D://51//python//project//instance//zyjk//CRM//web//default.png")
                    img = cv2.imread('D://51//python//project//instance//zyjk//CRM//web//default.png')
                    cropImg = img[(458):(496), (1025):(1097)]
                    cv2.imwrite('D://51//python//project//instance//zyjk//CRM//web//code.png', cropImg)
                    image = Image.open("code.png")
                    code = pytesseract.image_to_string(image)
                    level_PO.inputId("PassWord", varRow[6])
                    level_PO.inputId("vcode", code)
                    level_PO.clickId("login", 2)
        level_PO.inIframe("mainFrame", 2)
        level_PO.clickXpath("//div[@id='NavManagerMenu']/ul/li[3]/div/cite/a", 2)  # 网上查询
        level_PO.clickLinktext("商品库存查询", 2)
        level_PO.inIframe("main", 2)
        level_PO.inIframe("conditionframe", 2)
        level_PO.clickId("btnQuery", 2)
        level_PO.inIframeTopDivParent(2)
        level_PO.inIframe("reportframe", 2)
        s = webdriver_PO.driver.page_source
        s = len(str(s).split("更新时间")[1].split("ReportViewerControl_ctl09_ReportArea")[0].split("HEIGHT:5.33mm")) - 1
        webdriver_PO.close()
        print(str(varRow) + "，库存小计：" + str(s))
        b = 0
        return s, b

    # 8，温州英特医药有限公司
    def wzyt(self, varRow):
        webdriver_PO = WebdriverPO("chrome")
        webdriver_PO.open(varRow[3])
        webdriver_PO.driver.maximize_window()  # 全屏
        level_PO = LevelPO(webdriver_PO.driver)
        level_PO.inputId("txtUserName", varRow[5])
        level_PO.inputId("txtPwd", varRow[6])
        level_PO.clickId("submit", 2)
        level_PO.inIframeXpth("//frame[@name='leftFrame']", 2)
        level_PO.clickLinktext("采购库存", 2)
        level_PO.inIframeTopDivParent(2)
        level_PO.inIframeXpth("//frame[@name='main']", 2)
        level_PO.clickId("btnExport", 2)  # 所有库存明细
        l = []
        s = b = 0
        l = level_PO.getXpathsAttr("//table[@id='gvStockList']/tbody/tr", "class")
        webdriver_PO.close()
        for i in range(len(l)):
            if l[i] == "left_txt":
                s = s + 1
        print(str(varRow) + "，库存小计：" + str(s))
        return s, b

    # 9，华东岱山医药有限公司 (pass)
    def hdds(self, varRow):
        webdriver_PO = WebdriverPO("chrome")
        webdriver_PO.open(varRow[3])
        webdriver_PO.driver.maximize_window()  # 全屏
        webdriver_PO.driver.get_screenshot_as_file("D://51//python//project//instance//zyjk//CRM//web//default.png")
        img = cv2.imread('D://51//python//project//instance//zyjk//CRM//web//default.png')
        cropImg = img[(458):(496), (1025):(1097)]
        cv2.imwrite('D://51//python//project//instance//zyjk//CRM//web//code.png', cropImg)
        image = Image.open("code.png")
        code = pytesseract.image_to_string(image)
        level_PO = LevelPO(webdriver_PO.driver)
        level_PO.inputId("UserName", varRow[5])
        level_PO.inputId("PassWord", varRow[6])
        level_PO.inputId("vcode", code)
        level_PO.clickId("login", 2)
        if level_PO.isElementText("//div[@id='LoginBar']/ul/span/font", "验证码错误,请重新输入"):
            for i in range(10):
                if level_PO.isElementText("//div[@id='LoginBar']/ul/span/font", "验证码错误,请重新输入"):
                    webdriver_PO.driver.get_screenshot_as_file(
                        "D://51//python//project//instance//zyjk//CRM//web//default.png")
                    img = cv2.imread('D://51//python//project//instance//zyjk//CRM//web//default.png')
                    cropImg = img[(458):(496), (1025):(1097)]
                    cv2.imwrite('D://51//python//project//instance//zyjk//CRM//web//code.png', cropImg)
                    image = Image.open("code.png")
                    code = pytesseract.image_to_string(image)
                    level_PO.inputId("PassWord", varRow[6])
                    level_PO.inputId("vcode", code)
                    level_PO.clickId("login", 2)
        level_PO.inIframe("mainFrame", 2)
        level_PO.clickXpath("//div[@id='NavManagerMenu']/ul/li[3]/div/cite/a", 2)  # 网上查询

        # 库存
        level_PO.clickLinktext("批号库存查询", 2)
        level_PO.inIframe("main", 2)
        level_PO.inIframe("conditionframe", 2)
        level_PO.clickId("btnQuery", 2)  # 开始搜索
        level_PO.inIframeTopDivParent(2)
        level_PO.inIframe("reportframe", 2)
        s = webdriver_PO.driver.page_source
        s = len(str(s).split("更新时间")[1].split("ReportViewerControl_ctl09_ReportArea")[0].split("HEIGHT:5.33mm")) - 1
        level_PO.inIframeTopDivParent(2)
        level_PO.inIframeTopDivParent(2)

        # 采购
        level_PO.clickLinktext("批号流量流向", 2)
        level_PO.inIframe("main", 2)
        level_PO.inIframe("conditionframe", 2)
        level_PO.inputIdClear("BeginTime", "")  # 清空 开始时间
        level_PO.selectIdValue("dropBizType", "1A")  # 选择 进货
        level_PO.clickId("btnQuery", 2)  # 开始搜索
        level_PO.inIframeTopDivParent(2)
        level_PO.inIframe("reportframe", 2)
        b = webdriver_PO.driver.page_source
        b = len(str(b).split("更新日期")[1].split("ReportViewerControl_ctl09_ReportArea")[0].split("HEIGHT:5.00mm")) - 2

        webdriver_PO.close()
        print(str(varRow) + "，库存小计：" + str(s))
        return s, b

        # varName = varName.split("，")[1]
        # mysql_PO.cur.execute('select count(id) from data_stock where business="%s"' % (varName))
        # s1 = mysql_PO.cur.fetchone()
        # if int(s) == int(s1[0]):
        #     print("OK，库存，第三方平台合计：" + str(s) + "，我方爬取合计：" + str(s1[0]))
        # else:
        #     print("errorrrrrrrrrrr，库存，第三方平台合计：" + str(s) + "，我方爬取合计：" + str(s1[0]))
        #
        # mysql_PO.cur.execute('select count(id) from data_buy where business="%s"' % (varName))
        # b1 = mysql_PO.cur.fetchone()
        # if int(b) == int(b1[0]):
        #     print("OK，采购，第三方平台合计：" + str(b) + "，我方爬取合计：" + str(b1[0]))
        # else:
        #     print("errorrrrrrrrrrr，采购，第三方平台合计：" + str(b) + "，我方爬取合计：" + str(b1[0]))

        print("*" * 100)

    # 7，舟山英特卫盛医药有限公司
    def zsytws(self, varRow):
        webdriver_PO = WebdriverPO("chrome")
        webdriver_PO.open(varRow[3])
        handle = webdriver_PO.driver.current_window_handle
        webdriver_PO.driver.maximize_window()  # 全屏
        level_PO = LevelPO(webdriver_PO.driver)
        level_PO.inputName("username", varRow[5])
        level_PO.inputName("password", varRow[6])
        level_PO.clickXpath("//input[@name='verifyCode']", 2)
        webdriver_PO.driver.get_screenshot_as_file("D://51//python//project//instance//zyjk//CRM//web//default.png")
        img = cv2.imread('D://51//python//project//instance//zyjk//CRM//web//default.png')
        cropImg = img[(12):(35), (909):(979)]
        cv2.imwrite('D://51//python//project//instance//zyjk//CRM//web//code.png', cropImg)
        image = Image.open("code.png")
        code = pytesseract.image_to_string(image)
        level_PO.inputName("verifyCode", code)
        level_PO.clickXpath("//input[@name='Submit']", 2)
        level_PO.clickLinktext("流向查询", 2)
        handles = webdriver_PO.driver.window_handles
        for n in handles:
            if n != handle:
                webdriver_PO.driver.switch_to.window(n)
        level_PO.clickLinktext("药品流向查询", 2)
        level_PO.inIframe("cwin", 2)


        # 库存
        level_PO.clickId("button_2", 2)  # 库存明细
        level_PO.clickXpath("//input[@name='searchBtn']", 4)  # 搜索
        level_PO.inIframe("tabFrame", 2)
        x = level_PO.getXpathsText("//td")
        s = str(x).split(", '共")[1].split("条")[0]
        level_PO.inIframeTopDivParent(2)

        # 采购
        level_PO.clickId("button_3", 2)  # 进货明细
        level_PO.inputIdClear("startTime","")   # 清空 开始时间。
        level_PO.clickXpath("//input[@name='searchBtn']", 4)  # 搜索
        level_PO.inIframe("tabFrame", 2)
        x = level_PO.getXpathsText("//td")
        b = str(x).split(", '共")[1].split("条")[0]
        # print("第三方平台 库存合计：" + str(s) + " , " + "采购合计：" + str(b))
        webdriver_PO.close()

        print(str(varRow) + "，库存小计：" + str(s))
        return s, b

        # varName = varName.split("，")[1]
        # mysql_PO.cur.execute('select count(id) from data_stock where business="%s"' % (varName))
        # s1 = mysql_PO.cur.fetchone()
        # if int(s) == int(s1[0]):
        #     print("OK，库存，第三方平台合计：" + str(s) + "，我方爬取合计：" + str(s1[0]))
        # else:
        #     print("errorrrrrrrrrrr，库存，第三方平台合计：" + str(s) + "，我方爬取合计：" + str(s1[0]))
        #
        # mysql_PO.cur.execute('select count(id) from data_buy where business="%s"' % (varName))
        # b1 = mysql_PO.cur.fetchone()
        # if int(b) == int(b1[0]):
        #     print("OK，采购，第三方平台合计：" + str(b) + "，我方爬取合计：" + str(b1[0]))
        # else:
        #     print("errorrrrrrrrrrr，采购，第三方平台合计：" + str(b) + "，我方爬取合计：" + str(b1[0]))


    # 2，上药控股有限公司(pass)
    def sy(self, varName, varURL, varUser, varPass):
        webdriver_PO = WebdriverPO("chrome")
        webdriver_PO.open(varURL)
        handle = webdriver_PO.driver.current_window_handle
        webdriver_PO.driver.maximize_window()  # 全屏
        webdriver_PO.driver.get_screenshot_as_file("D://123.png")
        img = cv2.imread('D://123.png')
        cropImg = img[(452):(452 + 40), (1480):(1480 + 130)]
        cv2.imwrite('D://51//python//project//instance//zyjk//CRM//web//333.png', cropImg)
        image = Image.open("333.png")
        code = pytesseract.image_to_string(image)
        level_PO = LevelPO(webdriver_PO.driver)
        level_PO.inputId("username", varUser)
        level_PO.inputId("password", varPass)
        level_PO.inputId("captcha", code)
        level_PO.clickXpath("//input[@name='submit']", 2)
        if level_PO.isElementId("msg"):
            for i in range(10):
                if level_PO.isElementId("msg"):
                    webdriver_PO.driver.get_screenshot_as_file("D://123.png")
                    img = cv2.imread('D://123.png')
                    cropImg = img[(452):(452 + 40), (1480):(1480 + 130)]
                    cv2.imwrite('D://51//python//project//instance//zyjk//CRM//web//333.png', cropImg)
                    image = Image.open("333.png")
                    code = pytesseract.image_to_string(image)
                    level_PO.inputId("password", varPass)
                    level_PO.inputId("captcha", code)
                    level_PO.clickXpath("//input[@name='submit']", 2)
        level_PO.clickXpath("//input[@value='请用鼠标点我']", 1)
        level_PO.clickXpath("//div[@class='maskDiv3']/div/input", 1)
        level_PO.clickXpath("//input[@value='开始使用']", 2)
        level_PO.clickXpath("//a[@href='/cas-webapp-portal/main/system_mysystem.do']", 2)  # 我的应用
        js = 'window.open("http://report10.shaphar.com/WebReport/decision?portalname=565743327E5B988A0A6FE8364F3D0860");'
        webdriver_PO.driver.execute_script(js)  # 打开新标签页
        handles = webdriver_PO.driver.window_handles
        for n in handles:
            if n != handle:
                webdriver_PO.driver.switch_to.window(n)  # 切换到新标签页
        level_PO.clickXpath("//div[@class='bi-custom-tree bi-loader bi-vertical-layout']/div/div[1]/div", 2)

        print(varName + "(" + varURL + ", " + varUser + ", " + varPass + ")")

        # 库存
        level_PO.clickXpath("//div[@class='bi-custom-tree bi-loader bi-vertical-layout']/div/div[1]/div[2]/div/div[2]/div",2)  # 产品历史库存查询
        level_PO.inIframeXpth("//iframe[@src='/WebReport/decision/v10/entry/access/old-platform-reportlet-entry-2157?dashboardType=5&width=1296&height=692']",2)
        # level_PO.inputXpath("//div[@class='pmeter-container fr-absolutelayout ui-state-enabled']/div[6]/div[1]/input", "上药控股有限公司")  # 子公司选择：上药控股有限公司
        level_PO.clickXpath("//div[@id='fr-btn-FORMSUBMIT0']", 2)  # 查询
        sleep(6)
        s = webdriver_PO.driver.page_source
        s = str(s).split("row=")[-1]
        # print(s)
        s = str(s).split('"')[1].split('"')[0]
        s = int(s) - 2

        level_PO.inIframeTopDivParent(2)

        # 采购
        level_PO.clickXpath(
            "//div[@class='bi-custom-tree bi-loader bi-vertical-layout']/div/div[1]/div[2]/div/div[3]/div", 2)  # 采购业务查询
        level_PO.inIframeXpth(
            "//iframe[@src='/WebReport/decision/v10/entry/access/old-platform-reportlet-entry-2158?dashboardType=5&width=1296&height=692']",
            2)
        level_PO.clickXpath("//div[@id='fr-btn-FORMSUBMIT0']", 2)  # 查询
        sleep(65)
        if level_PO.isElementXpath("//div[@id='fr-btn-Last']/div/em/button"):
            level_PO.clickXpath("//div[@id='fr-btn-Last']/div/em/button", 2)  # 末页
        b = webdriver_PO.driver.page_source
        b = str(b).split("row=")[-1]
        # print(b)
        b = str(b).split('"')[1].split('"')[0]
        b = int(b)

        varName = varName.split("，")[1]
        mysql_PO.cur.execute('select count(id) from data_stock where business="%s"' % (varName))
        s1 = mysql_PO.cur.fetchone()
        if int(s) == int(s1[0]):
            print("OK，库存，第三方平台合计：" + str(s) + "，我方爬取合计：" + str(s1[0]))
        else:
            print("errorrrrrrrrrrr，库存，第三方平台合计：" + str(s) + "，我方爬取合计：" + str(s1[0]))

        mysql_PO.cur.execute(
            'select count(id) from data_buy where business="%s" and buy_time>"%s"' % (varName, varDate))
        b1 = mysql_PO.cur.fetchone()
        if int(b) == int(b1[0]):
            print("OK，采购，第三方平台合计：" + str(b) + "，我方爬取合计：" + str(b1[0]))
        else:
            print("errorrrrrrrrrrr，采购，第三方平台合计：" + str(b) + "，我方爬取合计：" + str(b1[0]))

        print("*" * 100)

    # 6，湖州英特药谷有限公司 （？）
    def hzytyg(self, varName, varURL, varUser, varPass):
        webdriver_PO = WebdriverPO("chrome")
        webdriver_PO.open(varURL)
        handle = webdriver_PO.driver.current_window_handle
        webdriver_PO.driver.maximize_window()  # 全屏
        webdriver_PO.driver.get_screenshot_as_file("D://123.png")
        img = cv2.imread('D://123.png')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        cropImg = img[(445):(475), (1273):(1366)]
        cv2.imwrite('D://51//python//project//instance//zyjk//CRM//web//333.png', cropImg)

        image = Image.open("D://51//python//project//instance//zyjk//CRM//web//333.png")
        # code = pytesseract.image_to_string(image)
        code = pytesseract.image_to_string(image, lang='num')  # 训练的数字库
        import numpy as np
        image = np.asarray(image)
        image = (image > 135) * 255
        image = Image.fromarray(image).convert('RGB')
        image.show()
        image.save('D://51//python//project//instance//zyjk//CRM//web//3334.png')

        print(code)
        print("1111111111")

        sleep(1212)

        level_PO = LevelPO(webdriver_PO.driver)
        level_PO.inputId("username", varUser)
        level_PO.inputId("password", varPass)
        level_PO.inputId("captcha", code)
        level_PO.clickXpath("//input[@name='submit']", 2)
        if level_PO.isElementId("msg"):
            for i in range(10):
                if level_PO.isElementId("msg"):
                    webdriver_PO.driver.get_screenshot_as_file("D://123.png")
                    img = cv2.imread('D://123.png')
                    cropImg = img[(452):(452 + 40), (1480):(1480 + 130)]
                    cv2.imwrite('D://51//python//project//instance//zyjk//CRM//web//333.png', cropImg)
                    image = Image.open("333.png")
                    code = pytesseract.image_to_string(image)
                    level_PO.inputId("password", varPass)
                    level_PO.inputId("captcha", code)
                    level_PO.clickXpath("//input[@name='submit']", 2)
        level_PO.clickXpath("//input[@value='请用鼠标点我']", 1)
        level_PO.clickXpath("//div[@class='maskDiv3']/div/input", 1)
        level_PO.clickXpath("//input[@value='开始使用']", 2)
        level_PO.clickXpath("//a[@href='/cas-webapp-portal/main/system_mysystem.do']", 2)  # 我的应用
        js = 'window.open("http://report10.shaphar.com/WebReport/decision?portalname=565743327E5B988A0A6FE8364F3D0860");'
        webdriver_PO.driver.execute_script(js)  # 打开新标签页
        handles = webdriver_PO.driver.window_handles
        for n in handles:
            if n != handle:
                webdriver_PO.driver.switch_to.window(n)  # 切换到新标签页
        level_PO.clickXpath("//div[@class='bi-custom-tree bi-loader bi-vertical-layout']/div/div[1]/div", 2)
        level_PO.clickXpath(
            "//div[@class='bi-custom-tree bi-loader bi-vertical-layout']/div/div[1]/div[2]/div/div[2]/div", 2)
        level_PO.inIframeXpth(
            "//iframe[@src='/WebReport/decision/v10/entry/access/old-platform-reportlet-entry-2157?dashboardType=5&width=1296&height=692']",
            2)
        # level_PO.inputXpath("//div[@class='pmeter-container fr-absolutelayout ui-state-enabled']/div[6]/div[1]/input", "上药控股有限公司")  # 子公司选择：上药控股有限公司
        level_PO.clickXpath("//div[@id='fr-btn-FORMSUBMIT0']", 2)  # 查询
        sleep(6)
        s = webdriver_PO.driver.page_source
        s = str(s).split("row=")[-1]
        # print(s)
        s = str(s).split('"')[1].split('"')[0]
        s = int(s) - 2
        print(varName)
        print(varURL + ", " + varUser + ", " + varPass + " 小计数量：" + str(s))
        varName = varName.split("，")[1]
        mysql_PO.cur.execute('select count(id) from data_stock where business="%s"' % (varName))
        t1 = mysql_PO.cur.fetchone()
        if int(s) == int(t1[0]):
            print("OK，数量匹配一致。第三方平台合计数量 " + str(s) + "，我方数据库数量 " + str(t1[0]))
        else:
            print("error，数量匹配不一致。第三方平台合计数量 " + str(s) + "，我方数据库数量 " + str(t1[0]))
        print("*" * 100)


class Browser(object):

    def openWeb(self, varURL):
        webdriver_PO = WebdriverPO("chrome")
        webdriver_PO.open(varURL)
        webdriver_PO.driver.maximize_window()  # 全屏


