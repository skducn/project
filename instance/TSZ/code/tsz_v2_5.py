# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description: android自动化测试框架
#****************************************************************

import os,sys,unittest,xlwt,xlrd,MySQLdb,tempfile,shutil,chardet,random,webbrowser,platform,string,datetime,redis,commands
from appium import webdriver
# from selenium import webdriver
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
#****************************************************************

# 参数化
ExcelFile = "/Users/linghuchong/Downloads/51/Project/TSZ/excel/tsz_v2_5.xls"
ReportHtml = "/Users/linghuchong/Downloads/51/ForWin/Project/TSZ/report/testreport_v2_5.html"
varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S') #当天日期时间
ReportHtmltime = "/Users/linghuchong/Downloads/51/Project/TSZ/report/tszTable" + varTimeYMDHSM + ".html" # TestReport文件

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
bk = xlrd.open_workbook(ExcelFile,formatting_info=True)
newbk = copy(bk)
sheetMain = bk.sheet_by_name("main")
sheetTestCase = bk.sheet_by_name("testcase")
styleRed = xlwt.easyxf('font: name Times New Roman, color-index red')
styleBlue = xlwt.easyxf('font: name Times New Roman, color-index blue')
styleGray25 = xlwt.easyxf('font: name Times New Roman, color-index gray25')
# 获取手机相关制造商信息
(x, androidVersion) = commands.getstatusoutput('adb shell getprop ro.build.version.release')
(x, androidSerialno) = commands.getstatusoutput('adb shell getprop ro.serialno')
# 获取手机相关制造商信息：adb shell getprop | grep "model\|version.sdk\|manufacturer\|hardware\|platform\|revision\|serialno\|product.name\|brand"




# varEndX = 720  #手机屏幕分辨率宽度和高度
# varEndY = 1280
# varEndXY = str(varEndX) + str(varEndY)
# ScreenshotFolder = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/"+str(varEndX)+str(varEndY)+"/screenshot/"
# ErrorScreenshotFolder = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/"+str(varEndX)+str(varEndY)+"/errscreenshot/"
# if os.path.exists("/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/" + str(varEndX) + str(varEndY)) == False:
#    os.makedirs("/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/"+str(varEndX)+str(varEndY))
#    print "Created," +" /Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/"+str(varEndX)+str(varEndY)
#    os.makedirs(ScreenshotFolder)
#    print "Created, " + ScreenshotFolder
#    os.makedirs(ErrorScreenshotFolder)
#    print "Created, " + ErrorScreenshotFolder



class tsz(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = str(float(androidVersion[0:3]))
        desired_caps['deviceName'] = androidSerialno
        desired_caps['appPackage'] = sheetMain.cell_value(1,5)  # 'com.mowin.tsz'
        desired_caps['appActivity'] = sheetMain.cell_value(1,6)  # 'com.mowin.tsz.SplashActivity'
        desired_caps['unicodeKeyboard'] = 'True'
        desired_caps['resetKeyboard'] = 'True'
        reload(sys)
        sys.setdefaultencoding('utf8')
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        # 手机分辨率的宽,高
        self.screenX = self.driver.get_window_size()['width']
        self.screenY = self.driver.get_window_size()['height']

        print "\n当前测试机信息如下:"
        (x, productmodel) = commands.getstatusoutput('adb shell getprop ro.product.model')
        print "品牌名: " + str(productmodel)
        (x, productdevice) = commands.getstatusoutput('adb shell getprop ro.product.device')
        print "设备名: " + str(productdevice)
        print "版本号: " + str(androidVersion)
        (x, sdk) = commands.getstatusoutput('adb shell getprop ro.build.version.sdk')
        print "s d k: " + str(sdk)
        print "分辨率: " + str(self.screenX) + " * " + str(self.screenY)
        (x, abi) = commands.getstatusoutput('adb shell getprop ro.product.cpu.abi')
        print "C P U: " + str(abi)
        (x, serialno) = commands.getstatusoutput('adb shell getprop ro.serialno')
        print "SerialNo: " + str(serialno)
        print ">" * 50
        sleep(11212)
        self.connWeb= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
        self.curWeb = self.connWeb.cursor()
        self.curWeb.execute('SET NAMES utf8;')
        # self.connWeb.set_character_set('utf8')
        # self.curWeb.execute('SET CHARACTER SET utf8;')
        # self.curWeb.execute('SET character_set_connection=utf8;')
        self.connApp= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardapp', port=3306, use_unicode=True)
        self.curApp = self.connApp.cursor()
        self.curApp.execute('SET NAMES utf8;')
        self.connGame= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='game', port=3306, use_unicode=True)
        self.curGame = self.connGame.cursor()
        self.curGame.execute('SET NAMES utf8;')

        # 获取数据库中手机号最小的那个,并减1
        self.curWeb.execute('select min(username) from t_user')
        tb = self.curWeb.fetchone()
        newPhone = int(tb[0]) - 1

        # 获取手机号
        try:
            l_phone = []
            if "/" in str(sheetMain.cell_value(1,7)):
                x = sheetMain.cell_value(1,7).split("/")
                for i in range(0,sheetMain.cell_value(1,7).count("/")+1):
                    l_phone.append(x[i])
                    # print l_phone[i]   # 13816109050/13636371320
                oldPhone1 = l_phone[0]
                oldPhone2 = l_phone[1]
            else:
                oldPhone1 = str(sheetMain.cell_value(1,7))
            varNickName = str(oldPhone1[0:3]) + "****" + str(oldPhone1[7:])
        except:
             print str('Error,excel中OldPhone字段不能为空!')



    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def test_Main(self):
        for i in range(1,sheetMain.nrows):
            if sheetMain.cell_value(i,0) == "Y":
                self.Maincol1 = sheetMain.cell_value(i,1)
                self.Maincol2 = sheetMain.cell_value(i,2)
                exec(sheetMain.cell_value(i,4))

    def TestcaseModule(self):
         # 遍历TestCase及调用函数模块,定位测试用例位置及数量
         case1 = caseN = 0
         for j in range(1,sheetTestCase.nrows):
              case1 = case1 + 1
              if sheetTestCase.cell_value(j,2) == self.Maincol1:
                  for k in range(case1+1,100):  # 假设有100个Case
                      if k + 1 > sheetTestCase.nrows:  # 最后一行
                           caseN = caseN + 1
                           break
                      elif sheetTestCase.cell_value(k,1) == "" and sheetTestCase.cell_value(k,2) == "":
                           caseN = caseN + 1
                      elif sheetTestCase.cell_value(k,1) == "skip":
                           caseN = caseN + 1
                      else:
                           caseN = caseN + 1
                           break
                  break
         if self.Maincol2 == "skip":
             case1 = case1 + 1
             caseN = caseN - 1

         # print case1,caseN
         #遍历 Testcase1~TestCaseN
         for l in range(case1,caseN+case1):
              str_list = []
              for m in range(6,15):  # id0 - id9 ,定位参数从第6列开始，遍历10列
                  if sheetTestCase.cell(l, m).value <> "":
                      N = sheetTestCase.cell_value(l, m)
                      str_list.append(str(N))
                  else:
                      break
              self.str_list=str_list
              try :
                  if sheetTestCase.cell_value(l, 1) == "skip":
                      newWs = newbk.get_sheet(1)
                      newWs.write(l, 0, "skip", styleGray25)
                      newbk.save(ExcelFile)
                  else:
                      exec(sheetTestCase.cell_value(l,5))
                      newWs=newbk.get_sheet(1)
                      newWs.write(l, 0, "OK", styleBlue)
                      newbk.save(ExcelFile)
                      # page << p("<font color=blue>[Pass]</font> ",self.sheetTestCase.cell_value(l,3))  #输出测试用例
              except:
                  print "Error,Excel,("+str(l+1)+")," + sheetTestCase.cell_value(case1, 2) + "," +sheetTestCase.cell_value(l, 3) + "," +sheetTestCase.cell_value(l, 4)
                  newWs=newbk.get_sheet(1)
                  newWs.write(l, 0, "error", styleRed)
                  newbk.save(ExcelFile)
                  # page << p("<font color=red>[Error]</font> ",self.sheetTestCase.cell_value(l,3))  #输出测试用例

         # # 是否生成ReportHTML文档, 1=生成一个testreport.html; 2=生成多个带时间的html,如testreport20161205121210.html;
         # if self.sheetMain.cell_value(1, 9) == 1:
         #     page.printOut(ReportHtml)
         #     sleep(4)
         #     # send Email
         #     if self.sheetMain.cell_value(1, 8) == "Y":self.sendemail(ReportHtml)
         # elif self.sheetMain.cell_value(1,9) == 2:
         #     page.printOut(ReportHtmltime)
         #     # send Email
         #     if self.sheetMain.cell_value(1,8) == "Y":
         #        self.sendemail(ReportHtmltime)


# [common]****************************************************************


    def captureCustomScreen(self,imageName,startX, startY, endX, endY):
        # 功能:截取屏幕(自定义范围)   # 如: captureCustomScreen("test.png",0,1080,1,1920)
        self.driver.save_screenshot(imageName)
        box=(startX, startY, endX, endY)
        i = Image.open(imageName)
        newImage = i.crop(box)
        newImage.save(imageName)
    def compareScreen(self,orgImageName,newImageName,startX,startY,endX,endY):
         # 功能:两图比较,如无原始图则只截屏(不比较),否则截屏后与原始图比较,不一致则返回时间戳. # compareScreen(self,img1,img2,0, 76, 1080, 1769)
         # newImageName='new_redgame.png'(当前截图) , orgImageName= 'org_redgame.png'(原始图)
         self.driver.save_screenshot(newImageName)
         box = (startX,startY,endX,endY)
         i = Image.open(newImageName)
         newImage = i.crop(box)
         newImage.save(newImageName)
         sleep(4)
         if os.path.exists(orgImageName):
             varimg1 = open(newImageName, "r")
             varimg2 = open(orgImageName, "r")
             if varimg1.read() <> varimg2.read():
                 varStrTimeAdd3 = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
                 return varStrTimeAdd3
             else:
                 return 1
         else:
             os.renames(newImageName,orgImageName)
             return 0
    def compareScreenResult(self,ImageName,startX,startY,endX,endY,casenum):
        # 功能: 调用两图比较函数 并输出结果.  # compareScreenResult("weixinpay",160, 0, 1080, 1920,"C1-1,title")
        compareResult = self.compareScreen(ScreenshotFolder  + ImageName + '_org.png',ScreenshotFolder + ImageName + '_new.png',startX,startY,endX,endY)
        if compareResult > 1:
             print "Err," + casenum  + ErrorScreenshotFolder + ImageName + compareResult + ".png (原始图: " + ScreenshotFolder + ImageName + "_org.png)"
             self.captureCustomScreen(ErrorScreenshotFolder + ImageName + compareResult + ".png",startX,startY,endX,endY)
        elif compareResult == 0:
             print "Created," + casenum  + ScreenshotFolder + ImageName + "_org.png"
        elif compareResult == 1:
             print "OK," + casenum + "两图对比结果一致" + ScreenshotFolder + ImageName + "_org.png = " + ImageName + "_new.png"


   # #判断app元素是否存在,不存在则返回时间戳
    def isElement(self,locate):
        # 判断app元素是否存在
        flag = False
        try:
            self.driver.find_element_by_id(locate)
            flag = True
        except :
            flag = False
        return flag
    def userLogin(self):
        # 无密码快捷登录 2.5.0
        self.driver.find_element_by_id("com.mowin.tsz:id/phone_number").clear()
        sleep(2)
        self.compareScreenResult("noPassUserLogin",0, 75, varEndX, varEndY,"OK,无密码快捷登录") # 登录页面截屏
        self.driver.find_element_by_id("com.mowin.tsz:id/phone_number").send_keys(oldPhone1)
        self.driver.find_element_by_id("com.mowin.tsz:id/get_mobile_code").click() # 获取验证码
        sleep(4)
        self.cur.execute('select verify_code from ta_message where phone=%s order by id desc limit 1' % (oldPhone1))
        t1 = self.cur.fetchone()
        self.driver.find_element_by_id("com.mowin.tsz:id/mobile_code").send_keys(t1[0])
        self.driver.find_element_by_id("com.mowin.tsz:id/login").click()     # 点击 手机号登录
        sleep(2)
    def userLoginWeixin(self,appName,appPass,varEndXY):
        # 登录微信 页面
        if self.isElement("com.tencent.mm:id/b5m")==True:  # 登录 按钮是否存在
            print "999999999"
            self.driver.find_element_by_xpath("//android.widget.EditText[contains(@index,'1')]").send_keys(appName)
            self.driver.find_element_by_xpath("//android.widget.EditText[contains(@NAF,'true')]").send_keys(appPass)
            self.driver.find_element_by_id("com.tencent.mm:id/b5m").click()
            sleep(12)
            # 微信页面确认登录
            if varEndXY=="14402392":
               self.driver.swipe(500, 1200, 500, 1200, 500); # 点击 确认登录
            elif varEndXY =="10801920":
               self.driver.swipe(500, 1065, 500, 1065, 500); # 点击 确认登录
        elif self.driver.find_element_by_id("android:id/text1").text==u"微信登录":
            if varEndXY=="14402392":
               self.driver.swipe(500, 1200, 500, 1200, 500); # 点击 确认登录
            elif varEndXY =="10801920":
               self.driver.swipe(500, 1065, 500, 1065, 500); # 点击 确认登录
        else:
            print "Error,微信页面刷新失败,请重试!"
    def userLoginQQ(self,appName,appPass,varEndXY):
        # 无密码快捷登录 - QQ登录
        if self.isElement("com.tencent.mobileqq:id/account")==True:
            self.driver.find_element_by_id("com.tencent.mobileqq:id/account").send_keys(appName)
            self.driver.find_element_by_id("com.tencent.mobileqq:id/password").send_keys(appPass)
            self.driver.find_element_by_id("com.tencent.mobileqq:id/name").click()  # 登录
            sleep(7)
        else:
            self.driver.find_element_by_xpath("//android.widget.Button[contains(@text,'登录')").click()
        sleep(3)
    def screenWidthHeight(self,rightCornerPicID):
        # self.screenWidthHeight("com.mowin.tsz:id/my_tab")
        # 获取屏幕右下角图片的长度和高度, 一般是屏幕的长度和高度(1440,2392)
        location =  self.driver.find_element_by_id(rightCornerPicID).location
        size = self.driver.find_element_by_id(rightCornerPicID).size
        varWidth = int(location["x"] + size["width"])
        varHeight = int(location["y"] + size["height"])
        return varWidth,varHeight

    def sendemail(self,varFile):
        # 邮箱配置
        sender = '<jinhao@mo-win.com.cn>'
        receiver = 'jinhao@mo-win.com.cn'
        f = open(varFile,'rb')
        mail_body = f.read()
        f.close()
        msg=MIMEText(mail_body,_subtype='html',_charset='utf-8')
        # msg = MIMEText('<html><h1>你好！</h1></html>','html','utf-8')
        # msg = MIMEText('你好','text','utf-8')
        # msg['Subject'] = Header(subject,'utf-8')
        msg['Subject'] = u'三藏红包gameTAble'
        try:
            smtp = smtplib.SMTP()
            smtp.connect('smtp.exmail.qq.com')
            smtp.login('jinhao@mo-win.com.cn','Jinhao80')
            smtp.sendmail(sender,receiver,msg.as_string())
            smtp.quit()
        except Exception, e:
            print str(e)

# [main]****************************************************************
# self.driver.switch_to.context("WEBVIEW")
# self.driver.switch_to_default_content()

    # 首页
    def drv_home(self):
        self.TestcaseModule()
    def midpointXYclick(self, midpointX, midpointY):
        # 功能: 自适应分辨率,获取元素并点击 #  (startX+endX)/2 , (startY+endY)/2
        # 用法: 输入元素X,Y坐标的中点,自动转换成当前手机分辨率相应的坐标位置.
        # 适用于 1920*1080 , 1280*720 , 2560*1440 , 800*480 = (1.77777777778)
        # 适用于 2392*1440 = (1.66111111111)
        # 适用于 2560*1600 = (1.6)
        # 适用于 1024*768 =(1.33333333333)
        if self.screenY > self.screenX :  # 竖屏
            fx = int(float(midpointX/1080.00)*self.screenX*self.screenX/1080)
            fy = int(float(midpointY/1920.00)*self.screenY*self.screenY/1920)
        else:  # 横屏
            fx = int(float(midpointX/1920.00)*self.screenY*self.screenY/1920)
            fy = int(float(midpointY/1080.00)*self.screenX*self.screenX/1080)
        sleep(3)
        self.driver.swipe(fx, fy, fx, fy, 500)

    def homepage(self):
        print "1111111"
        # # C1-1,新账号首次登录，检查首页元素（截图）
        # # 如果登录则退出
        # self.midpointXYclick(1018, 147)
        # sleep(3)
        # varEndX,varEndY=self.screenWidthHeight("com.mowin.tsz:id/my_tab")
        # self.driver.find_element_by_id("com.mowin.tsz:id/my_tab").click() # 我
        # if self.isElement("com.mowin.tsz:id/no_login_item")<>True: # 已登录
        #     self.driver.find_element_by_id("com.mowin.tsz:id/settings").click()     # 我 - 设置
        #     sleep(2)
        #     self.driver.find_element_by_id("com.mowin.tsz:id/logout").click() # 退出登录
        #     self.driver.find_element_by_id("com.mowin.tsz:id/positive").click() # 三藏红包,你确定要退出登录吗? 点击 退出登录
        #     self.driver.swipe(100, 100, 100, 100, 500)  # 无密码快捷登录 页面,点击 左上角的关闭,应返回首页
        # else:
        #     self.driver.find_element_by_id("com.mowin.tsz:id/home_tab").click()
        #     sleep(2)
        # # 截首页屏幕
        # if varEndXY=="14402392":
        #     self.compareScreenResult("homepage",0, 1197, varEndX, varEndY,"C1-1,新账号首次登录，检查首页元素（截图）")
        # elif varEndXY=="10801920":
        #     self.compareScreenResult("homepage",0, 929, varEndX, varEndY,"C1-1,新账号首次登录，检查首页元素（截图）")

    def homeJumpLogin(self):
        # C1-1-2,检查未登录时，页面跳转到无密码快捷登录页（截图）
        # 点击消息 ? (消息页,显示 正在加载数据...)
        self.driver.find_element_by_id("com.mowin.tsz:id/message").click() # 点击 消息icon
        if self.isElement("com.mowin.tsz:id/phone_number")==True: self.midpointXYclick(69, 147) # 点击 无密码快捷登录"X"按钮
        else: print "Error,C1-1-2,消息,无密码快捷登录界面无显示!"
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()

        # 点击抢红包看广告
        self.driver.find_element_by_id("com.mowin.tsz:id/fight_red_packet_layout").click()
        self.driver.find_element_by_id("com.mowin.tsz:id/fight").click()
        if self.isElement("com.mowin.tsz:id/phone_number")==True:self.midpointXYclick(69, 147) # 点击 无密码快捷登录"X"按钮
        else: print "Error,C1-1-2,抢红包,无密码快捷登录界面无显示!"
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()

        # 点发红包发广告
        self.driver.find_element_by_id("com.mowin.tsz:id/send_red_packet_layout").click()
        # 红包类型 - 广告红包炸弹
        self.driver.find_element_by_id("com.mowin.tsz:id/ad_red_packet_item").click()
        self.driver.find_element_by_id("com.mowin.tsz:id/bind_red_packet").click() # 去绑红包炸弹
        if self.isElement("com.mowin.tsz:id/phone_number")==True:self.midpointXYclick(69, 147) # 点击 无密码快捷登录"X"按钮
        else: print "Error,C1-1-2,广告红包炸弹,去绑红包炸弹,无密码快捷登录界面无显示!"

        # ??
        # self.driver.find_element_by_id("com.mowin.tsz:id/save_template").click() # 保存为模版
        # if self.isElement("com.mowin.tsz:id/phone_number")==True:self.midpointXYclick(69, 147) # 点击 无密码快捷登录"X"按钮
        # else: print "Error,C1-1-2,广告红包炸弹,保存为模版,无密码快捷登录界面无显示!"

        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()

        # 红包类型 - 拼手气群红包
        self.driver.find_element_by_id("com.mowin.tsz:id/spell_luck_red_packet_item").click()
        self.driver.find_element_by_id("com.mowin.tsz:id/to_bind_red").click() # 去绑红包
        if self.isElement("com.mowin.tsz:id/phone_number")==True:self.midpointXYclick(69, 147) # 点击 无密码快捷登录"X"按钮
        else: print "Error,C1-1-2,拼手气群红包,无密码快捷登录界面无显示!"
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()

        # 红包类型 - 普通群红包
        self.driver.find_element_by_id("com.mowin.tsz:id/normal_red_packet_item").click
        self.driver.find_element_by_id("com.mowin.tsz:id/to_bind_red").click() # 去绑红包
        if self.isElement("com.mowin.tsz:id/phone_number")==True:self.midpointXYclick(69, 147) # 点击 无密码快捷登录"X"按钮
        else: print "Error,C1-1-2,普通群红包,无密码快捷登录界面无显示!"
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()

        # 红包类型 - 私信红包
        self.driver.find_element_by_id("com.mowin.tsz:id/private_msg_red_packet_item").click()
        if self.isElement("com.mowin.tsz:id/phone_number")==True:self.midpointXYclick(69, 147) # 点击 无密码快捷登录"X"按钮
        else: print "Error,C1-1-2,私信,无密码快捷登录界面无显示!"
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()

        # 点击 红包游戏 (??返回显示 正在加载数据...)
        # self.driver.find_element_by_id("com.mowin.tsz:id/game_tab").click()
        # if self.isElement("com.mowin.tsz:id/phone_number")==True:
        #    self.driver.swipe(100, 100, 100, 100, 500)  # 无密码快捷登录 页面,点击 左上角的关闭,应返回首页
        # else: print "Error,C1-1-2,红包游戏,无密码快捷登录界面无显示!"

        # 点击 红包群 - 点击登录创建
        self.driver.find_element_by_id("com.mowin.tsz:id/red_packet_group_tab").click()
        self.driver.find_element_by_id("com.mowin.tsz:id/my_red_packet_login_item").click()
        if self.isElement("com.mowin.tsz:id/phone_number")==True:self.midpointXYclick(69, 147) # 点击 无密码快捷登录"X"按钮
        else: print "Error,C1-1-2,点击登录创建,无密码快捷登录界面无显示!"

        # 点击 红包群 - 点击 通讯录 (数据一致加载中...)
        self.driver.find_element_by_id("com.mowin.tsz:id/more").click() # 红包群 - 通讯录
        self.driver.find_element_by_id("com.mowin.tsz:id/contacts").click() # 点击 通讯录
        if self.isElement("com.mowin.tsz:id/phone_number")==True:self.midpointXYclick(69, 147) # 点击 无密码快捷登录"X"按钮
        else: print "Error,C1-1-2,红包群-通讯录,无密码快捷登录界面无显示!"
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()

        # 点击 红包群 - 点击 加入
        appEnter = self.driver.find_elements_by_id("com.mowin.tsz:id/add_red_packet_group") # 遍历 加入
        for a_ppEnter in appEnter:
            a_ppEnter.click()
            sleep(10)
            break
        self.driver.find_element_by_id("com.mowin.tsz:id/next").click() # 点击 关注群广告中的加入
        if self.isElement("com.mowin.tsz:id/phone_number")==True:self.midpointXYclick(69, 147) # 点击 无密码快捷登录"X"按钮
        else: print "Error,C1-1-2,红包群-加入,无密码快捷登录界面无显示!"


    def homeLogin(self):
        # C1-1-3,微信、QQ、微博、手机号登录
        sleep(5)
        # 判断当前是否有账号登录,如有则退出
        self.driver.find_element_by_id("com.mowin.tsz:id/my_tab").click() # 我
        if self.isElement("com.mowin.tsz:id/no_login_item")==True :
            self.driver.find_element_by_id("com.mowin.tsz:id/no_login_item").click() # 点击登录
        else:
            self.driver.find_element_by_id("com.mowin.tsz:id/settings").click()     # 我 - 设置
            self.driver.find_element_by_id("com.mowin.tsz:id/logout").click() # 退出登录
            self.driver.find_element_by_id("com.mowin.tsz:id/positive").click() # 三藏红包,你确定要退出登录吗? 点击 退出登录
            sleep(2)

        # 无密码快捷登录 检查微信icon,登录,登录后头像 和 用户名
        if self.isElement("com.mowin.tsz:id/wechat_login_item")==True:
            self.driver.find_element_by_id("com.mowin.tsz:id/wechat_login_item").click()
            sleep(5)
            self.userLoginWeixin("happyjinhao","jinhao123",varEndXY)  # 用微信登录
            self.driver.find_element_by_id("com.mowin.tsz:id/my_tab").click() # 我
            sleep(2)
            # 检查我 页面中用户名截图
            if varEndXY=="14402392":self.compareScreenResult("myWeixinPicName",0, 259, varEndX, 620,"C1-1-3,微信登录后头像和用户名截图")
            elif varEndXY =="10801920":self.compareScreenResult("myWeixinPicName",0, 225, varEndX, 534,"C1-1-3,微信登录后头像和用户名截图")
            sleep(2)
            self.driver.find_element_by_id("com.mowin.tsz:id/settings").click()     # 我 - 设置
            self.driver.find_element_by_id("com.mowin.tsz:id/logout").click() # 退出登录
            self.driver.find_element_by_id("com.mowin.tsz:id/positive").click() # 三藏红包,你确定要退出登录吗? 点击 退出登录
            sleep(2)
        else:
            print "Error,C1-1-3,无密码快捷登录页面微信icon不存在!"

        # 无密码快捷登录 检查QQicon,登录,登录后头像 和 用户名
        if self.isElement("com.mowin.tsz:id/qq_login_item")==True:
            self.driver.find_element_by_id("com.mowin.tsz:id/qq_login_item").click()
            sleep(5)
            self.userLoginQQ("3525023378","jinhao123",varEndXY)  # 用QQ登录
            self.driver.find_element_by_id("com.mowin.tsz:id/my_tab").click() # 我
            sleep(2)
            # 检查我 页面中用户名截图
            if varEndXY=="14402392":self.compareScreenResult("myQQPicName",0, 259, varEndX, 620,"C1-1-3,QQ登录后头像和用户名截图")
            elif varEndXY =="10801920":self.compareScreenResult("myQQPicName",0, 225, varEndX, 534,"C1-1-3,QQ登录后头像和用户名截图")
            sleep(2)
            self.driver.find_element_by_id("com.mowin.tsz:id/settings").click()     # 我 - 设置
            self.driver.find_element_by_id("com.mowin.tsz:id/logout").click() # 退出登录
            self.driver.find_element_by_id("com.mowin.tsz:id/positive").click() # 三藏红包,你确定要退出登录吗? 点击 退出登录
            sleep(2)
        else:
            print "Error,C1-1-3,无密码快捷登录页面QQicon不存在!"
    def home(self):
        # C1-1,城市、标题、消息、底部菜单
        print "44444444444"
        sleep(8)
        # 检查 选择城市
        if self.isElement("com.mowin.tsz:id/select_city")==True:
            self.driver.find_element_by_id("com.mowin.tsz:id/select_city").click()
            sleep(2)
            # self.homeCity()
            self.driver.find_element_by_id("com.mowin.tsz:id/back").click()
        else: print "Error,C1-1,home,左上角城市不存在!"
        # 检查 标题=三藏红包
        if self.driver.find_element_by_id("com.mowin.tsz:id/title").text <> u"三藏红包": print "Error,C1-1,home,标题是" + self.driver.find_element_by_id("com.mowin.tsz:id/title").text
        # 检查 消息
        if self.isElement("com.mowin.tsz:id/message")==True:
            self.driver.find_element_by_id("com.mowin.tsz:id/message").click()
            sleep(2)
            self.midpointXYclick(69, 147) # 点击 无密码快捷登录"X"按钮
            # self.homeMessage()
            self.driver.find_element_by_id("com.mowin.tsz:id/back").click()
        else: print "Error,C1-1,home,右上角消息不存在!"
        # 检查 底部菜单各个名称
        if self.isElement("com.mowin.tsz:id/home_tab_icon") == False or self.driver.find_element_by_id("com.mowin.tsz:id/home_tab_text").text <> u"首页" : print "C1-2,home,菜单首页不能存在!"
        if self.isElement("com.mowin.tsz:id/red_packet_group_tab_icon") == False or self.driver.find_element_by_id("com.mowin.tsz:id/red_packet_group_tab_text").text <> u"红包群" : print "C1-2,home,菜单红包群不能存在!"
        if self.isElement("com.mowin.tsz:id/game_tab_icon") == False or self.driver.find_element_by_id("com.mowin.tsz:id/game_tab_text").text <> u"红包游戏" : print "C1-2,home,菜单红包游戏不能存在!"
        if self.isElement("com.mowin.tsz:id/my_tab_icon") == False or self.driver.find_element_by_id("com.mowin.tsz:id/my_tab_text").text <> u"我" : print "C1-2,home,菜单我不能存在!"

    def homeCity(self):
        print "ggggg"

    def homeMessage(self):
        # C1-3，消息内容及红点测试
        print "rrrrrrrr"

    def homeGiveRedbonus(self):
        # 点击 发红包发广告
        print "2222"
        sleep(6)
        self.driver.find_element_by_id("com.mowin.tsz:id/send_red_packet_layout").click()
        sleep(2)
        # 检查 标题 = 红包类型
        if self.driver.find_element_by_id("com.mowin.tsz:id/title").text <> u"红包类型": print "Error,C1-4,homeGiveRedbonus,标题是" + self.driver.find_element_by_id("com.mowin.tsz:id/title").text
        # 广告红包炸弹
        if self.isElement("com.mowin.tsz:id/ad_image") == True and self.isElement("com.mowin.tsz:id/ad_red_text") == True :
             if self.driver.find_element_by_id("com.mowin.tsz:id/ad_red_text").text <> u"广告红包炸弹" : print "Error,C1-?,homeGiveRedbonus,广告红包炸弹 文字有误!"
             title2 = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/child::android.widget.RelativeLayout[1]/android.widget.TextView[contains(@index,2)]").text
             if title2 <> u"宣传推广，营销神器" : print "Error,C1-?,homeGiveRedbonus,'" + title2 + "'文字或标点符号错!"

        if self.isElement("com.mowin.tsz:id/appraise_image")  == True and self.isElement("com.mowin.tsz:id/good_appraise_red_text") == True :
             if self.driver.find_element_by_id("com.mowin.tsz:id/good_appraise_red_text").text <> u"好评红包炸弹" : print "Error,C1-?,homeGiveRedbonus,好评红包炸弹 文字有误!"
             title2 = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,2)]").text
             if title2 <> u"好评传千里，传播更给力" : print "Error,C1-?,homeGiveRedbonus,'" + title2 + "'文字或标点符号错!"

        if self.isElement("com.mowin.tsz:id/spell_image") ==True and self.isElement("com.mowin.tsz:id/spell_red_text") ==True :
             if self.driver.find_element_by_id("com.mowin.tsz:id/spell_red_text").text <> u"拼手气群红包" : print "Error,C1-?,homeGiveRedbonus,拼手气群红包 文字有误!"
             title2 = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/child::android.widget.RelativeLayout[3]/android.widget.TextView[contains(@index,2)]").text
             if title2 <> u"红包拼手气，活跃群成员" : print "Error,C1-?,homeGiveRedbonus,'" + title2 + "'文字或标点符号错!"

        if self.isElement("com.mowin.tsz:id/normal_image") ==True and self.isElement("com.mowin.tsz:id/normal_red_text") ==True :
             if self.driver.find_element_by_id("com.mowin.tsz:id/normal_red_text").text <> u"普通群红包" : print "Error,C1-?,homeGiveRedbonus,普通群红包 文字有误!"
             title2 = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/child::android.widget.RelativeLayout[4]/android.widget.TextView[contains(@index,2)]").text
             if title2 <> u"人人都一样，红包不偏心" : print "Error,C1-?,homeGiveRedbonus,'" + title2 + "'文字或标点符号错!"

        if self.isElement("com.mowin.tsz:id/private_msg_image") ==True and self.isElement("com.mowin.tsz:id/private_msg_red_text") ==True :
             if self.driver.find_element_by_id("com.mowin.tsz:id/private_msg_red_text").text <> u"私信红包" : print "Error,C1-?,homeGiveRedbonus,私信红包 文字有误!"
             title2 = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/child::android.widget.RelativeLayout[5]/android.widget.TextView[contains(@index,2)]").text
             if title2 <> u"只给你喜欢的那个TA" : print "Error,C1-?,homeGiveRedbonus,'" + title2 + "'文字或标点符号错!"

        if self.isElement("com.mowin.tsz:id/draw_image") ==True and self.isElement("com.mowin.tsz:id/draw_red_text") ==True :
             if self.driver.find_element_by_id("com.mowin.tsz:id/draw_red_text").text <> u"抽奖红包" : print "Error,C1-?,homeGiveRedbonus,抽奖红包 文字有误!"
             title2 = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/child::android.widget.RelativeLayout[6]/android.widget.TextView[contains(@index,2)]").text
             if title2 <> u"转发抽奖聚人气，迅速扩大红包群" : print "Error,C1-?,homeGiveRedbonus,'" + title2 + "'文字或标点符号错!"

        self.driver.swipe(500, 1015, 500, 500, 1000)# 向下滚动到底部
        sleep(3)

        if self.isElement("com.mowin.tsz:id/qr_code_image") ==True and self.isElement("com.mowin.tsz:id/qr_code_red_text") ==True :
             if self.driver.find_element_by_id("com.mowin.tsz:id/qr_code_red_text").text <> u"二维码红包炸弹" : print "Error,C1-?,homeGiveRedbonus,二维码红包炸弹 文字有误!"
             title2 = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/child::android.widget.RelativeLayout[6]/android.widget.TextView[contains(@index,2)]").text
             if title2 <> u"线下商户好帮手，扫码推广效果棒" : print "Error,C1-?,homeGiveRedbonus,'" + title2 + "'文字或标点符号错!"

        self.driver.swipe(500, 500, 500, 1500, 1000)# 向上滚动到顶部
        sleep(3)



    def redTypeAD(self):
        # 广告红包炸弹
        self.driver.find_element_by_id("com.mowin.tsz:id/ad_red_packet_item").click()
        # 检查 标题 =设置你的广告内容
        if self.driver.find_element_by_id("com.mowin.tsz:id/title").text <> u"设置你的广告内容": print "Error,C1-1,home,标题是" + self.driver.find_element_by_id("com.mowin.tsz:id/title").text



    def redTypeReputation(self):
        # 好评红包炸弹
        pass

    def redTypeLuck(self):
        # 拼手气群红包
        pass

    def redTypeNormal(self):
        # 普通群红包
        pass

    def redTypeLetter(self):
        # 私信红包
        pass

    def redTypeLottery(self):
        # 抽奖红包
        pass

    def redTypeTwoCode(self):
        # 二维码红包炸弹
        pass








    def bridingThird(self):
        # C1-2，初次登录，检查第三方账号绑定
        # 清理第三方账号
        self.driver.find_element_by_id("com.mowin.tsz:id/my_tab").click()
        self.userLogin()
        self.cur.execute('delete from t_user_thirdInfo where belongName="%s" or belongName="%s" or belongName="%s"' % ("John","令狐冲","用户5590858666"))
        self.conn.commit()
        sleep(8)

        # 第三方账号绑定
        self.driver.find_element_by_id("com.mowin.tsz:id/settings").click()
        self.driver.find_element_by_id("com.mowin.tsz:id/bind_other_account").click()
        sleep(2)
        img = "third"
        compareResult = self.compareScreen(ScreenshotFolder + 'big_' + img + '.png',ScreenshotFolder + 'org_' + img + '.png',0, 76, 1080, 1769)
        if compareResult>1:
             print "Err,third 截屏文件:"+ img + compareResult + ".png!"
             self.driver.save_screenshot(ErrorScreenshotFolder + compareResult + ".png")
        elif compareResult==0:
             print "Info,获取原始 "+img+" 的截屏."


        # 点击微信 授权  测试微信号 = John
        self.driver.find_element_by_id("com.mowin.tsz:id/bind_wx_status").click()
        sleep(4)
        img = "thirdweixinLogin"
        compareResult = self.compareScreen(ScreenshotFolder + 'big_' + img + '.png',ScreenshotFolder + 'org_' + img + '.png',0, 76, 1080, 1769)
        if compareResult>1:
             print "Err,微信授权登录页:"+ img + compareResult + ".png!"
             self.driver.save_screenshot(ErrorScreenshotFolder + img + compareResult + ".png")
        elif compareResult==0:
             print "Info,获取原始 "+img+" 的截屏."
        # 微信页面确认登录
        self.driver.swipe(500, 1065, 500, 1065, 500); # 点击 登录
        sleep(3)
        if self.driver.find_element_by_id("com.mowin.tsz:id/bind_wx_status").text<>"已授权":
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
            print "Err,C1-2,微信授权失败:"+ErrorScreenshotFolder + img + timestamp + ".png"
            self.driver.save_screenshot(ErrorScreenshotFolder + img + timestamp + ".png")
        sleep(2)


        # # 点击QQ 授权  测试QQ号 = 令狐冲
        self.driver.find_element_by_id("com.mowin.tsz:id/bind_qq_status").click()
        sleep(4)
        img = "thirdqqLogin"
        compareResult = self.compareScreen(ScreenshotFolder + 'big_' + img + '.png',ScreenshotFolder + 'org_' + img + '.png',0, 76, 1080, 1769)
        if compareResult>1:
             print "Err,QQ授权登录页:"+ img + compareResult + ".png!"
             self.driver.save_screenshot(ErrorScreenshotFolder + img + compareResult + ".png")
        elif compareResult==0:
             print "Info,获取原始 "+img+" 的截屏."
        # QQ页面确认登录
        self.driver.swipe(500, 1500, 500, 1500, 500); # 点击 登录
        sleep(3)
        if self.driver.find_element_by_id("com.mowin.tsz:id/bind_qq_status").text<>"已授权":
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
            print "Err,C1-2,qq授权失败:"+ErrorScreenshotFolder + img + timestamp + ".png"
            self.driver.save_screenshot(ErrorScreenshotFolder + img + timestamp + ".png")


        # # 点击微博 授权
        self.driver.find_element_by_id("com.mowin.tsz:id/bind_weibo_status").click()
        sleep(4)
        img = "thirdweiboLogin"
        compareResult = self.compareScreen(ScreenshotFolder + 'big_' + img + '.png',ScreenshotFolder + 'org_' + img + '.png',0, 76, 1080, 1769)
        if compareResult>1:
             print "Err,weibo授权登录页:"+ img + compareResult + ".png!"
             self.driver.save_screenshot(ErrorScreenshotFolder + img + compareResult + ".png")
        elif compareResult==0:
             print "Info,获取原始 "+img+" 的截屏."
        # weibo页面确认登录
        self.driver.swipe(500, 900, 500, 900, 500); # 点击 登录
        sleep(3)
        if self.driver.find_element_by_id("com.mowin.tsz:id/bind_weibo_status").text<>"已授权":
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
            print "Err,C1-2,weibo授权失败:"+ErrorScreenshotFolder + img + timestamp + ".png"
            self.driver.save_screenshot(ErrorScreenshotFolder + img + timestamp + ".png")

        # 第三方账号绑定 微信\QQ\微博 已授权截图
        img = "thirdweixinqqAuthorized"
        compareResult = self.compareScreen(ScreenshotFolder + 'big_' + img + '.png',ScreenshotFolder + 'org_' + img + '.png',0, 76, 1080, 1769)
        if compareResult>1:
             print "Err,第三方账号全部已授权:"+ img + compareResult + ".png!"
             self.driver.save_screenshot(ErrorScreenshotFolder + img + compareResult + ".png")
        elif compareResult==0:
             print "Info,获取原始 "+img+" 的截屏."
        sleep(4)
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()
        if self.driver.find_element_by_id("com.mowin.tsz:id/name").text<>"John":print "Err,C1-2,微信授权后,我页面中昵称未更换!"

        # # t_user_thirdINfo表验证数据 , 获取userId  ?有问题
        # self.cur.execute('select id from t_user where username="%s" order by id desc limit 1' % (oldPhone1))
        # data1 = self.cur.fetchone()
        # print "12121212"
        # print data1[0]
        # self.cur.execute('select belongName,belongThumb,isValid,openid,token from t_user_thirdInfo where userId=%s and channel=1 order by id desc ' % (data1[0]))
        # data2 = self.cur.fetchone()
        # if data2[0] == "John" and data2[1]<>"" and data2[2]=="1" and data2[3]<>"" and data2[4]<>"":
        #     pass
        # else:
        #     print u"Err,微信授权数据库:belongName="+ data2[0]+" , belongThumb="+ data2[1]+" , isValid="+ data2[2]+" , openid="+ data2[3]+" , token="+ data2[4]
        #
        # self.cur.execute('select belongName,belongThumb,isValid,openid,token from t_user_thirdInfo where userId=%s and channel=2 order by id desc ' % (data1[0]))
        # data2 = self.cur.fetchone()
        # if data2[0] == u"令狐冲" and data2[1]<>"" and data2[2]=="1" and data2[3]<>"" and data2[4]<>"":
        #     pass
        # else:
        #     print u"Err,QQ授权数据库:belongName="+ data2[0]+" , belongThumb="+ data2[1]+" , isValid="+ data2[2]+" , openid="+ data2[3]+" , token="+ data2[4]





    # 红包群
    def drv_redgroup(self):
        self.TestcaseModule()

    def redGroupFollow(self):
        print "12121212"
        sleep(4)
        self.driver.find_element_by_id("com.mowin.tsz:id/red_packet_group_tab").click() # 点击群
        sleep(5)
        varRedgroupname =self.driver.find_elements_by_id("com.mowin.tsz:id/red_packet_group_name")
        for i in varRedgroupname:
            if i.text == "平价店" :
                i.click()
                break
        self.driver.find_element_by_id("com.mowin.tsz:id/hot_goods").click() # 点击 爆款
        sleep(3)
        self.driver.find_elements_by_id("com.mowin.tsz:id/buy_now")[1].click() # 点击第二个立即购买
        sleep(5)
        self.driver.find_element_by_id("com.mowin.tsz:id/plus_num").click() # +1
        self.driver.find_element_by_id("com.mowin.tsz:id/account_balance_checkbox").click()
        self.driver.swipe(500, 1500, 500, 400, 500)  # 向上滚动
        self.driver.find_element_by_id("com.mowin.tsz:id/pay_order").click() # 确认支付


    # 红包游戏
    def drv_redgame(self):
        print "\n"
        self.driver.find_element_by_id("com.mowin.tsz:id/game_tab").click() # 红包游戏
        self.userLogin()
        sleep(2)
        # 红包游戏列表页截屏,红包游戏列表页
        self.compareScreenResult("HBBDX_list",0, 76, 1080, 1769,"C3-1")
        # 进入游戏
        self.driver.find_element_by_id("com.mowin.tsz:id/button").click()  # 点击 进入游戏
        self.TestcaseModule()
    def HBBDXweixinRecharge(self):
        # C3-1,用户首次进入游戏(体验游戏)
        # 检查点1,红包比大小页面元素截屏(不包括在线人数)
        self.compareScreenResult("HBBDX_mainPageWithWidth",160, 0, 1080, 1920,"C3-1")
        self.compareScreenResult("HBBDX_mainPageWithHeight",0, 0, 1080, 1500,"C3-1")

        # 检查点2,游戏余额 + 现金余额 = 0.00
        gameAmount = self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance").text
        gameAmount = gameAmount.split("￥")
        if gameAmount[1] == "0.00":
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance").click()   # 点击 游戏余额:$0.00
            # 点击游戏余额后, 弹出 充值游戏余额(高亮) 和 余额退回我的钱包 浮层,
            self.compareScreenResult("HBBDX_clickGameBalanceRechargeLight",0, 0, 1080, 1500,"C3-1")
            sleep(2)
            self.driver.swipe(300, 750, 300, 750, 500); # 点击 充值游戏余额
            # 充值游戏余额
            self.compareScreenResult("HBBDX_rechargeGameBalanceWeixinLight",160, 0, 1080, 1920,"C3-1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/weixin_pay_icon").click()
            # 充值游戏余额浮层中 , 点击 微信支付
            self.compareScreenResult("HBBDX_weixinPay",160, 0, 1080, 1920,"C3-1")
            # 微信支付
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/amount").send_keys("1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click()
            sleep(10)
            # 页面跳转到 微信安全支付 确认交易 ,点击立即支付
            self.compareScreenResult("HBBDX_weixinPagePayConfirm",0, 350, 1080, 1769,"C3-1")
            print self.driver.find_element_by_id("com.tencent.mm:id/cnp").text  # 游戏充值 190899
            self.driver.swipe(500, 800, 500, 800, 500); # 点击 立即支付
            # 820124
            sleep(4)
            self.driver.swipe(540, 1600, 540, 1600, 500); # 点击 8
            sleep(1)
            self.driver.swipe(540, 1300, 540, 1300, 500); # 点击 2
            sleep(1)
            self.driver.swipe(540, 1800, 540, 1800, 500); # 点击 0
            sleep(1)
            self.driver.swipe(200, 1300, 200, 1300, 500); # 点击 1
            sleep(1)
            self.driver.swipe(540, 1300, 540, 1300, 500); # 点击 2
            sleep(1)
            self.driver.swipe(200, 1400, 200, 1400, 500); # 点击 4
            sleep(4)
            # 交易详情 , 微信安全支付 ,完成
            self.compareScreenResult("HBBDX_weixinPagePayFinish",0, 220, 1080, 600,"C3-1")
            sleep(3)
            self.driver.find_element_by_id("com.tencent.mm:id/ed").click() # 点击完成
            sleep(5)
            # 红包比大小页面 ,浮层 已成功充值1.00元游戏余额,快进入游戏试试手气吧.
            self.compareScreenResult("HBBDX_infoWeixinPay1yuanOK",0, 0, 1080, 1500,"C3-1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click() # 点击 知道了
            # 红包比大小页面 检查游戏余额:$ 1.00
            self.compareScreenResult("HBBDX_gameBalance1yuanFromWeixin",0, 0, 1080, 1500,"C3-1")

            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance").click()   # 点击 游戏余额:$1.00
            # 点击游戏余额后, 弹出 充值游戏余额(高亮) 和 余额退回我的钱包(高亮) 浮层,
            self.compareScreenResult("HBBDX_clickGameBalanceRechargeAndBackLight",0, 0, 1080, 1500,"C3-1")
            sleep(2)
            self.driver.swipe(300, 840, 300, 840, 500); # 点击 余额退回我的钱包
            self.compareScreenResult("HBBDX_balanceOut",160, 0, 1080, 1920,"C3-1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/amount_hint").send_keys("1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click()
            # 浮层 , 1.00元游戏余额已成功退回到你的钱包余额账户内.
            self.compareScreenResult("HBBDX_info1yuantoAccount",160, 0, 1080, 1920,"C3-1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click() # 点击 知道了
            # 红包比大小页面 检查游戏余额:$ 0.00
            gameAmount = self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance").text
            gameAmount = gameAmount.split("￥")
            if gameAmount[1] <> "0.00":print "Err,C3-1,经过了微信充值及余额退回操作后,游戏余额应是0.00!,实测结果:" + str(gameAmount[1])

            # 点击 游戏余额
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance").click()   # 点击 游戏余额:$0.00
            self.driver.swipe(300, 750, 300, 750, 500); # 点击 充值游戏余额
            # 点击 充值游戏余额
            self.compareScreenResult("HBBDX_rechargeGameBalanceAllLight",160, 0, 1080, 1920,"C3-1")
            # 充值游戏余额浮层中 , 点击 余额支付
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/account_balance_icon").click() # 点击 余额支付
            # 余额支付 浮层, 充值 1元
            self.compareScreenResult("HBBDX_balancePay",160, 0, 1080, 1920,"C3-1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/amount_hint").send_keys("1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click()
            sleep(2)
            # 浮层, 已成功充值1.00元游戏余额,快进入游戏试试手气吧.
            self.compareScreenResult("HBBDX_infoBalancePay1yuanOK",0, 0, 1080, 1500,"C3-1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click() # 点击 知道了

            # 开始 体验游戏 ,游戏中点击退出游戏
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/experience_or_start_game").click() # 点击 体验游戏
            sleep(8)
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/exit_game").click() # 点击 退出游戏
            var1=self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/message").text
            print var1
            if var1 <> u"现在离开, 本轮游戏将由笨笨的机器人代玩哟, 输了可不要怪它喔~":print u"Err,C3-1,提示:现在离开, 本轮游戏将由笨笨的机器人代玩哟, 输了可不要怪它喔~ 实测:" + str(var1)
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/negative").click() # 点击 知道 返回游戏主界面
            # redis中清除isExperience =0
            self.cur.execute('select id from t_user where username="%s" order by id desc' % (oldPhone1))
            data1 = self.cur.fetchone()
            ppz = "t_game_user:"+str(data1[0])
            r = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
            r.hset(ppz,"isExperience",0)
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/exit_game").click() # 点击 退出游戏
            # 退出游戏 浮层截屏 ,
            self.compareScreenResult("HBBDX_exitGame",180, 0, 1080, 1500,"C3-1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/negative").click() # 点击 确定
            sleep(2)

            self.driver.find_element_by_id("com.mowin.tsz:id/button").click()  # 点击 进入游戏

            # 检查点3,开始 体验游戏 ,体验游戏结束后自动弹出浮层 ,点击知道返回游戏主界面
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/experience_or_start_game").click() # 点击 体验游戏
            sleep(80)
            if self.isElement("com.mowin.tsz.thanthesize:id/positive"):
                var1=self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/message").text
                if var1 <> u"游戏体验已结束, 进入正式游戏试试身手吧~":print u"Err,C3-1,提示:游戏体验已结束, 进入正式游戏试试身手吧~ 实测:" + str(var1)
                self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click() # 点击知道了
            else:
                self.driver.save_screenshot(ErrorScreenshotFolder + u"体验游戏结束后无弹出浮层.png")
                print "Err,C3-1,体验游戏结束后无弹出浮层!"


            # 检查点4,体验游戏 变为 开始游戏 ,截屏
            self.compareScreenResult("HBBDX_startGame",0, 0, 1080, 1500,"C3-1")

            # 检查点5,游戏说明及规则
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/game_help").click() # 点击 游戏说明及规则
            sleep(3)
            # 游戏说明及规则 截图
            self.compareScreenResult("HBBDX_gameRule1",0, 0, 1080, 1730,"C3-1")
            self.driver.swipe(1500,600,50,600,2000)
            sleep(2)
            self.compareScreenResult("HBBDX_gameRule2",0, 0, 1080, 1730,"C3-1")
            self.driver.swipe(1500,600,50,600,2000)
            sleep(2)
            self.compareScreenResult("HBBDX_gameRule3",0, 0, 1080, 1730,"C3-1")
            self.driver.swipe(1500,600,50,600,2000)
            sleep(2)
            self.compareScreenResult("HBBDX_gameRule4",0, 0, 1080, 1730,"C3-1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/close").click()  # 点击 右上角关闭

            # 检查点5,游戏分享
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/share_game").click() # 点击 游戏分享
            # 游戏分享至 截图
            self.compareScreenResult("HBBDX_gameShareTo",0, 0, 1080, 1500,"C3-1")
            # # 朋友圈
            # print "1,朋友圈"
            # self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/wx_timeline_icon").click() # 点击 朋友圈
            # sleep(5)
            # self.compareScreenResult("HBBDX_gameShareToFriendCircle",0, 491, 1080, 755,"C3-1") # 朋友圈 截屏
            # self.driver.find_element_by_id("com.tencent.mm:id/ez").click() # 朋友圈, 点击 返回
            # self.driver.find_element_by_id("com.tencent.mm:id/bgp").click() # 朋友圈, 点击 退出
            # sleep(8)
            # self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/wx_timeline_icon").click() # 点击 朋友圈
            # self.driver.find_element_by_id("com.tencent.mm:id/ee").click() # 点击 发送
            # print "分享已完成, 请前往朋友圈检查..."
            # sleep(8)
            #
            # # 微信 群
            # print "2,微信群"
            # self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/wx_session_icon").click() # 点击 微信 群
            # sleep(5)
            # self.driver.find_element_by_id("com.tencent.mm:id/ez").click() # 点击 返回
            # sleep(8)
            # self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/wx_session_icon").click() # 点击 微信 群
            # tmpWeixin = self.driver.find_elements_by_id("com.tencent.mm:id/hw")
            # for i in tmpWeixin:
            #     if i.text=="tsz测试群":
            #         i.click()
            #         break
            # self.compareScreenResult("HBBDX_gameShareToWeixin",125, 620, 955, 1370,"C3-1") # 微信 截屏
            # self.driver.find_element_by_id("com.tencent.mm:id/bgp").click() # 点击 分享
            # self.driver.find_element_by_id("com.tencent.mm:id/a6x").click() # 点击 返回三藏红包
            # sleep(8)
            # print "分享已完成, 请前往微信群检查..."


            # QQ好友 ? 程序有问题
            print "3,QQ好友"
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/wx_qq_icon").click() # 点击 QQ好友
            sleep(5)
            self.driver.find_element_by_id("com.tencent.mobileqq:id/ivTitleBtnRightText").click() # 点击取消
            sleep(8)
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/wx_qq_icon").click() # 点击 QQ好友
            tmpQQ = self.driver.find_elements_by_id("com.tencent.mobileqq:id/name")
            for i in tmpQQ:
                if i.text=="选择群聊":
                    i.click()
                    break
            self.driver.swipe(800,800,800,800,500) # 选中 TSZtest
            self.compareScreenResult("HBBDX_gameShareToQQ",75, 600, 1005, 1395,"C3-1") # QQ 截屏
            self.driver.find_element_by_id("com.tencent.mobileqq:id/dialogRightBtn").click() # 点击 发送
            self.driver.find_element_by_id("com.tencent.mobileqq:id/dialogLeftBtn").click() # 点击 返回三藏红包
            sleep(8)
            print "分享已完成, 请前往QQ好友检查..."


            # # QQ空间 ?程序有问题
            # print "4,QQ空间"
            # self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/wx_qq_zone_icon").click() # 点击 QQ空间
            # sleep(5)
            # self.compareScreenResult("HBBDX_gameShareToQQarea",0, 76, 1080, 686,"C3-1") # QQ空间 截屏
            # self.driver.swipe(100,150,100,150,500) # QQ,点击取消
            # sleep(8)
            # self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/wx_qq_zone_icon").click() # 点击 QQ空间
            # sleep(3)
            # self.driver.find_element_by_id("com.tencent.mobileqq:id/ivTitleBtnRightText").click() # QQ空间,点击发表
            # sleep(5)
            # print "分享已完成, 请前往QQ空间检查..."

            # 新浪微博
            print "5,新浪微博"
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/wx_weibo_icon").click() # 点击 新浪微博
            sleep(5)
            self.compareScreenResult("HBBDX_gameShareToSinaweibo",0, 76, 1080, 735,"C3-1") # 新浪微博页面 截屏
            self.driver.find_element_by_id("com.sina.weibo:id/titleBack").click() # 新浪微博,点击取消
            self.driver.swipe(300,1200,300,1200,500) # 新浪微博,点击不保存
            sleep(8)
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/wx_weibo_icon").click() # 点击 新浪微博
            sleep(3)
            self.driver.find_element_by_id("com.sina.weibo:id/titleSave").click() # 新浪微博,点击发送
            sleep(5)
            print "分享已完成, 请前往新浪微博检查..."

            # 关闭 游戏分享至
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/close").click() # 点击 右上角关闭
            # 开始游戏
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/experience_or_start_game").click() # 点击 开始游戏
            # 游戏余额不足 请充值,截屏
            self.compareScreenResult("HBBDX_gameBalanceLackingPlsRecharge",180, 0, 1080, 1500,"C3-1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/close").click()
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/exit_game").click()
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/negative").click()
    def HBBDXstartGame(self):
        # C3-2，红包比大小开始游戏后，检查余额及数据库余额
        # 后台数据库重置 50元
        # 修改redis中修改commission_residue, t_user中commission_residue
        varCommission_residue = 5000
        self.cur.execute('select id from t_user where username="%s" order by id desc' % (oldPhone1))
        data0 = self.cur.fetchone()
        self.cur.execute('update t_user set commission_residue=%s where id=%s' % (varCommission_residue,data0[0]))
        self.conn.commit()
        pp = "t_user:id:"+str(data0[0])
        r = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
        r.hset(pp,"Commission_residue",varCommission_residue)

        # 进入游戏
        self.driver.find_element_by_id("com.mowin.tsz:id/button").click()  # 点击 进入游戏
        self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/experience_or_start_game").click() # 点击 开始游戏
        self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/account_balance_icon").click() # 点击 余额支付
        self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/amount_hint").send_keys("30")
        self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click() # 点击 确定
        self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click() # 点击 知道了
        self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/experience_or_start_game").click() # 点击 开始游戏


        sleep(121212)
          # # 点击 充值游戏余额 并截屏  ,注:截屏中现金余额 = 100.00
            # self.driver.swipe(300, 750, 300, 750, 500); # 点击 充值游戏余额
            # sleep(2)
            # img = "rechargegameamount"
            # compareResult = self.compareScreen(ScreenshotFolder + 'big_' + img + '.png',ScreenshotFolder + 'org_' + img + '.png',160, 0, 1080, 1920)
            # if compareResult > 1:
            #      print "Err,C3-2," + img + compareResult + ".png!"
            #      self.driver.save_screenshot(ErrorScreenshotFolder + compareResult + ".png")
            # elif compareResult == 0:
            #      print "Created,C3-2,org_" + img + ".png"
            #
            # # 充值游戏余额浮层中 , 点击 余额支付 并截屏
            # self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/account_balance_icon").click()
            # sleep(2)
            # img = "balancepay"
            # compareResult = self.compareScreen(ScreenshotFolder + 'big_' + img + '.png',ScreenshotFolder + 'org_' + img + '.png',160, 0, 1080, 1920)
            # if compareResult > 1:
            #      print "Err,C3-2," + img + compareResult + ".png!"
            #      self.driver.save_screenshot(ErrorScreenshotFolder + compareResult + ".png")
            # elif compareResult == 0:
            #      print "Created,C3-2,org_" + img + ".png"
            #
            # sleep(2)
            # cashAmount = self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/account_balance").text
            # cashAmount = cashAmount.split("￥")
            # print cashAmount[1]
            # self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/close").click() # 关闭 充值游戏余额浮层
            # myAcount = gameAmount + cashAmount
            # if myAcount == "0.00" or myAcount < "10.00":
            #     # 修改redis中修改commission_residue, t_user中commission_residue
            #     varCommission_residue = 10000
            #     self.cur.execute('select id from t_user where username="%s" order by id desc' % (oldPhone1))
            #     data0 = self.cur.fetchone()
            #     self.cur.execute('update t_user set commission_residue=%s where id=%s' % (varCommission_residue,data0[0]))
            #     self.conn.commit()
            #     pp = "t_user:id:"+str(data0[0])
            #     r = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
            #     r.hset(pp,"Commission_residue",varCommission_residue)

        # 点击 充值游戏余额 并截屏  ,注:截屏中现金余额 = 100.00
        self.driver.swipe(300, 750, 300, 750, 500); # 点击 充值游戏余额
        sleep(2)
        img = "rechargegameamount"
        compareResult = self.compareScreen(ScreenshotFolder + 'big_' + img + '.png',ScreenshotFolder + 'org_' + img + '.png',160, 0, 1080, 1920)
        if compareResult > 1:
             print "Err,C3-2," + img + compareResult + ".png!"
             self.driver.save_screenshot(ErrorScreenshotFolder + compareResult + ".png")
        elif compareResult == 0:
             print "Created,C3-2,org_" + img + ".png"

        # 充值游戏余额浮层中 , 点击 余额支付 并截屏
        self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/account_balance_icon").click()
        sleep(2)
        img = "balancepay"
        compareResult = self.compareScreen(ScreenshotFolder + 'big_' + img + '.png',ScreenshotFolder + 'org_' + img + '.png',160, 0, 1080, 1920)
        if compareResult > 1:
             print "Err,C3-2," + img + compareResult + ".png!"
             self.driver.save_screenshot(ErrorScreenshotFolder + compareResult + ".png")
        elif compareResult == 0:
             print "Created,C3-2,org_" + img + ".png"



        xx=gamebalance.split("￥") #游戏余额: ￥50.00
        self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance").click()
        sleep(1)
        # x = self.driver.get_window_size()['width']
        # y = self.driver.get_window_size()['height']
        # print x
        # print y
        if float(xx[1])>= 40.00:
            # 余额退回我的钱包
            sleep(2)
            self.driver.swipe(300, 850, 300, 850, 500); # 点击 余额退回我的钱包
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/amount_hint").send_keys("20")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click()
            chongzhitishi=self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/message").text
            if chongzhitishi<>"20.00元游戏余额已成功退回到你的钱包余额账户内。": print "Err,余额退回我的钱包!"
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click()
            sleep(3)
            # 检查 游戏余额是否减掉20元
            gamebalance = self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance").text # 获取游戏余额
            yy=gamebalance.split("￥")
            if float(yy[1])<>(float(xx[1])-20.00):print "Err,余额退回后计算错误!"
        elif float(xx[1])>= 10.00:
            print "Info, 游戏金额超过10元,可玩游戏"

            # # 检查是否是体验游戏
            # self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/experience_or_start_game").click()
            # # 游戏体验已结束, 进入正式游戏试试身手吧~
            # # com.mowin.tsz.thanthesize:id/message

        elif float(xx[1])>5.00 and float(xx[1])<10.00:
            print "Warning, 游戏金额不足10元,正在充值!"
            # 点击 开始游戏 进行充值
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/experience_or_start_game").click()
            sleep(2)
            self.driver.swipe(300, 750, 300, 750, 500); # 点击 充值游戏余额
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance_recharge").click() # 余额支付
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/amount_hint").send_keys("1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click()
            chongzhitishi=self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/message").text
            if chongzhitishi<>"已成功充值1.00元游戏余额, 快进入游戏试试手气吧。": print "Err,充值游戏余额!"
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click()
            sleep(3)
            # 检查 游戏余额是否加1元
            gamebalance = self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance").text # 获取游戏余额
            zz=gamebalance.split("￥")
            if float(zz[1])<>(float(xx[1])+1.00):print "Err,充值游戏余额后后计算错误!"
        elif float(xx[1])<5.00 :
            self.driver.swipe(300, 750, 300, 750, 500); # 点击 充值游戏余额
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance_recharge").click() # 余额支付
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/amount_hint").send_keys("1")
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click()
            chongzhitishi=self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/message").text
            if chongzhitishi<>"已成功充值1.00元游戏余额, 快进入游戏试试手气吧。": print "Err,充值游戏余额!"
            self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/positive").click()
            sleep(3)
            # 检查 游戏余额是否加1元
            gamebalance = self.driver.find_element_by_id("com.mowin.tsz.thanthesize:id/balance").text # 获取游戏余额
            zz=gamebalance.split("￥")
            if float(zz[1])<>(float(xx[1])+1.00):print "Err,充值游戏余额后后计算错误!"

    # 我
    def drv_me(self):
        # 我
        print "\n"
        self.driver.find_element_by_id("com.mowin.tsz:id/my_tab").click() # 我
        if self.isElement("com.mowin.tsz:id/no_login_item")==True: #无登录情况下
            self.driver.find_element_by_id("com.mowin.tsz:id/no_login_item").click()     # 点击登录
            sleep(2)
            self.driver.swipe(100, 100, 100, 100, 500)  # 无密码快捷登录 页面,点击 左上角的关闭,应返回首页
            print "OK, 无密码快捷登录,关闭按钮"
            self.driver.find_element_by_id("com.mowin.tsz:id/my_tab").click() # 我
            self.driver.find_element_by_id("com.mowin.tsz:id/no_login_item").click()     # 点击登录
            self.userLogin()
        sleep(2)
        self.TestcaseModule()
    def myList(self):
        #C4-1, 我页面中功能清单，如个人钱包、购物订单、群账户、邀请好友、收藏等功能
        self.compareScreenResult("myList",0, 75, 1080, 1702,"") # 我 列表页截图, 13816109050对应的是: 头像是黑中绿原点,令狐冲,john,男,红包炸弹二维码充值


    def myInfo(self,varNickname,varSign,varArea):
         #C4-2, 顶部个人信息，如头像、手机号、性别、个性签名、二维码
         sleep(3)
         # 检查 右侧 二维码
         self.driver.find_element_by_id("com.mowin.tsz:id/qr_code").click()
         self.compareScreenResult("qr_code",90,271,990, 1505,"") # 我 的二维码 截图
         self.driver.swipe(80, 250, 80, 250, 500)  # 点击 页面空白处
         sleep(12121)

         # 检查 昵称
         if self.isElement("com.mowin.tsz:id/name")==True:
              text_Search=self.driver.find_element_by_id("com.mowin.tsz:id/name").text
              if varNickName<>text_Search:
                  print "Err,C1-2,我-昵称 错误!"
         else:
             print "Err，C1-2,我-昵称 不存在!"
         # 检查 签名
         if self.isElement("com.mowin.tsz:id/sign")==True:
              text_Sign=self.driver.find_element_by_id("com.mowin.tsz:id/sign").text
              if text_Sign<>"编辑个性签名" :
                  print "Err,C1-2,我-签名 错误!"
         else:
             print "Err，C1-2,我-签名 不存在!"



         # 编辑个人信息,检查返回按钮\标题\昵称\个性签名\性别\常住地\手机号
         self.driver.find_element_by_id("com.mowin.tsz:id/user_name_and_gender_layout").click()
         # 检查 返回按钮
         if self.isElement("com.mowin.tsz:id/back")<>True:print "Err，C1-2,个人信息-返回按钮 不存在!"
         # 检查 标题文字
         if self.driver.find_element_by_id("com.mowin.tsz:id/title").text<>u"个人信息":print "Err,C1-2,个人信息-标题文字!"
         # 检查 昵称文字 和 昵称 ,修改昵称
         if self.driver.find_element_by_id("com.mowin.tsz:id/nick_title").text<>u"昵称":print "Err，C1-2,个人信息-昵称文字!"
         if self.driver.find_element_by_id("com.mowin.tsz:id/nick_name").text<>varNickName:print "Err，C1-2,个人信息-昵称!"
         self.driver.find_element_by_id("com.mowin.tsz:id/nick_name").click()
         # 修改昵称
         if self.driver.find_element_by_id("com.mowin.tsz:id/title").text<>u"昵称":print "Err，C1-2,个人信息-昵称-标题文字!"
         self.driver.find_element_by_class_name("android.widget.EditText").clear()
         self.driver.find_element_by_class_name("android.widget.EditText").send_keys(varNickname)
         self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'保存')]").click()
         if self.driver.find_element_by_id("com.mowin.tsz:id/nick_name").text<>varNickname:print "Err，C1-2,个人信息-昵称修改后!"

         # 检查 个人签名文字 和 个人签名
         if self.driver.find_element_by_id("com.mowin.tsz:id/sign_title").text<>u"个性签名":print "Err，C1-2,个人信息-个性签名文字!"
         if self.driver.find_element_by_id("com.mowin.tsz:id/sign").text<>u"编辑个性签名":print "Err，C1-2,个人信息-个性签名!"
         self.driver.find_element_by_id("com.mowin.tsz:id/sign").click()
         # 修改个性签名
         if self.driver.find_element_by_id("com.mowin.tsz:id/title").text<>u"个性签名":print "Err，C1-2,个人信息-个人签名-标题文字!"
         self.driver.find_element_by_xpath("//android.widget.EditText[contains(@index,0)]").send_keys(varSign)
         self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'保存')]").click()
         if self.driver.find_element_by_id("com.mowin.tsz:id/sign").text<>varSign:print "Err，C1-2,个人信息-个性签名修改后!"

         # 检查 性别文字 和 性别
         if self.driver.find_element_by_id("com.mowin.tsz:id/gender_title").text<>u"性别":print "Err，C1-2,个人信息-性别文字!"
         text_sex=self.driver.find_element_by_id("com.mowin.tsz:id/gender").text
         if text_sex<>u"男":print "Err，C1-2,个人信息-性别!"
         self.driver.find_element_by_id("com.mowin.tsz:id/gender").click()
         # 修改性别
         if text_sex=="男":
             self.driver.find_element_by_id("com.mowin.tsz:id/famale").click()
         else:
             self.driver.find_element_by_id("com.mowin.tsz:id/male").click()
         text_sex=self.driver.find_element_by_id("com.mowin.tsz:id/gender").text
         if text_sex<>"女":print "Err，C1-2,个人信息-性别修改后!"

         # 检查 常住地文字 和 手机号
         if self.driver.find_element_by_id("com.mowin.tsz:id/always_place_title").text<>u"常驻地":print "Err，C1-2,个人信息-常驻地文字!"
         if self.driver.find_element_by_id("com.mowin.tsz:id/always_place").text<>u"上海":print "Err，C1-2,个人信息-常住地!"
         self.driver.find_element_by_id("com.mowin.tsz:id/always_place").click()
         # 修改地区
         text_area=self.driver.find_elements_by_id("com.mowin.tsz:id/city_name")
         for t_area in text_area:
             if t_area.get_attribute("text")==varArea:
                 t_area.click()
                 break
         sleep(3)
         if self.driver.find_element_by_id("com.mowin.tsz:id/always_place").text<>varArea:print "Err，C1-2,个人信息-常住地修改后!"
         # 检查 手机号文字 和 手机号
         if self.driver.find_element_by_id("com.mowin.tsz:id/phone_title").text<>u"手机号":print "Err，C1-2,个人信息-手机号文字!"
         if self.driver.find_element_by_id("com.mowin.tsz:id/phone").text<>varNickName:print "Err，C1-2,个人信息-手机号!"

         self.driver.find_element_by_id("com.mowin.tsz:id/back").click()

         # 检查 我 页面中个人信息修改后的结果 ,检查 昵称\个性签名
         # 检查 昵称修改后
         if self.driver.find_element_by_id("com.mowin.tsz:id/name").text<> varNickname:print "Err,C1-2,我-个人信息-昵称修改后!"
         # 检查 个性签名修改后
         if self.driver.find_element_by_id("com.mowin.tsz:id/sign").text<> u"个性签名: "+varSign :print "Err,C1-2,我-个人信息-个性签名修改后!"

         # 编辑个人信息,检查返回按钮\标题\昵称\个性签名\性别\常住地\手机号
         self.driver.find_element_by_id("com.mowin.tsz:id/user_name_and_gender_layout").click()
         # 恢复 默认昵称\个性签名\性别\常驻地
         # 恢复昵称
         self.driver.find_element_by_id("com.mowin.tsz:id/nick_name").click()
         self.driver.find_element_by_class_name("android.widget.EditText").clear()
         self.driver.find_element_by_class_name("android.widget.EditText").send_keys(varNickName)
         self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'保存')]").click()
         # 恢复个性签名
         self.driver.find_element_by_id("com.mowin.tsz:id/sign").click()
         self.driver.find_element_by_xpath("//android.widget.EditText[contains(@index,0)]").clear()
         self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'保存')]").click()
         # 恢复性别
         self.driver.find_element_by_id("com.mowin.tsz:id/gender").click()
         self.driver.find_element_by_id("com.mowin.tsz:id/male").click()
         # 恢复常驻地
         self.driver.find_element_by_id("com.mowin.tsz:id/always_place").click()
         for t_area in text_area:
             if t_area.get_attribute("text")=="上海":
                 t_area.click()
                 break
         self.driver.find_element_by_id("com.mowin.tsz:id/back").click()


    def meWalletAccount(self):
        #C4-2-1，检查账户余额 、账户明细、立即提现、余额充值及页面信息
        self.driver.find_element_by_id("com.mowin.tsz:id/my_wallet").click()
        # 获取账户余额
        varAccountbefore=self.driver.find_element_by_id("com.mowin.tsz:id/mywalleny_allmoney").text
        print self.driver.find_element_by_id("com.mowin.tsz:id/mywalleny_allmoney").text
        # # 余额充值
        # self.driver.find_element_by_id("com.mowin.tsz:id/balance_recharge").click()

        # ######### 以下是 余额充值详情页,可单独封装
        # # 充值金额 1yuan
        # self.driver.find_element_by_id("com.mowin.tsz:id/amount_edit").send_keys("1")
        # # 点击 充值按钮
        # self.driver.find_element_by_id("com.mowin.tsz:id/recharge").click()
        # sleep(6)
        # # 使用支付微信账户登录 ,如用户未登录微信
        # if self.isElement("com.tencent.mm:id/ew")==True:
        #     self.driver.find_element_by_id("com.tencent.mm:id/ew").send_keys("11114573029")
        #     self.driver.find_element_by_id("com.tencent.mm:id/ew").send_keys("xlq2009081424")
        #     self.driver.find_element_by_id("com.tencent.mm:id/b4n").click()
        #
        # # 获取账户充值号 充值金额
        # print self.driver.find_element_by_id("com.tencent.mm:id/cp6").text # 账户充值191557
        # print self.driver.find_element_by_id("com.tencent.mm:id/coa").text # 1.01
        # print self.driver.find_element_by_id("com.tencent.mm:id/co9").text # 三藏闪惠
        # # 点击立即支付
        # self.driver.find_element_by_id("com.tencent.mm:id/cpq").click() # 立即支付
        # # 820124
        # sleep(4)
        # self.driver.swipe(540, 1600, 540, 1600, 500); # 点击 8
        # sleep(1)
        # self.driver.swipe(540, 1300, 540, 1300, 500); # 点击 2
        # sleep(1)
        # self.driver.swipe(540, 1800, 540, 1800, 500); # 点击 0
        # sleep(1)
        # self.driver.swipe(200, 1300, 200, 1300, 500); # 点击 1
        # sleep(1)
        # self.driver.swipe(540, 1300, 540, 1300, 500); # 点击 2
        # sleep(1)
        # self.driver.swipe(200, 1400, 200, 1400, 500); # 点击 4
        # sleep(8)
        # self.driver.find_element_by_id("com.tencent.mm:id/ef").click() # 微信平台点击完成
        # # 充值成功 弹框提示信息
        # print self.driver.find_element_by_id("com.mowin.tsz:id/recharge_hint").text
        # self.driver.find_element_by_id("com.mowin.tsz:id/got_it").click() # 知道了
        # # 检查充值以前的账户余额值 与 充值后的值对比.
        # sleep(3)
        # varAccountafter=self.driver.find_element_by_id("com.mowin.tsz:id/mywalleny_allmoney").text
        # if varAccountbefore <> varAccountafter :
        #     print "Error,C4-2-1,账户余额充值前"+str(varAccountbefore)+"<>充值后金额"+str(varAccountafter)+"不一致"


        # 账户明细 ,检查充值金额.
        self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'账户明细')]").click()
        # 账户明细 - 明细金额
        varAccountDetailsCash =self.driver.find_elements_by_id("com.mowin.tsz:id/money")
        count=0
        d_list=[]
        e_list=[]
        f_list=[]

        for var_AccountDetailsCash in varAccountDetailsCash:
            # print var_AccountDetailsCash.text
            d_list.append(var_AccountDetailsCash.text)
            count=count+1
        print count
        for var_AccountDetailsCash in varAccountDetailsCash:
             if var_AccountDetailsCash.text<>u"1.00元":
                 print "Error,C4-2-1,账户明细 - 金额为" + str(var_AccountDetailsCash.text)
             break
        sleep(3)

        # 账户明细 - 明细类型
        varAccountDetailsType = self.driver.find_elements_by_id("com.mowin.tsz:id/item_accountdetail_hint")
        for var_AccountDetailsType in varAccountDetailsType:
            print var_AccountDetailsType.text
            e_list.append(var_AccountDetailsType.text)
        for var_AccountDetailsType in varAccountDetailsType:
             if var_AccountDetailsType.text<>u"账户余额充值":
                 print "Error,C4-2-1,账户明细 - 类型为" + str(var_AccountDetailsType.text)
             break
        sleep(3)

        # 账户明细 - 明细时间
        varAccountDetailsTime = self.driver.find_elements_by_id("com.mowin.tsz:id/item_account_detail_time")
        for var_AccountDetailsTime in varAccountDetailsTime:
            print var_AccountDetailsTime.text
            f_list.append(var_AccountDetailsTime.text)

        print str(e_list[0]) +"," +str(d_list[0]) +"," + str(f_list[0])
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click()  # 返回


        # 立即提现 ,
        self.driver.find_element_by_id("com.mowin.tsz:id/withdrawal_button").click()
        # 可提现金额 来自 commission_residue
        print self.driver.find_element_by_id("com.mowin.tsz:id/with_drawal_balance").text
        varGetCash = self.driver.find_element_by_id("com.mowin.tsz:id/with_drawal_balance").text
        varGetCash = varGetCash.replace('¥','')
        self.cur.execute('select commission_residue from t_user where username=%s ' % (oldPhone1))
        data9 = self.cur.fetchone()
        dataCommission_residue = data9[0]/100.00
        if varGetCash <> dataCommission_residue :
            print "Error,C4-2-1,立即提现 - 可提现金额与数据库不一致"

        # 添加银行卡
        self.driver.find_element_by_id("com.mowin.tsz:id/select_bank_card").click()
        self.driver.find_element_by_id("com.mowin.tsz:id/bankcard_choose").click() # 发卡行
        self.driver.swipe(540, 1300, 540, 1300, 500); # 选择银行
        self.driver.find_element_by_id("com.mowin.tsz:id/add_bankcard_number").send_keys("1234567891234567891")
        self.driver.find_element_by_id("com.mowin.tsz:id/add_bankcard_name").send_keys("john")
        self.driver.find_element_by_id("com.mowin.tsz:id/add_bankcard_sure").click()
        self.driver.find_element_by_id("com.mowin.tsz:id/add_card_sure").click() # 确认提交
        self.driver.find_element_by_id("com.mowin.tsz:id/add_card_sure").send_keys("10") # 提现金额
        self.driver.find_element_by_id("com.mowin.tsz:id/withdrawal_password_not").click()
        self.driver.swipe(540, 300, 540, 1300, 500); # 请选择安全问题
    def me2(self):
        # 我 打开app,点击我,跳到登录页面,登录后跳到 我 页面,检查我 页面上标题
        # 检查 我 标题
        self.driver.find_element_by_id("com.mowin.tsz:id/my_tab").click()
        self.userLogin()
        if self.driver.find_element_by_id("com.mowin.tsz:id/title").text<>u"我":print "Err,C1-1,我标题文字!"
        # 检查私信及连接
        if self.driver.find_element_by_id("com.mowin.tsz:id/private_msg").text<>u"私信":print "Err,C1-1,私信标题!"
        if self.isElement("com.mowin.tsz:id/private_msg")==True:
            self.driver.find_element_by_id("com.mowin.tsz:id/private_msg").click()
            # 私信页面, 检查标题\内容
            if self.driver.find_element_by_id("com.mowin.tsz:id/title").text<>u"私信":print "Err,C1-1,私信文字!"

            # 私信 - 检查头像
            if self.isElement("com.mowin.tsz:id/thumb_private")<>True:print "Err，C1-1,私信-头像 不存在!"
            # 私信 - 检查 138****1115的红包群 页面返回按钮,标题
            # 返回按钮
            if self.isElement("com.mowin.tsz:id/back")<>True:print "Err，C1-1,私信-红包群信息-返回按钮 不存在!"
            # 标题
            if self.isElement("com.mowin.tsz:id/nick_name")==True:
                text_actual= varNickName + "的红包群"
                if self.driver.find_element_by_id("com.mowin.tsz:id/nick_name").text<>text_actual:print "Err,C1-1,私信-'" + varNickName + "的红包群'文字!"
                self.driver.find_element_by_id("com.mowin.tsz:id/private_layout").click()
            else:
                 print "Err，C1-1,私信-"+ varNickName +"的红包群 不存在!"

            # 私信 - 138****1115的红包群页面,检查返回按钮\标题\群成员Icon连接\内容=点击右上角，选择群成员进行私信
            # 检查返回按钮
            if self.isElement("com.mowin.tsz:id/back")<>True:print "Err，C1-1,私信-"+varNickName+"的红包群-返回按钮 不存在!"
            # 检查标题
            text_title = varNickName+"的红包群"
            if self.driver.find_element_by_id("com.mowin.tsz:id/title").text<>text_title:print "Err,C1-1,'" +varNickName + "的红包群'标题!"
            # 检查 内容 = 点击右上角，选择群成员进行私信
            if self.driver.find_element_by_id("com.mowin.tsz:id/no_data_layout").text<>u"点击右上角，选择群成员进行私信":print "Err,C1-1,私信-'"+varNickName+"红包群'内 文字!"
            # 检查 右上角 群成员icon,并点击.
            self.driver.find_element_by_xpath("//android.widget.ImageView[contains(@index,2)]").click()

            # 私信 - 红包群信息页面 ,检查 返回按钮\标题\头像\电话号码\群主\所有组成员 = 全部群成员(1)
            if self.isElement("com.mowin.tsz:id/back")<>True:print "Err，C1-1,私信-红包群信息-返回按钮 不存在!"
            # 检查标题
            if self.driver.find_element_by_id("com.mowin.tsz:id/title").text<>u"红包群信息":print "Err,C1-1,私信-红包群信息 标题文字错误!"

            # 检查头像
            if self.isElement("com.mowin.tsz:id/head_thumb")<>True:print "Err，C1-1,私信-红包群信息-头像 不存在!"
            # 检查电话号码
            if self.driver.find_element_by_id("com.mowin.tsz:id/name").text<>varNickName:print "Err,C1-1,私信-红包群信息-"+varNickName+"文字错误!"
            # 检查群主
            if self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'群主')]").text<>u"群主":print "Err,C1-1,私信-红包群信息-群主 文字错误!"
            # 检查 全部群成员(1)
            if self.isElement("com.mowin.tsz:id/all_group_member")==True:
                 if self.driver.find_element_by_id("com.mowin.tsz:id/all_group_member").text<>u"全部群成员(1)":print "Err,C1-1,私信-红包群信息-全部群成员(1) 文字错误!"
                 # 私信 - 群成员(1) ,检查 返回按钮\标题\搜索框\头像\昵称
                 self.driver.find_element_by_id("com.mowin.tsz:id/all_group_member").click()
                 if self.isElement("com.mowin.tsz:id/back")<>True:print "Err，C1-1,私信-群成员(1)-返回按钮 不存在!"
                 # 检查标题
                 if self.driver.find_element_by_id("com.mowin.tsz:id/title").text<>u"群成员(1)":print "Err,C1-1,私信-红包群信息 标题文字错误!"
                 # 检查 搜索框
                 if self.isElement("com.mowin.tsz:id/search_edit")==True:
                      if self.driver.find_element_by_id("com.mowin.tsz:id/search_edit").text<>u"搜索":print "Err,C1-1,私信-红包群信息-搜索 文字错误!"
                 else:
                      print "Err，C1-1,私信-群成员(1)-搜索框 不存在!"
                 # 检查 头像
                 if self.isElement("com.mowin.tsz:id/thumb")<>True:print "Err，C1-1,私信-群成员(1)-头像 不存在!"
                 # 检查 昵称
                 if self.isElement("com.mowin.tsz:id/nick_name")==True:
                       if self.driver.find_element_by_id("com.mowin.tsz:id/nick_name").text<>varNickName:print "Err,C1-1,私信-红包群信息-昵称 文字错误!"
                 else:
                    print "Err，C1-1,私信-群成员(1)-昵称 不存在!"
                 self.driver.find_element_by_id("com.mowin.tsz:id/back").click()
            else:
                 print "Err，C1-1,私信-红包群信息-全部群成员(1) 文字不存在!"

            self.driver.find_element_by_id("com.mowin.tsz:id/back").click()
            self.driver.find_element_by_id("com.mowin.tsz:id/back").click()
            self.driver.find_element_by_id("com.mowin.tsz:id/back").click()
        else:
            print "Err,C1-1 私信icon!"
    def myWalletGetcash(self,oldPhone1,xlGetCash):
         # 前置条件 : 已添加银行卡,密码设置,安全提示.(此部分未做)
         #C4-3，钱包－账户余额，点击立即提现
         print "12121211111111"
         sleep(3)
         tGetCash = xlGetCash * 100 # 用于数据库中值的比较, 如10元 = 1000 , 12.34元=1234
         self.driver.find_element_by_id("com.mowin.tsz:id/my_tab").click()  # 点击 我
         self.driver.find_element_by_id("com.mowin.tsz:id/my_wallet").click() # 点击 钱包

         if self.isElement("com.mowin.tsz:id/withdrawal_button")<>True:print "Err,C4-3,钱包-立即提现按钮不存在!"
         else:self.driver.find_element_by_id("com.mowin.tsz:id/withdrawal_button").click()          # 点击 立即提现
         appGetCash = self.driver.find_element_by_id("com.mowin.tsz:id/with_drawal_balance").text  # ¥5.00 # 获取原始可提现金额的值

         # 如果可提现金额小于10元,则后台系统自动修改数据库和redis值 = 100元.
         conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
         cur = conn.cursor()
         cur.execute('select id,commission_residue from t_user where username="%s" ' % (oldPhone1))
         t1 = cur.fetchone()
         if t1[1]<1000:
             print "Warning,C4-3,可提现金额" + str(appGetCash) + "元 , 由于小于10元系统自动充值100元"
             cur.execute('update t_user set commission_residue=10000 where username="%s" ' % (oldPhone1))
             conn.commit()
             r2 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
             r2.hset("t_user:id:" + str(t1[0]),"Commission_residue","10000")
         self.driver.find_element_by_id("com.mowin.tsz:id/back").click()
         self.driver.find_element_by_id("com.mowin.tsz:id/withdrawal_button").click()
         sleep(4)

         # 检查 app可提现金额 与 表中 commission_residue 是否一致
         appGetCash100 = self.driver.find_element_by_id("com.mowin.tsz:id/with_drawal_balance").text  # ¥100.00
         appGetCash100 = appGetCash100.replace('¥','')
         conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
         cur = conn.cursor()
         cur.execute('select commission_residue from t_user where username="%s" ' % (oldPhone1))
         t2 = cur.fetchone()
         tCommission_residue = "%.2lf" % (t2[0]/100)
         if appGetCash100 <> tCommission_residue :print "Error,C4-3,立即提现 - 可提现金额与数据库不一致!"
         else: print "OK,C4-3,可提现金额" + str(appGetCash100) + "元"

         #  添加银行卡
         if self.isElement("com.mowin.tsz:id/bank_card_info")<>True:
             self.driver.find_element_by_id("com.mowin.tsz:id/withdrawal_bankname").click()
             self.driver.find_element_by_id("com.mowin.tsz:id/bankcard_choose").click() # 发卡行
             self.driver.swipe(540, 1300, 540, 1300, 500); # 选择银行
             self.driver.find_element_by_id("com.mowin.tsz:id/add_bankcard_number").send_keys("1234567891234567891")
             self.driver.find_element_by_id("com.mowin.tsz:id/add_bankcard_name").send_keys("john")
             self.driver.find_element_by_id("com.mowin.tsz:id/add_bankcard_sure").click() # 下一步
             self.driver.find_element_by_id("com.mowin.tsz:id/add_card_sure").click() # 确认提交

         self.driver.find_element_by_id("com.mowin.tsz:id/withdrawal_amount").send_keys(xlGetCash)  # 提现金额

         # 未设置提现密码 , 提现密码
         if self.isElement("com.mowin.tsz:id/withdrawal_password_not")==True:
             self.driver.find_element_by_id("com.mowin.tsz:id/withdrawal_password_not").click()
             sleep(2)
             self.driver.swipe(540, 300, 540, 300, 500); # 请选择安全问题
             sleep(2)
             self.driver.swipe(500, 680, 500, 680, 500); # 我的第一个班主任名字
             sleep(4)
             self.driver.find_element_by_id("com.mowin.tsz:id/security_hint").send_keys("mailaoshi")
             self.driver.find_element_by_id("com.mowin.tsz:id/security_password").click() # 下一步,设置提现密码
             # 设置提现密码 对应的表 ukardapp,t_other_security_question, 如要清楚密码,删除记录即可.
             self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/child::android.widget.FrameLayout[1]/android.widget.RelativeLayout/android.widget.EditText[1]").send_keys("123456")
             sleep(3)
             self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/child::android.widget.FrameLayout[2]/android.widget.RelativeLayout/android.widget.EditText[1]").send_keys("123456")
             sleep(3)
             self.driver.find_element_by_id("com.mowin.tsz:id/withdrawalsecurity_makesure").click() # 确定

         self.driver.find_element_by_id("com.mowin.tsz:id/withdrawal_password").send_keys("123456") # 请输入提现密码

         # 获取验证码
         self.driver.find_element_by_id("com.mowin.tsz:id/withdrawal_get_code").click() # 获取验证码
         sleep(5)
         conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
         cur = conn.cursor()
         cur.execute('select verify_code from ta_message where phone=%s order by id desc limit 1' % (oldPhone1))
         t3 = cur.fetchone()
         sleep(4)
         self.driver.find_element_by_id("com.mowin.tsz:id/verify_code").send_keys(t3[0])
         self.driver.find_element_by_id("com.mowin.tsz:id/withdrawal_button").click() # 点击 立即提现 ,成功后返回到钱包页面
         sleep(4)

         # 提现成功后,检查 last_withdraw_time是否保存当前日期,
         conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
         cur = conn.cursor()
         cur.execute('select id,commission_residue,last_withdraw_time from t_user where username="%s" order by id desc limit 1' % (oldPhone1))
         t4 = cur.fetchone()
         if t4[2]<>"":print "OK,C4-3,提现成功,t_user,last_withdraw_time保存日期"
         else:print "Error,C4-3,提现失败,t_user,last_withdraw_time为空"
         # 提现金额是否被扣除
         tCommission_residue= t2[0]-tGetCash
         if t4[1]==tCommission_residue:print "OK,C4-3,t_user,commission_residue"
         else:print "Error,C4-3,t_user,commission_residue"

         # 检查 redis中, t_user , commission_residue
         r2 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
         redisCommission_residue = r2.hget("t_user:id:"+str(t4[0]),"Commission_residue")
         if int(redisCommission_residue)==int(tCommission_residue) :print "OK,C4-3,redis,t_user,Commission_residue"
         else:print "Error,C4-3,redis,t_user,Commission_residue"

         # 检查 提现表 是否记录xlGetCash + 手续费2元
         conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
         cur = conn.cursor()
         cur.execute('select id from t_user_withdraw where user_id=%s and amount=%s and charge=200 order by id desc limit 1' % (t4[0],tGetCash))
         t5 = cur.fetchone()
         if t5[0]<>"":print "OK,C4-3,t_user_withdraw,amount=" +str(tGetCash)+ ",charge=200"
         else:print "Error,C4-3,t_user_withdraw,amount=" +str(tGetCash)+ ",charge=200"


         # 再次 立即提现,当天(0:00:00-24:59:59)只能提现1次,第二次触发提现时 立即提现按钮置灰.
         self.driver.find_element_by_id("com.mowin.tsz:id/withdrawal_button").click()# 点击 立即提现
         appGetCash = self.driver.find_element_by_id("com.mowin.tsz:id/with_drawal_balance").text  # ¥5.00 # 获取原始可提现金额的值
         print "OK,C4-3,第一次提现成功,可提现金额变为 " + str(appGetCash) + "元"
         self.driver.find_element_by_id("com.mowin.tsz:id/withdrawal_amount").send_keys(xlGetCash)# 提现金额
         self.driver.find_element_by_id("com.mowin.tsz:id/withdrawal_password").send_keys("102585") # 提现密码
         self.driver.find_element_by_id("com.mowin.tsz:id/withdrawal_get_code").click() # 点击 获取验证码
         sleep(5)
         # 获取验证码
         conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
         cur = conn.cursor()
         cur.execute('select verify_code from ta_message where phone=%s order by id desc limit 1' % (oldPhone1))
         t6 = cur.fetchone()
         sleep(4)
         self.driver.find_element_by_id("com.mowin.tsz:id/verify_code").send_keys(t6[0])
         self.driver.find_element_by_id("com.mowin.tsz:id/withdrawal_button").click() # 点击 立即提现
         sleep(5)
         # 一天只能提现1次哦! 重复提现则按钮变灰.
         appGetCashButton=self.driver.find_element_by_id("com.mowin.tsz:id/withdrawal_button").is_enabled()
         if appGetCashButton==False: print "OK,C4-3,第二次提现,一天只能提现1次,立即提现按钮变灰."
         else: print "Error,C4-3,第二次提现,一天怎么能提现多次,立即按钮仍然为红色!"
         self.driver.find_element_by_id("com.mowin.tsz:id/back").click()

         # 恢复原样, 清除 t_user表中 last_withdraw_time 值
         conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
         cur = conn.cursor()
         cur.execute('update t_user set last_withdraw_time=null  where username="%s" ' % (oldPhone1))
         # # 恢复 原来commission_residue值
         # cur.execute('update t_user set commission_residue=%s  where username="%s" ' % (t1[1],oldPhone1))
         conn.commit()

         # 检查账户明细
         self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'账户明细')]").click()
         self.myWalletAccountDetail("all","","")
         self.myWalletAccountDetail("type","本人提现","")
         self.myWalletAccountDetail("1","","")
    def myWalleRecharge(self,varRecharge):
        #C4-4，钱包－账户余额，点击余额充值
        sleep(3)
        # varRecharge=1  #充值金额 = 1元

        self.driver.find_element_by_id("com.mowin.tsz:id/my_tab").click()  # 点击 我
        self.driver.find_element_by_id("com.mowin.tsz:id/my_wallet").click() # 点击 钱包
        sleep(5)
        self.driver.find_element_by_id("com.mowin.tsz:id/balance_recharge").click() # 点击 余额充值
        self.driver.find_element_by_id("com.mowin.tsz:id/amount_edit").send_keys(varRecharge) #
        sleep(3)
        # 检查 最终金额值  规则: 充值金额/(1-0.006) 结果只如不舍,如: 50/(1-0.006)=50.31
        appPay=self.driver.find_element_by_id("com.mowin.tsz:id/pay_amount").text  #¥50.31  appPay[1:] =   ¥50.31
        calPay=varRecharge/(1-0.006)
        strCalPay=str(calPay)  # 12.34567890
        dot=strCalPay.split(".")
        dotLeftX=dot[0] #12
        dotRight3=dot[1][2:3] #5
        if int(dotRight3)<>0:
            hh = float(dotLeftX + "." + dot[1][:2])
            hh=hh + 0.01
        if appPay=="¥" + str(hh):print "OK,C4-4,微信支付金额" + str(varRecharge) + "元,微信收取0.6%后金额合计 " + str(appPay) +"元"
        else:print "Err,C4-4,微信支付金额收取交易手续费计算错误"

        self.driver.find_element_by_id("com.mowin.tsz:id/recharge").click() # 点击 充值
        print "正在生成预订单..."
        sleep(8)
        self.weixinPay("1114573029","xlq2009081424",varRecharge)
    def weixinPay(self,weixinName,weixinPassword,varRechargeDotTwoYuan):
        # 微信支付 (微信账号登录\支付\账户明细中检查是否支付成功
        sleep(5)
        # 判断 varRechargeDotTwoYuan 金额格式,默认金额格式是保留小数点后2位并加元,如 50.00元,
        # 如 100 ,则格式化成: 100.00元
        # 如 100. ,则格式化成: 100.00元
        # 如 100.1 ,则格式化成: 100.10元
        # 如 100.12 ,则格式化成: 100.12元
        # 如 100.1234 ,则格式化成: 100.12元
        if '.' in str(varRechargeDotTwoYuan):
            strvarRechargeDotTwoYuan=str(varRechargeDotTwoYuan)
            dot=strvarRechargeDotTwoYuan.split(".")
            dotLeftX=dot[0] #12
            dotRightLen=len(dot[1])
            if dotRightLen==1:
                dotRight = dot[1]+"0"
            elif dotRightLen >2:
                dotRight = dot[1][0:2]
            else:
                dotRight = dot[1]
            varRechargeDotTwoYuan = dotLeftX + "." + dotRight + "元"
        else:
            varRechargeDotTwoYuan=str(varRechargeDotTwoYuan) + ".00元"

        # 第三方 登录微信 页面
        if self.isElement("com.tencent.mm:id/b4n")==True:
            self.driver.find_element_by_xpath("//android.widget.EditText[contains(@index,'1')]").send_keys(weixinName)
            self.driver.find_element_by_xpath("//android.widget.EditText[contains(@NAF,'true')]").send_keys(weixinPassword)
            self.driver.find_element_by_id("com.tencent.mm:id/b4n").click()
            sleep(8)
        # 获取账户充值号\充值金额\收款人
        print self.driver.find_element_by_id("com.tencent.mm:id/cp6").text # 账户充值191557
        print self.driver.find_element_by_id("com.tencent.mm:id/coa").text # 1.01
        print self.driver.find_element_by_id("com.tencent.mm:id/co9").text # 三藏闪惠
        self.driver.find_element_by_id("com.tencent.mm:id/cpq").click() # 立即支付
        sleep(4)
        self.driver.swipe(540, 1600, 540, 1600, 500); # 点击 8
        sleep(1)
        self.driver.swipe(540, 1300, 540, 1300, 500); # 点击 2
        sleep(1)
        self.driver.swipe(540, 1800, 540, 1800, 500); # 点击 0
        sleep(1)
        self.driver.swipe(200, 1300, 200, 1300, 500); # 点击 1
        sleep(1)
        self.driver.swipe(540, 1300, 540, 1300, 500); # 点击 2
        sleep(1)
        self.driver.swipe(200, 1400, 200, 1400, 500); # 点击 4
        print "微信支付..."
        sleep(8)
        print self.driver.find_element_by_id("com.tencent.mm:id/co6").text # 支付成功
        print self.driver.find_element_by_id("com.tencent.mm:id/cof").text # 商品: 账户充值191567
        print self.driver.find_element_by_id("com.tencent.mm:id/col").text # 交易时间: 2016-07-27 14:50
        print self.driver.find_element_by_id("com.tencent.mm:id/coo").text # 支付方式:交通银行
        print self.driver.find_element_by_id("com.tencent.mm:id/coq").text # 交易单号:4010112001201607279895607537
        self.driver.find_element_by_id("com.tencent.mm:id/ef").click() # 点击 完成

        # 弹框提示 充值成功
        print self.driver.find_element_by_id("com.mowin.tsz:id/recharge_hint").text # 本次充值1.00元已入你的账户
        self.driver.find_element_by_id("com.mowin.tsz:id/got_it").click() # 点击 知道了

        # 检查 账户明细 是否有充值金额
        self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'账户明细')]").click()
        self.myWalletAccountDetail("1","账户余额充值",varRechargeDotTwoYuan)
        self.driver.find_element_by_id("com.mowin.tsz:id/back").click() # 点击 返回 到钱包 账户余额页面
    def myWalletAccountDetail(self,varState,varType,varCash):
        # self.myWalletAccountDetail("1","","")
        # self.myWalletAccountDetail("type","账户余额充值","")
        # self.myWalletAccountDetail("all","","")
        # self.myWalletAccountDetail("num","账户余额充值","100")
        # 账户明细页面检查明细记录, 三种情况 (只限1屏幕)
        # 1, varState=1 时,输出账户明细中第一条记录的明细类型\金额\时间 (第一个参数有效)
        # 2, varState=type 时,输出账户明细中所有符合varName的记录(第一二参数有效,最后一个参数无效)
        # 3, varState=all 时,输出账户明细中一屏所有记录(第一个参数有效,后2个参数无效)
        sleep(5)
        d_list=[]
        e_list=[]
        f_list=[]
        s_list=[]
        h_list=[]
        sh_list=[]
        # 账户明细 - 遍历明细金额
        varAccountDetailsCash =self.driver.find_elements_by_id("com.mowin.tsz:id/money")
        dcount=0
        for var_AccountDetailsCash in varAccountDetailsCash:
            d_list.append(var_AccountDetailsCash.text)
            dcount=dcount+1

        # 账户明细 - 明细类型
        appAccountDetailsType = self.driver.find_elements_by_id("com.mowin.tsz:id/item_accountdetail_hint")
        ecount=0
        tmpcount=0
        tmpcount1=0
        egcount=0
        for app_AccountDetailsType in appAccountDetailsType:
            e_list.append(app_AccountDetailsType.text)
            tmpcount=tmpcount+1
            if varType==app_AccountDetailsType.text:
                 ecount=ecount+1
                 h_list.append(tmpcount-1)

        if varType=="本人提现":
            appAccountDetailsStatus = self.driver.find_elements_by_id("com.mowin.tsz:id/item_accountdetail_status")
            for app_AccountDetailsStatus in appAccountDetailsStatus:
                tmpcount1=tmpcount1+1
                s_list.append(app_AccountDetailsStatus.text)
                egcount=egcount+1
                sh_list.append(tmpcount1-1)

        # 账户明细 - 明细时间
        varAccountDetailsTime = self.driver.find_elements_by_id("com.mowin.tsz:id/item_account_detail_time")
        for var_AccountDetailsTime in varAccountDetailsTime:
            f_list.append(var_AccountDetailsTime.text)

        if varState=="1":
            print "OK,账户明细第一条记录是 [" + str(e_list[0]) +"," + str(d_list[0]) + "," + str(f_list[0]) + "]"
        elif varState=="all":
            print "OK,账户明细一屏显示记录是 ["
            for i in range(dcount):
                print str(e_list[i]) + "," + str(d_list[i]) + "," + str(f_list[i])
            print "]"
        elif varState=="num":
            for i in range(dcount):
                if e_list[i] == varType and d_list[i] == varCash:print "OK,此记录 ["  + str(e_list[i]) + "," + str(d_list[i]) + "," + str(f_list[i]) + "]存在"
                else: print "Error, 此记录 ["+ str(e_list[i]) + "," + str(d_list[i]) + "," + str(f_list[i]) + "]不存在!"
        elif varState=="type" and egcount>0:
            for i in range(egcount):
                print "OK,账户明细,本人提现记录是 [" + str(e_list[h_list[i]]) +"," + str(d_list[h_list[i]]) + "," + str(f_list[h_list[i]]) + "," + str(s_list[sh_list[i]]) + "]"
        elif varState=="type" and ecount>0:
            for i in range(ecount):
                print "OK,账户明细," + str(varType) + "记录是 ["  + str(e_list[h_list[i]]) +"," + str(d_list[h_list[i]]) + "," + str(f_list[h_list[i]]) + "]"
        else:
            print "Warning,账户明细中不存在<" + str(varType) +">记录!"


    def web_chongzhi(self):
           # 打开sit2,进行充值操作
           self.browser.get("http://sit2.88uka.com/admin/finance/userExperienceList.do")
           self.browser.find_element_by_id("phoneValue").send_keys("13816101118")
           self.browser.find_elements_by_class_name("savebtn").click()

           allhandles=self.browser.window_handles
           for handle in allhandles:
               if handle != self.nowhandle:
                   self.browser.switch_to_window(handle)
           sleep(3)
           self.browser.maximize_window()
           # 商品标题
           self.browser.find_element_by_id("itemTitle").send_keys(GoodsName)
           # 商品副标题
           self.browser.find_element_by_id("phoneValue").send_keys("13816101118")
           # 参考价格
           self.browser.find_element_by_id("refPrice").send_keys(u"12.44")
           self.browser.find_element_by_id("goods_c_a").click()
           xx=self.browser.find_elements_by_class_name("select_cat")
           for x1 in xx:
               if x1.text==u"好货优先":
                   x1.click()
           # 保存
           self.browser.find_element_by_id("categorSelect").click()


    # 安装卸载
    def drv_install(self):
        self.TestcaseModule()

    def uninstallAPK(self, appPackage):
        sleep(6)
        if self.driver.is_app_installed(appPackage) == True:
           os.system('adb uninstall ' + appPackage + "> null")
           print "[OK,已卸载" + str(appPackage) + "包]"
        else:
           print "[Warning,无" + str(appPackage) + "包]"
    def installAPK(self,ApkName,appPackage,appActivity):
        sleep(6)
        print "[文件 " + str(ApkName) + " 安装中...]"
        os.system('adb install ' + ApkName + "> null")
        sleep(3)
        self.driver.start_activity(appPackage,appActivity)
        print "[OK," + str(appPackage) + " 安装成功]"
        # if os.path.isfile(ApkName): os.remove(ApkName)



    ##########################################################################################


if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(tsz) # 构造测试集
    unittest.TextTestRunner(verbosity=2).run(suite1) # 执行测试

