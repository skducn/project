# coding: utf-8
#****************************************************************
# Author     : John
# Date       : 2016-7-12
# Description: 系统管理后台（http://sit2.88uka.com/admin/system/toLogin.do），WEB类函数
# sudo pip install -U selenium
#****************************************************************

import os,sys,unittest,MySQLdb,random,webbrowser,string,datetime,redis
from selenium1.webdriver.common.action_chains import ActionChains
from selenium1.webdriver.common.keys import Keys
from selenium1.webdriver.support.ui import WebDriverWait
from time import sleep
import time,Image,ImageChops

# print sys.path
# from resource.source.comparePic import *
# from resource.source import test2
# http://sit2.88uka.com/admin/system/logout.do
# bIsElementStampTime=u"%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  #20160804143447945

def webIsElement(browser,elementId):
    # 判断browser元素是否存在,不存在则返回时间戳 (默认id)
    status = False
    try:
        browser.find_element_by_id(elementId)
        status = True
    except :
        status = False
    return status

def webIsElementPath(browser,elementPath):
    # 判断browser元素是否存在,不存在则返回时间戳 (xpath)
    status = False
    try:
        browser.find_element_by_xpath(elementPath)
        status = True
    except :
        status = False
    return status

def webSit2Login(browser):
    # 功能：sit2 WEB页面登录 ,http://sit2.88uka.com/admin/system/logout.do
    # 依赖：webIsElementPath
    browser.find_element_by_id("userName").clear() #清空输入框默认内容
    browser.find_element_by_id("userName").send_keys("test")
    browser.find_element_by_id("passWord").send_keys("111111")
    browser.save_screenshot('/Users/linghuchong/Downloads/51/aa.png')  #截取当前网页，该网页有我们需要的验证码
    imgelement = browser.find_element_by_id("authCode")  #定位验证码
    location = imgelement.location  #获取验证码x,y轴坐标
    size=imgelement.size  #获取验证码的长宽
    rangle=(int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height'])) #写成我们需要截取的位置坐标
    i=Image.open("/Users/linghuchong/Downloads/51/aa.png") #打开截图
    frame4=i.crop(rangle)  #使用Image的crop函数，从截图中再次截取我们需要的区域
    frame4.save('/Users/linghuchong/Downloads/51/aaframe4.png')
    qq=Image.open('/Users/linghuchong/Downloads/51/aaframe4.png')
    #text=pytesseract.image_to_string(qq) #使用image_to_string识别验证码
    os.system('tesseract /Users/linghuchong/Downloads/51/aaframe4.png out -l eng')
    text = os.popen('more out.txt').readline()
    browser.find_element_by_id("randomCode").send_keys(text)
    # browser.find_element_by_class_name("btn-c").click()
    sleep(3)
    # 判断是否登录成功
    if webIsElementPath(browser,'//div[@class="nav"]/ul/li[3]')==False:  # 登录失败,可能验证码错误.
        browser.close()
        status=0
    else:
        status=1
    return status

def webBigDogUser(browser,varPhone,varAmount,varExpire):
    # 功能：大咖用户充值 ，Web后台充值并审核通过,如13816101118充值70元,有效期99天,则 webRecharge(self,"70","99") ,默认手机号是当前myPhone
    browser.find_element_by_xpath('//div[@class="nav"]/ul/li[3]').click()    # 点击主菜单 财务
    sleep(3)
    browser.find_element_by_xpath('//div[@id="container"]/div/dl/dd[14]').click()  # 点击侧边菜单 充值
    sleep(4)
    browser.find_element_by_name("btnUserExperience").click()  # 点击 充值按钮
    browser.find_element_by_name("userName").send_keys(varPhone) # 手机号
    browser.find_element_by_name("experienceAmount").send_keys(varAmount) # 充值金额 70
    browser.find_element_by_name("day").clear()
    browser.find_element_by_name("day").send_keys(varExpire) # 金额过期 99 days
    browser.find_element_by_id("submitButton").click()
    a=browser.switch_to_alert()
    a.accept()
    sleep(4)
    # 运营
    browser.find_element_by_xpath('//div[@class="nav"]/ul/li[4]').click()    # 运营
    sleep(3)
    browser.find_element_by_xpath('//div[@id="container"]/div/dl/dd[4]').click()  # 信息审核(1425)
    sleep(2)
    for i in range(1,6):
        varSubject = browser.find_element_by_xpath('//tbody/tr['+ str(i) +']/td[4]/div').text
        if varPhone in varSubject:
            browser.find_element_by_xpath('//tbody/tr['+ str(i) +']/td[7]/a').click()  # 审核
            break
    browser.find_element_by_name("auditPass").click() # 通过
    sleep(5)
    a=browser.switch_to_alert()
    a.accept()
    sleep(2)
    a=browser.switch_to_alert()
    a.accept()
    browser.close()

def webBusinessCommission(browser,varAgentName,varPhone,varAgentNum,varRate):
    # 功能：代理商发展商户 ， Web后台设置某手机为代理商户,app我中显示红包炸弹二维码充值
    browser.find_element_by_xpath('//div[@class="nav"]/ul/li[2]').click()    # 点击主菜单 商户
    sleep(3)
    browser.find_element_by_xpath('//div[@id="container"]/div/dl/dd[2]').click()  # 点击侧边菜单 代理商发展商户
    sleep(4)
    browser.find_element_by_name("addAgentStore").click()  # 点击 添加
    browser.find_element_by_name("storeName").send_keys(varAgentName) # 商户名称
    browser.find_element_by_name("phone").send_keys(varPhone) # 商户手机号
    browser.find_element_by_xpath('//select[@id="busiId"]/option[' + str(varAgentNum)+ ']').click()  # 代理商 譬如6=john代理商1
    browser.find_element_by_name("rate").send_keys(varRate) # 佣金
    browser.find_element_by_id("submitStoreButton").click() # 提交
    a=browser.switch_to_alert()
    a.accept()
    sleep(4)
    # 运营
    browser.find_element_by_xpath('//div[@class="nav"]/ul/li[4]').click()    # 运营
    sleep(3)
    browser.find_element_by_xpath('//div[@id="container"]/div/dl/dd[4]').click()  # 信息审核(1425)
    sleep(2)
    for i in range(1,6):
        # print i
        varSubject = browser.find_element_by_xpath('//tbody/tr['+ str(i) +']/td[4]/div').text
        if u"合作商户" in varSubject:
            browser.find_element_by_xpath('//tbody/tr['+ str(i) +']/td[7]/a').click()  # 审核
            sleep(5)
            tmpvarAgentName = browser.find_element_by_name("storeName").get_attribute("value")
            if  tmpvarAgentName != varAgentName: # 如果选错了的话
                browser.find_element_by_name("cancel").click() # 返回
            else:
                break
    browser.find_element_by_name("auditPass").click() # 通过
    a=browser.switch_to_alert()
    a.accept()
    sleep(2)
    a=browser.switch_to_alert()
    a.accept()
    browser.close()

def webSysMessage(browser,varPhone,varTitle,varContact,varLink):
    # 功能：消息管理, 给手机发送消息 ,制定发送用户输入框如果为空则指系统内所有用户,如需指定多个用户则用逗号分隔,如 13816109050,13611958544,13012342344
    browser.find_element_by_xpath('//div[@class="nav"]/ul/li[4]').click()    # 运营
    sleep(3)
    browser.find_element_by_xpath('//div[@id="container"]/div/dl/dd[9]').click()  # 消息管理
    sleep(2)
    browser.find_element_by_name("btnUserExperience").click() # 添加
    browser.find_element_by_name("title").send_keys(varTitle) #消息标题*：
    browser.find_element_by_name("contact").send_keys(varContact) #消息内容
    browser.find_element_by_name("link").send_keys(varLink) # 外部链接
    browser.find_element_by_name("userArray").send_keys(varPhone) # 指定发送用户：
    browser.find_element_by_id("submitButton").click() # 提交
    sleep(3)
    a=browser.switch_to_alert()
    a.accept()
    sleep(3)
    browser.find_element_by_xpath('//div[@id="container"]/div/dl/dd[4]').click()  # 信息审核
    sleep(2)
    for i in range(1,6):
        # print browser.find_element_by_xpath('//tbody/tr['+ str(i) +']/td[3]').text
        varSubject = browser.find_element_by_xpath('//tbody/tr['+ str(i) +']/td[3]').text
        # 内容来源 = 平台
        if u"平台" in varSubject:
            browser.find_element_by_xpath('//tbody/tr['+ str(i) +']/td[7]/a').click()  # 审核
            sleep(5)
            auditVarPhone = browser.find_element_by_name("userArray").get_attribute("value") # varPhone = 13816101112
            if  auditVarPhone != varPhone: # 如果选错了的话
                browser.find_element_by_name("cancel").click() # 返回
            else:
                break
    browser.find_element_by_name("auditPass").click() # 通过
    a=browser.switch_to_alert()
    a.accept()
    sleep(2)
    a=browser.switch_to_alert()
    a.accept()
    browser.close()


# varPhone="13816101112"
# # Main****************************************************************
# # 当验证码错误时继续尝试再次登录,最多尝试5次
# for a in range(5):
#     from selenium import webdriver
#     browser = webdriver.Firefox()
#     browser.maximize_window()
#     browser.get("http://sit2.88uka.com/admin/system/logout.do")
#     x=webSit2Login(browser)
#     if x==1:
#         b_sysMessage(browser,"13816101112",u"自动的呀",u"内容abcde",u"") # 给指定的手机号发送系统信息
#         # b_BusinessCommission(browser,u"自动化商户名称1","13816109050","6","0.06") # 代理商户,(商户名称,手机号,代理商,佣金) 其中代理商6 = john代理商1
#         break


def webSit2LoginTimes(self):
    # 功能：登录失败后继续登录,最多尝试5次
    for b in range(5):
        # WEB端登录
        self.browser.maximize_window()  #将浏览器最大化
        self.browser.get("http://sit2.88uka.com/admin/finance/userExperienceList.do")
        self.browser.find_element_by_id("userName").clear() #清空输入框默认内容
        self.browser.find_element_by_id("userName").send_keys("test")
        self.browser.find_element_by_id("passWord").send_keys("111111")

        self.browser.save_screenshot('/Users/linghuchong/Downloads/51/aa.png')  #截取当前网页，该网页有我们需要的验证码
        imgelement = self.browser.find_element_by_id("authCode")  #定位验证码
        location = imgelement.location  #获取验证码x,y轴坐标
        size=imgelement.size  #获取验证码的长宽
        rangle=(int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height'])) #写成我们需要截取的位置坐标
        i=Image.open("/Users/linghuchong/Downloads/51/aa.png") #打开截图
        frame4=i.crop(rangle)  #使用Image的crop函数，从截图中再次截取我们需要的区域
        frame4.save('/Users/linghuchong/Downloads/51/aaframe4.png')
        qq=Image.open('/Users/linghuchong/Downloads/51/aaframe4.png')
        #text=pytesseract.image_to_string(qq) #使用image_to_string识别验证码
        os.system('tesseract /Users/linghuchong/Downloads/51/aaframe4.png out -l eng')
        text = os.popen('more out.txt').readline()
        self.browser.find_element_by_id("randomCode").send_keys(text)
        #self.browser.find_element_by_class_name("btn-c").click()
        sleep(5)
        if self.b_isElement("edit_password") != True:
             print "Err,WEb三藏红包系统平台验证码错误!"
             self.browser.close()
             self.browser = webdriver.Firefox()
             sleep(3)
        else:
            break

def webClose(self):
    self.browser.close()

def webRecharge(self,varAmount,varExpire):
        # Web后台充值并审核通过,如对手机13816101118充值70元,有效期99天,则 b_chongzhi(self,"70","99") ,默认手机号是当前myPhone
        self.browser.find_element_by_xpath('//div[@class="nav"]/ul/li[3]').click()    # 点击主菜单 财务
        sleep(3)
        self.browser.find_element_by_xpath('//div[@id="container"]/div/dl/dd[14]').click()  # 点击侧边菜单 充值
        sleep(2)
        self.browser.find_element_by_name("btnUserExperience").click()  # 点击 充值按钮
        self.browser.find_element_by_name("userName").send_keys(myPhone) # 手机号
        self.browser.find_element_by_name("experienceAmount").send_keys(varAmount) # 充值金额 70
        self.browser.find_element_by_name("day").send_keys(varExpire) # 金额过期 99 days
        self.browser.find_element_by_id("submitButton").click()
        a=self.browser.switch_to_alert()
        a.accept()
        sleep(2)
        # 运营
        self.browser.find_element_by_xpath('//div[@class="nav"]/ul/li[4]').click()    # 运营
        sleep(3)
        self.browser.find_element_by_xpath('//div[@id="container"]/div/dl/dd[4]').click()  # 信息审核(1425)
        sleep(2)
        self.browser.find_element_by_xpath('//tbody/tr/td[7]/a').click()  # 审核
        self.browser.find_element_by_name("auditPass").click() # 通过
        a=self.browser.switch_to_alert()
        a.accept()
        sleep(2)
        a=self.browser.switch_to_alert()
        a.accept()
        return varAmount

#****************************************************************
# 错误提示:selenium.common.exceptions.WebDriverException: Message: Can't load the profile
# sudo pip install -U selenium
# 卸载火狐浏览器
