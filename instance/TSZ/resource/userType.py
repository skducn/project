# coding: utf-8
#****************************************************************
# source.py
# Author     : John
# Version    : 1.0.0
# Date       : 2016-7-12
# Description: 用户类型,通过后台创建的用户类型
# sudo pip install -U selenium
#****************************************************************

import os,sys,unittest,xlwt,xlrd,MySQLdb,tempfile,shutil,chardet,random,webbrowser,platform,string,datetime,redis
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
from xlutils.copy import copy
from PIL import Image
from pyh import *
#from jhj_v1_5_setup import *
#win32api,win32con,HTMLTestRunner
# import HTMLTestRunner
import time,Image,ImageChops
# print sys.path
# from resource.source.comparePic import *
# from resource.source import test2
# http://sit2.88uka.com/admin/system/logout.do




def b_isElementPath(browser,element):
    flag = False
    try:
        browser.find_element_by_xpath(element)
        flag = True
    except :
        flag = False
        flagfile=u"%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    return flag

def b_login(browser):
    # WEB页面登录 ,http://sit2.88uka.com/admin/system/logout.do
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
    sleep(5)
    # 判断是否登录成功
    if b_isElementPath(browser,'//div[@class="nav"]/ul/li[3]')==False:  # 登录失败,可能验证码错误.
        browser.close()
        tmpState=0
    else:
        tmpState=1
    return tmpState

def b_bigDogUser(browser,varPhone,varAmount,varExpire):
    # 大咖用户 充值.
    # Web后台充值并审核通过,如对手机13816101118充值70元,有效期99天,则 b_chongzhi(self,"70","99") ,默认手机号是当前myPhone
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
        # print i
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

def b_BusinessCommission(browser,varAgentName,varPhone,varAgentNum,varRate):
    # 代理商发展商户
    # Web后台设置某手机为代理商户,app我中显示红包炸弹二维码充值
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
            if  tmpvarAgentName <> varAgentName: # 如果选错了的话
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


# [main]---------------------------------------------------------------

# # # 当验证码错误时继续尝试再次登录,最多尝试5次
# for a in range(5):
#     browser = webdriver.Firefox()
#     browser.maximize_window()
#     browser.get("http://sit2.88uka.com/admin/system/logout.do")
#     x=b_login(browser)
#     if x==1:
#         b_bigDogUser(browser,"13816107018","120","99") # 大咖用户,(手机号,金额,到期日期)
#         # b_BusinessCommission(browser,u"自动化商户名称1","13816109050","6","0.06") # 代理商户,(商户名称,手机号,代理商,佣金) 其中代理商6 = john代理商1
#         break













