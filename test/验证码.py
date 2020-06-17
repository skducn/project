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



def webSit2Login(browser):
    # 功能：sit2 WEB页面登录 ,http://sit2.88uka.com/admin/system/logout.do
    # 依赖：webIsElementPath

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




