# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description: android自动化测试框架
#****************************************************************

import os, sys, unittest, xlwt, xlrd, MySQLdb, tempfile,shutil,chardet,random,webbrowser,platform,string,datetime,redis,commands,urllib2
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
from pymongo import MongoClient
from CJLinterfaceDriver import *

# print sys.path
# from resource.source.comparePic import *
# from resource.source import test2

#****************************************************************

# 参数化
varExcel = "/Users/linghuchong/Downloads/51/Project/CJL/excel/CJL1_0.xls"
varReport = "/Users/linghuchong/Downloads/51/Project/CJL/report/CJLreport1_0.html"
varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 获取当天日期时间,如20161020130318
varTableDetails = "/Users/linghuchong/Downloads/51/Project/CJL/report/CJLtable" + varTimeYMDHSM + ".html"
connMongo155 = MongoClient('192.168.2.155', 10005); db = connMongo155.sceneWeb  # mongodb
connRedis166 = redis.StrictRedis(host='192.168.2.166', port=6379, db=0, password="dlhy123456")  # redis CJL66
connRedis167 = redis.StrictRedis(host='192.168.2.167', port=6380, db=0, password="dlhy123456")  # redis CJL67
connPersonal = MySQLdb.connect(host='192.168.2.164', user='remote', passwd='Dlhy66506043', db='personal', port=3306, use_unicode=True)
curPersonal = connPersonal.cursor();curPersonal.execute('SET NAMES utf8;');connPersonal.set_character_set('utf8');curPersonal.execute('show tables')
connScenemsg = MySQLdb.connect(host='192.168.2.164', user='remote', passwd='Dlhy66506043', db='scenemsg', port=3306, use_unicode=True)
curScenemsg = connScenemsg.cursor();curScenemsg.execute('SET NAMES utf8;');connScenemsg.set_character_set('utf8');curScenemsg.execute('show tables')
connSysparam = MySQLdb.connect(host='192.168.2.164', user='remote', passwd='Dlhy66506043', db='sysparam', port=3306, use_unicode=True)
curSysparam = connSysparam.cursor();curSysparam.execute('SET NAMES utf8;');connSysparam.set_character_set('utf8');curSysparam.execute('show tables')
connUpload = MySQLdb.connect(host='192.168.2.164', user='remote', passwd='Dlhy66506043', db='upload', port=3306, use_unicode=True)
curUpload = connUpload.cursor();curUpload.execute('SET NAMES utf8;');connUpload.set_character_set('utf8');curUpload.execute('show tables')
bk = xlrd.open_workbook(varExcel, formatting_info=True)
newbk = copy(bk)
sheetMain = bk.sheet_by_name("main")
sheetTestCase = bk.sheet_by_name("testcase")
sheetArea = bk.sheet_by_name("area")
sheetCom = bk.sheet_by_name("com")
sheetSplit = bk.sheet_by_name("split")
styleRed = xlwt.easyxf('font: name Times New Roman, color-index red')
styleBlue = xlwt.easyxf('font: name Times New Roman, color-index blue')
styleGray25 = xlwt.easyxf('font: name Times New Roman, color-index gray25')

# 获取手机制造商信息,如 adb shell getprop | grep "model\|version.sdk\|manufacturer\|hardware\|platform\|revision\|serialno\|product.name\|brand"
androidVersion = commands.getoutput('adb shell getprop ro.build.version.release')
androidSerialno = commands.getoutput('adb shell getprop ro.serialno')

# def exl(exlSheet,col):
#     # 获取sheetArea某列的行数 (表格列从1算起)
#     vatCount = 0
#     varContent = [eval(exlSheet).cell(i, col-1).value for i in range(eval(exlSheet).nrows)]
#     for i in range(len(varContent)):
#         if varContent[i]!="":vatCount = vatCount + 1
#         else:break
#     print vatCount
#
# exl("sheetArea",1)
# sleep(1212)

class cjl(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = str(float(androidVersion[0:3]))
        desired_caps['deviceName'] = androidSerialno
        desired_caps['appPackage'] = sheetMain.cell_value(1, 5)
        desired_caps['appActivity'] = sheetMain.cell_value(3, 5)
        desired_caps['unicodeKeyboard'] = 'True'
        desired_caps['resetKeyboard'] = 'True'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        reload(sys)
        sys.setdefaultencoding('utf8')

        # 手机分辨率的宽,高
        self.screenX = self.driver.get_window_size()['width']
        self.screenY = self.driver.get_window_size()['height']
        print ">" * 150
        print "当前测试机信息如下:"
        # (x, productmodel) = commands.getstatusoutput('adb shell getprop ro.product.model')
        productmodel = commands.getoutput('adb shell getprop ro.product.model')
        print "品牌名: " + productmodel
        self.productmodel = productmodel.strip()
        productdevice = commands.getoutput('adb shell getprop ro.product.device')
        print "设备名: " + productdevice
        print "版本号: " + androidVersion
        sdk = commands.getoutput('adb shell getprop ro.build.version.sdk')
        print "S D K: " + sdk
        print "分辨率: " + str(self.screenX) + " * " + str(self.screenY)
        abi = commands.getoutput('adb shell getprop ro.product.cpu.abi')
        print "C P U: " + abi
        serialno = commands.getoutput('adb shell getprop ro.serialno')
        print "SerialNo: " + serialno

        # # 自动生成一个新的手机号，方法是从数据库中获取最小的手机号,并减1
        # self.curWeb.execute('select min(username) from t_user')
        # tb = self.curWeb.fetchone()
        # varNewphone = int(tb[0]) - 1

        # # 获取excel中的oldphone手机号 ，手机号可以由多个组成，用／分割，如13816109050/13636371320
        # try:
        #     l_phone = []
        #     if "/" in str(sheetMain.cell_value(1, 7)):
        #         x = sheetMain.cell_value(1, 7).split("/")
        #         print "初始化" + str(sheetMain.cell_value(1,7).count("/")+1) + "个旧手机号"
        #         for i in range(0, sheetMain.cell_value(1, 7).count("/")+1):
        #             l_phone.append(x[i])
        #             print l_phone[i]
        #     else:
        #         l_phone.append(sheetMain.cell_value(1, 7))
        #         varNickName1 = str(l_phone[0][0:3]) + "****" + str(l_phone[0][7:])
        # except:
        #      print str('Error,excel中OldPhone字段不能为空!')

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def test_Main(self):
        for i in range(1, sheetMain.nrows):
            if sheetMain.cell_value(i, 0) == "Y":
                self.Maincol1 = sheetMain.cell_value(i, 1)
                self.Maincol2 = sheetMain.cell_value(i, 2)
                exec(sheetMain.cell_value(i, 4))

    def TestcaseModule(self):
         # 遍历TestCase及调用函数模块,定位测试用例位置及数量
         sleep(5)
         self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/nextView").click()  # 场景进入
         sleep(5)
         case1 = caseN = 0
         for j in range(1, sheetTestCase.nrows):
              case1 = case1 + 1
              if sheetTestCase.cell_value(j, 2) == self.Maincol1:
                  for k in range(case1+1, 100):  # 假设有100个Case
                      if k + 1 > sheetTestCase.nrows:  # 最后一行
                           caseN = caseN + 1
                           break
                      elif sheetTestCase.cell_value(k, 1) == "" and sheetTestCase.cell_value(k, 2) == "":
                           caseN = caseN + 1
                      elif sheetTestCase.cell_value(k, 1) == "skip":
                           caseN = caseN + 1
                      else:
                           caseN = caseN + 1
                           break
                  break
         if self.Maincol2 == "skip":
             case1 = case1 + 1
             caseN = caseN - 1

         #遍历 Testcase1~TestCaseN
         for l in range(case1, caseN+case1):
              str_list = []
              for m in range(7, 30):  # id0 - id22 ,定位参数从第6列开始，遍历23列
                  if sheetTestCase.cell(l, m).value != "":
                      N = sheetTestCase.cell_value(l, m)
                      N = sheetMain.cell_value(1, 5) + ":" + N
                      str_list.append(str(N))
                  else:
                      break
              self.str_list = str_list
              try :
                  if sheetTestCase.cell_value(l, 1) == "skip":
                      newWs = newbk.get_sheet(1)
                      newWs.write(l, 0, "skip", styleGray25)
                      newbk.save(varExcel)
                  elif sheetTestCase.cell_value(l, 5) == "":
                      pass
                  else:
                      self.l = l
                      exec(sheetTestCase.cell_value(l, 5))
                      newWs=newbk.get_sheet(1)
                      newWs.write(l, 0, "OK", styleBlue)
                      newbk.save(varExcel)
              except:
                  print "Errorrrrrrr , Excel("+str(l+1)+") , " + sheetTestCase.cell_value(case1, 2) + " , " + sheetTestCase.cell_value(l, 3) + " , " +sheetTestCase.cell_value(l, 4) + " , " +sheetTestCase.cell_value(l, 5)
                  newWs = newbk.get_sheet(1)
                  newWs.write(l, 0, "error", styleRed)
                  newbk.save(varExcel)

         # # 是否生成ReportHTML文档, 1=生成一个testreport.html; 2=生成多个带时间的html,如testreport20161205121210.html;
         # if self.sheetMain.cell_value(1, 9) == 1:
         #     page.printOut(varReport)
         #     sleep(4)
         #     # send Email
         #     if self.sheetMain.cell_value(1, 8) == "Y":self.sendemail(varReport)
         # elif self.sheetMain.cell_value(1,9) == 2:
         #     page.printOut(varTableDetails)
         #     # send Email
         #     if self.sheetMain.cell_value(1,8) == "Y":
         #        self.sendemail(varTableDetails)

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
    def assertEqual(self,expected, actual,okmessage,errmessage):
        if expected == actual :print okmessage
        else:print errmessage
    def assertSplit(self, varExcel):
        # 拆分两个值，如 id/cance=取消
        x = varExcel.split("=")
        return (x[0], x[1])
    def getElementExist(self, _id):
        # 获取元素是否存在
        ElementStatus = False
        try:
            self.driver.find_element_by_id(_id)
            ElementStatus = True
        except :
            ElementStatus = False
        return ElementStatus
    def screenWidthHeight(self, rightCornerPicID):
        # self.screenWidthHeight("com.mowin.tsz:id/my_tab")
        # 获取屏幕右下角图片的长度和高度, 一般是屏幕的长度和高度(1440,2392)
        location = self.driver.find_element_by_id(rightCornerPicID).location
        size = self.driver.find_element_by_id(rightCornerPicID).size
        varWidth = int(location["x"] + size["width"])
        varHeight = int(location["y"] + size["height"])
        return int(location["x"]),varWidth, int(location["y"]), varHeight
    def exlColnums(self,exlSheet,col):
        # 获取sheetArea某列的行数 (表格列从1算起)
        # 遍历分类
        vatCount = 0
        varContent = [eval(exlSheet).cell(i, col-1).value for i in range(eval(exlSheet).nrows)]
        for i in range(len(varContent)):
            if varContent[i]!="":vatCount = vatCount + 1
            else:break
        return vatCount

    def camera(self,choose1):
        # self.camera("拍照")
        # 点击某一头像或照片，下拉框显示 拍照、从手机相册选择、取消
        # 拍照
        el1 = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[contains(@index,0)]")
        self.assertEqual(el1.text, "拍照", "OK, " + el1.text, "errorrrrrr, " + el1.text)
        # 从手机相册选择
        el2 = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[contains(@index,2)]")
        self.assertEqual(el2.text, "从手机相册选择", "OK, " + el2.text, "errorrrrrr, " + el2.text)
        sleep(2)
        # 取消
        cancel = self.driver.find_element_by_id(sheetMain.cell_value(1,5) + ":id/cancel").text
        self.assertEqual(cancel, "取消", "OK, 取消", "errorrrrrr, 取消")
        sleep(2)
        if choose1 == "拍照":
            el1.click()
        elif choose1 == "从手机相册选择":
            el2.click()
        else:
            self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/cancel").click()
        sleep(2)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>华丽分割线>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # 安装卸载
    def drv_package(self):
        self.TestcaseModule()
        sleep(2)
    def uninstallAPK(self, appPackage):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        if self.driver.is_app_installed(appPackage) == True:
           os.system('adb uninstall ' + appPackage + "> null")
           print "[OK, " + str(appPackage) + " 卸载成功]"
        else:
           print "[Warning, 无" + str(appPackage) + "包]"
        sleep(2)
    def installAPK(self,ApkName,appPackage,appActivity):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        print "[Doing, " + str(ApkName) + "]"
        os.system('adb install ' + ApkName + "> null")
        sleep(3)
        self.driver.start_activity(appPackage,appActivity)
        print "[OK, " + str(appPackage) + " 安装成功]"
        # if os.path.isfile(ApkName): os.remove(ApkName)



    # 登录
    def drv_login(self):
        self.TestcaseModule()
    def jumpLogin(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        # 跳转到登录页
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()
        sleep(4)

        # 假设没有二维码，则可能是没有登录。
        if self.getElementExist(self.str_list[1]) == True:
            # 点击设置，进行退出操作
            self.driver.find_element_by_id(self.str_list[0]).click()
            self.driver.find_element_by_id(self.str_list[2]).click()
            self.driver.find_element_by_id(self.str_list[3]).click()
            sleep(2)
            self.driver.find_element_by_id(self.str_list[4]).click()
        sleep(2)
        el = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.ScrollView/android.widget.RelativeLayout/child::android.widget.RelativeLayout/child::android.widget.RelativeLayout[1]/android.widget.TextView[contains(@text,'点击登录')]")
        el.click()
        sleep(3)
    def loginElement(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        # 无密码快捷登录,页面元素检查
    def loginPhone(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.driver.find_element_by_id(self.str_list[0]).send_keys(int(sheetMain.cell_value(1, 7)))  # testPhone 手机号码
        self.driver.find_element_by_id(self.str_list[1]).click()  # 获取验证码
        sleep(5)
        self.driver.find_element_by_id(self.str_list[2]).send_keys(getCJLverifyCode(int(sheetMain.cell_value(1, 7))))  # 输入验证码
        self.driver.find_element_by_id(self.str_list[3]).click()  # 手机号登录
    def loginWeixin(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.driver.find_element_by_id(self.str_list[0]).click()  # 点击微信
    def loginQQ(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.driver.find_element_by_id(self.str_list[0]).click()  # 点击QQ
    def loginWeibo(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.driver.find_element_by_id(self.str_list[0]).click()  # 点击微博
    def loginInfoElement(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        # 完善个人资料，页面元素
        sleep(3)
        # 返回键
        self.assertEqual(self.driver.find_element_by_id(self.str_list[0]).is_displayed(), True, "OK, 返回键", "errorrrrrr, 返回键")

        # 点击 拍照机，检查文案"拍照、从手机相册选择、取消"
        self.driver.find_element_by_id(self.str_list[1]).click()  # 上传头像
        sleep(6)
        self.camera("取消")
        # # 拍照
        # el1 = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[contains(@index,0)]")
        # self.assertEqual(el1.text, sheetTestCase.cell_value(self.l, 9), "OK, " + el1.text, "errorrrrrr, " + el1.text)
        # # 从手机相册选择
        # el2 = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[contains(@index,2)]")
        # self.assertEqual(el2.text, sheetTestCase.cell_value(self.l, 10), "OK, " + el2.text, "errorrrrrr, " + el2.text)
        # sleep(2)
        # # 取消
        # (a, b) = self.assertSplit(self.str_list[4])
        # self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, "+b, "errorrrrrr, "+b)
        # self.driver.find_element_by_id(a).click()
        # sleep(2)

        for i in range(5, 11):
            # 5=完善个人资料 , 6=上传头像 , 7=昵称 , 8=输入昵称 , 9=我是帅哥 ,10=我是美女 ，
            (a, b) = self.assertSplit(self.str_list[i])
            self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)

        # 注：....
        el3 = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/child::android.widget.FrameLayout[1]/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.TextView[contains(@index,8)]")
        self.assertEqual(el3.text, sheetTestCase.cell_value(self.l, 18), "OK, " + el3.text, "errorrrrrr, " + el3.text)
        sleep(2)
    def loginInfo(self):
        # 完善个人资料
        # 如果上传头像存在则完善，否则可能是老用户登录将不会显示完善个人资料页面
        if self.getElementExist(self.str_list[0]) == True:
            print ">" * 150
            print sheetTestCase.cell_value(self.l, 4)
            self.driver.find_element_by_id(self.str_list[0]).click()  # 上传头像
            sleep(3)
            # 从手机相册选择
            el2 = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[contains(@index,2)]")
            el2.click()
            sleep(4)
            # 品牌名: ATH-AL00
            varimages = self.driver.find_elements_by_id(self.str_list[4])
            x=0
            for varimage in varimages:
                if x == 10:
                    varimage.click()
                    break
                x = x + 1
            sleep(3)

            # 调用第三方手机特有ID
            for i in range(1, 3):
                if self.productmodel == sheetMain.cell_value(i, 9).encode("utf-8"):
                    self.driver.find_element_by_id(sheetMain.cell_value(i, 10)).click()
                    break

            sleep(6)
            # 侦探+手机号尾4位 varnickname
            varnickname = sheetMain.cell_value(1, 6) + str(int(sheetMain.cell_value(1, 7)))[-4:]
            self.driver.find_element_by_id(self.str_list[1]).send_keys(varnickname)  # 输入昵称
            sleep(2)
            self.driver.find_element_by_id(self.str_list[2]).click()  # 选择性别,男／女
            self.driver.find_element_by_id(self.str_list[3]).click()  # 完成
            sleep(3)



    # 我
    def drv_me(self):
        self.TestcaseModule()
    def meElement(self):
        print ">" * 150
        print "C3-1,我，页面元素（头像、昵称、性别、小鹿号、个人签名、二维码、通讯录、我建的场景、我的相册、我的足迹、分享、设置、扫一扫）"
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()
        sleep(4)
        # 我
        el3 = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/child::android.widget.RelativeLayout[1]/child::android.widget.FrameLayout[1]/android.widget.ScrollView/android.widget.RelativeLayout/child::android.widget.RelativeLayout[1]/android.widget.TextView[contains(@index,0)]")
        self.assertEqual(el3.text, sheetTestCase.cell_value(self.l, 20), "OK, " + el3.text, "errorrrrrr, " + el3.text)

        # 头像
        self.assertEqual(self.driver.find_element_by_id(self.str_list[0]).is_displayed(), True, "OK, 头像", "errorrrrrr, 头像")

        # 昵称
        self.assertEqual(self.driver.find_element_by_id(self.str_list[1]).text, sheetMain.cell_value(1, 6), "OK, 昵称", "errorrrrrr, 昵称 ," + sheetMain.cell_value(1, 6)+ "<>" + self.driver.find_element_by_id(self.str_list[1]).text)

        # 性别
        self.assertEqual(self.driver.find_element_by_id(self.str_list[2]).is_displayed(), True, "OK, 性别", "errorrrrrr, 性别")

        # 小鹿号，只检查文案+数字个数 (小鹿号：2016122710030)
        varDeernumber = self.driver.find_element_by_id(self.str_list[3]).text
        varDeernumber = varDeernumber.replace("：", ":")
        x = varDeernumber.split(":")
        if x[0] == "小鹿号" and len(x[1]) == 13:
            print "OK, " + varDeernumber
        else:
            print "errorrrrrr, " + varDeernumber
        self.meXiaoluhao = x[1]

        # 个人签名
        self.assertEqual(self.driver.find_element_by_id(self.str_list[4]).text, "个性签名：", "OK, 个性签名", "errorrrrrr, 个性签名错误 , 个性签名： <>" + self.driver.find_element_by_id(self.str_list[4]).text)

        # 二维码
        self.assertEqual(self.driver.find_element_by_id(self.str_list[5]).is_displayed(), True, "OK, 二维码", "errorrrrrr, 二维码")

        # 6=通讯录 , 7=我建的场景 , 8=我的相册 , 9=我的足迹 , 10=分享[场景鹿]给好友 ,11=设置 ，
        for i in range(6, 12):
            (a, b) = self.assertSplit(self.str_list[i])
            self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)

        # 扫一扫
        self.assertEqual(self.driver.find_element_by_id(self.str_list[12]).is_displayed(), True, "OK, 扫一扫", "errorrrrrr, 扫一扫")

    def meInfo(self):
        print ">" * 150
        print "C3-2，个人信息（头像、昵称、小鹿号、登录账号、性别、地区、个人签名）"
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()
        sleep(2)

        # 个人信息
        self.driver.find_element_by_id(self.str_list[0]).click()
        sleep(3)
        # 标题 = 个人信息
        (a, b) = self.assertSplit(self.str_list[1])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)

        # 头像
        (a, b) = self.assertSplit(self.str_list[2])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(self.str_list[3]).click()
        sleep(6)
        self.camera("取消")

        # 昵称 (修改昵称为 科比abc)
        (a, b) = self.assertSplit(self.str_list[4])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(self.str_list[5]).click()
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/title").text, "更改昵称", "OK, 更改昵称", "errorrrrrr, 更改昵称")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/content").clear()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/content").send_keys(u"科比abc")
        sleep(2)
        el3 =self.driver.find_element_by_id("com.mowin.scenesdeer:id/actionBar").find_element_by_xpath("//android.widget.TextView[contains(@index,2)]")
        self.assertEqual(el3.text, "保存", "OK, 保存" , "errorrrrrr, 保存")
        el3.click()
        sleep(2)
        self.assertEqual(self.driver.find_element_by_id(self.str_list[5]).text, "科比abc", "OK, 修改昵称后显示", "errorrrrrr, 修改昵称后显示")

        # 小鹿号
        (a, b) = self.assertSplit(self.str_list[6])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        infoXiaolvhao = self.driver.find_element_by_id(self.str_list[7]).text

        # 登录账号 及 小icon
        (a, b) = self.assertSplit(self.str_list[8])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.assertEqual(self.driver.find_element_by_id(self.str_list[9]).is_displayed(), True, "OK, 登录账号第三方头像", "errorrrrrr, 登录账号第三方头像")

        # 性别 (修改昵称为 女)
        (a, b) = self.assertSplit(self.str_list[10])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        (a, b) = self.assertSplit(self.str_list[11])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)

        # 地区 及值
        (a, b) = self.assertSplit(self.str_list[12])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(self.str_list[13]).click()
        sleep(2)
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/title").text, "选择地区", "OK, 标题选择地区第一层", "errorrrrrr, 标题选择地区第一层")
        districts = self.driver.find_elements_by_id("com.mowin.scenesdeer:id/district")
        for district in districts:
            if district.text == "上海市":
                district.click()
                sleep(2)
                self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/title").text, "选择地区", "OK, 标题选择地区第二层", "errorrrrrr, 标题选择地区第二层")
                districts2 = self.driver.find_elements_by_id("com.mowin.scenesdeer:id/district")
                for district2 in districts2:
                    if district2.text == "上海市市辖区":
                        district2.click()
                        break
                break
        sleep(3)
        self.assertEqual(self.driver.find_element_by_id(self.str_list[13]).text, u"上海市  上海市市辖区", "OK, 上海市  上海市市辖区", "errorrrrrr, 上海市  上海市市辖区")

        # 个人签名 (修改为 weibo)
        (a, b) = self.assertSplit(self.str_list[14])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(self.str_list[15]).click()
        sleep(2)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/title").text, "更改个人签名", "OK, 更改个人签名", "errorrrrrr, 更改个人签名")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/content").clear()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/content").send_keys(u"weibo")
        sleep(2)
        el3 = self.driver.find_element_by_id("com.mowin.scenesdeer:id/actionBar").find_element_by_xpath("//android.widget.TextView[contains(@index,2)]")
        self.assertEqual(el3.text, "保存", "OK, 保存" , "errorrrrrr, 保存")
        el3.click()
        sleep(3)
        self.assertEqual(self.driver.find_element_by_id(self.str_list[15]).text, "weibo", "OK, 修改个人签名后显示", "errorrrrrr, 修改个人签名后显示")

        # 返回
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()

        # 验证小鹿号
        self.assertEqual(infoXiaolvhao, self.meXiaoluhao, "OK, 小鹿号码内外比较", "errorrrrrr, 小鹿号码内外比较")

    def meAddresslist(self):
        print ">" * 150
        print "C3-3,我 - 通讯录（搜索、新的朋友、分组标签）"
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()
        sleep(2)
        # 我 - 小鹿号，(小鹿号：2016122710030)
        varDeernumber = self.driver.find_element_by_id("com.mowin.scenesdeer:id/small_deer_number").text
        varDeernumber = "我的" + varDeernumber.replace("：", ":")

        self.driver.find_element_by_id(self.str_list[0]).click()
        sleep(2)
        self.assertEqual(self.driver.find_element_by_id(self.str_list[1]).is_displayed(), True, "OK, 搜索框", "errorrrrrr, 搜索框")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/search").text, "搜索", "OK, 搜索文字", "errorrrrrr, 搜索文字")
        # 新的朋友
        (a, b) = self.assertSplit(self.str_list[2])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).click()
        sleep(2)
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/title").text, "新的朋友", "OK, 标题=新的朋友", "errorrrrrr, 标题=新的朋友" )

        # 新的朋友 - 详情页中扫一扫
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/actionBar").find_element_by_xpath("//android.widget.ImageView[contains(@index,2)]").is_displayed(), True, "OK, 扫一扫", "errorrrrrr, 扫一扫")
        # 新的朋友 - 详情页各元素
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/status_bar").is_displayed(), True, "OK, 搜索框", "errorrrrrr, 搜索框")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/search").text, "搜索小鹿号", "OK, 搜索小鹿号文字", "errorrrrrr, 搜索小鹿号文字")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/my_small_deer_number").text, varDeernumber, "OK, " + varDeernumber, "errorrrrrr, " + varDeernumber)
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/qr_code").is_displayed(), True, "OK, 二维码", "errorrrrrr, 二维码")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/add_phone_contacts").text, "添加手机联系人", "OK, 添加手机联系人", "errorrrrrr, 添加手机联系人")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/add_weixin_friend").text, "添加微信好友", "OK, 添加微信好友", "errorrrrrr, 添加微信好友")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/add_qq_friend").text, "添加QQ好友", "OK, 添加QQ好友", "errorrrrrr, 添加QQ好友")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/no_data_icon").is_displayed(), True, "OK, 背景鹿头", "errorrrrrr, 背景鹿头")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/no_data_hint").text, "没有新的好友邀请信息", "OK, 没有新的好友邀请信息", "errorrrrrr, 没有新的好友邀请信息")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()

        # 分组标签
        (a, b) = self.assertSplit(self.str_list[3])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).click()
        sleep(2)
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/title").text, "分组标签", "OK, 标题=分组标签", "errorrrrrr, 标题=分组标签" )
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/add_label").find_element_by_xpath("//android.widget.ImageButton[contains(@index,0)]").is_displayed(), True, "OK, 分组标签+", "errorrrrrr, 分组标签+")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/add_label").find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, "新建标签", "OK, 新建标签", "errorrrrrr, 新建标签")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()

        # 字母列表
        self.assertEqual(self.driver.find_element_by_id(self.str_list[4]).is_displayed(), True, "OK, 字母列表", "errorrrrrr, 字母列表")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()

        print ">" * 150
        print "C3-3,我 - 通讯录（搜索、新的朋友、分组标签）"
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()
        sleep(2)

    def meMyscene(self):
        print ">" * 150
        print "C3-4,我 - 我建的场景"
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()
        sleep(2)
        self.driver.find_element_by_id(self.str_list[0]).click()
        sleep(2)
        (a, b) = self.assertSplit(self.str_list[1])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.assertEqual(self.driver.find_element_by_id(self.str_list[2]).is_displayed(), True, "OK, 背景鹿头", "errorrrrrr, 背景鹿头")
        (a, b) = self.assertSplit(self.str_list[3])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()
        sleep(2)

    def meMyalbum(self):
        print ">" * 150
        print "C3-5,我 - 我的相册"
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()
        sleep(2)
        self.driver.find_element_by_id(self.str_list[0]).click()
        sleep(2)
        (a, b) = self.assertSplit(self.str_list[1])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.assertEqual(self.driver.find_element_by_id(self.str_list[2]).is_displayed(), True, "OK, 背景鹿头", "errorrrrrr, 背景鹿头")
        (a, b) = self.assertSplit(self.str_list[3])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()
        sleep(2)

    def meMyfoot(self):
        print ">" * 150
        print "C3-6,我 - 我的足迹"
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()
        sleep(2)
        self.driver.find_element_by_id(self.str_list[0]).click()
        sleep(2)
        (a, b) = self.assertSplit(self.str_list[1])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.assertEqual(self.driver.find_element_by_id(self.str_list[2]).is_displayed(), True, "OK, 背景鹿头", "errorrrrrr, 背景鹿头")
        (a, b) = self.assertSplit(self.str_list[3])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()
        sleep(2)

    def meShare(self):
        print ">" * 150
        print "C3-7,我 - 分享[场景鹿]给好友(朋友圈、微信好友、QQ、QQ空间、新浪微博)"
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()
        sleep(2)
        self.driver.find_element_by_id(self.str_list[0]).click()
        sleep(2)
        (a, b) = self.assertSplit(self.str_list[2])
        self.assertEqual(self.driver.find_element_by_id(self.str_list[1]).is_displayed(), True, "OK, " + b + "icon", "errorrrrrr, " + b + "icon")
        self.assertEqual(self.driver.find_element_by_id(a).find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, b, "OK, " + b, "errorrrrrr, " + b)
        (a, b) = self.assertSplit(self.str_list[4])
        self.assertEqual(self.driver.find_element_by_id(self.str_list[3]).is_displayed(), True, "OK, " + b + "icon", "errorrrrrr, " + b + "icon")
        self.assertEqual(self.driver.find_element_by_id(a).find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, b, "OK, " + b, "errorrrrrr, " + b)
        (a, b) = self.assertSplit(self.str_list[6])
        self.assertEqual(self.driver.find_element_by_id(self.str_list[5]).is_displayed(), True, "OK, " + b + "icon", "errorrrrrr, " + b + "icon")
        self.assertEqual(self.driver.find_element_by_id(a).find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, b, "OK, " + b, "errorrrrrr, " + b)
        (a, b) = self.assertSplit(self.str_list[8])
        self.assertEqual(self.driver.find_element_by_id(self.str_list[7]).is_displayed(), True, "OK, " + b + "icon", "errorrrrrr, " + b + "icon")
        self.assertEqual(self.driver.find_element_by_id(a).find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, b, "OK, " + b, "errorrrrrr, " + b)
        (a, b) = self.assertSplit(self.str_list[10])
        self.assertEqual(self.driver.find_element_by_id(self.str_list[9]).is_displayed(), True, "OK, " + b + "icon", "errorrrrrr, " + b + "icon")
        self.assertEqual(self.driver.find_element_by_id(a).find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(self.str_list[11]).click()
        sleep(2)

    def meSetup(self):
        print ">" * 150
        print "C3-7,我 - 设置"
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()
        sleep(2)
        self.driver.find_element_by_id(self.str_list[0]).click()
        sleep(2)
        # 设置 标题
        (a, b) = self.assertSplit(self.str_list[1])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        # 新消息通知
        (a, b) = self.assertSplit(self.str_list[2])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).click()
        # 遍历 新消息通知
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/title").text, "新消息通知", "OK, 新消息通知", "errorrrrrr, 新消息通知")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/contentParentLayout").find_element_by_xpath("//android.widget.LinearLayout/child::android.widget.RelativeLayout[1]/android.widget.TextView[contains(@index,0)]").text, "接收新消息通知", "OK, 接收新消息通知", "errorrrrrr, 接收新消息通知")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/receive_new_message_alerts").get_attribute("checked"), "true", "OK, 接收新消息通知(打开)", "errorrrrrr, 接收新消息通知(打开)")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/contentParentLayout").find_element_by_xpath("//android.widget.LinearLayout/child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,0)]").text, "通知显示消息详情", "OK, 通知显示消息详情", "errorrrrrr, 通知显示消息详情")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/notice_shows_the_details").get_attribute("checked"), "true", "OK, 通知显示消息详情(打开)", "errorrrrrr, 通知显示消息详情(打开)")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/contentParentLayout").find_element_by_xpath("//android.widget.LinearLayout/android.widget.TextView[contains(@index,3)]").text, "若关闭，当收到聊天新消息时，将不再显示发送人和消息内容", "OK, 若关闭，当收到聊天新消息时，将不再显示发送人和消息内容", "errorrrrrr, 若关闭，当收到聊天新消息时，将不再显示发送人和消息内容")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/contentParentLayout").find_element_by_xpath("//android.widget.LinearLayout/child::android.widget.RelativeLayout[3]/android.widget.TextView[contains(@index,0)]").text, "声音", "OK, 声音", "errorrrrrr, 声音")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/sound").get_attribute("checked"), "true", "OK, 声音(打开)", "errorrrrrr, 声音(打开)")
        # 开关打开功能。
        # self.driver.find_element_by_id("com.mowin.scenesdeer:id/sound").click()
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/contentParentLayout").find_element_by_xpath("//android.widget.LinearLayout/child::android.widget.RelativeLayout[4]/android.widget.TextView[contains(@index,0)]").text, "振动", "OK, 振动", "errorrrrrr, 振动")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/vibrate").get_attribute("checked"), "true", "OK, 振动(打开)", "errorrrrrr, 振动(打开)")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()

        # 勿扰模式
        (a, b) = self.assertSplit(self.str_list[3])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).click()
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/title").text, "勿扰模式", "OK, 勿扰模式", "errorrrrrr, 勿扰模式")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/contentParentLayout").find_element_by_xpath("//android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.TextView[contains(@index,0)]").text, "勿扰模式", "OK, 勿扰模式", "errorrrrrr, 勿扰模式")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/no_disturb_pattern").get_attribute("checked"), "false", "OK, 勿扰模式(关闭)", "errorrrrrr, 勿扰模式(关闭)")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/contentParentLayout").find_element_by_xpath("//android.widget.LinearLayout/android.widget.TextView[contains(@index,1)]").text, "开启后在设定时间段内收到新消息时不会响铃或振动", "OK, 开启后在设定时间段内收到新消息时不会响铃或振动", "errorrrrrr, 开启后在设定时间段内收到新消息时不会响铃或振动")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()


        # 隐私
        (a, b) = self.assertSplit(self.str_list[4])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).click()
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/title").text, "隐私", "OK, 隐私", "errorrrrrr, 隐私")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/contentParentLayout").find_element_by_xpath("//android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.TextView[contains(@index,0)]").text, "加我为好友时需要验证", "OK, 加我为好友时需要验证", "errorrrrrr, 加我为好友时需要验证")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/verify").get_attribute("checked"), "true", "OK, 加我为好友时需要验证(打开)", "errorrrrrr, 加我为好友时需要验证(打开)")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/black_list").text, "黑名单", "OK, 黑名单", "errorrrrrr, 黑名单")
        # 黑名单
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/black_list").click()
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/title").text, "黑名单", "OK, 黑名单", "errorrrrrr, 黑名单")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/no_black_list_bg").is_displayed(), True, "OK, 背景长颈鹿", "errorrrrrr, 背景长颈鹿")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/black_list_is_empty").text, "黑名单为空", "OK, 黑名单为空", "errorrrrrr, 黑名单为空")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/no_black_list_layout").find_element_by_xpath("//android.widget.TextView[contains(@index,2)]").text, "加入黑名单后，你将不再接收对方任何消息", "OK, 加入黑名单后，你将不再接收对方任何消息", "errorrrrrr, 加入黑名单后，你将不再接收对方任何消息")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()



        # 关于场景鹿
        (a, b) = self.assertSplit(self.str_list[5])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        # 场景鹿1.0
        (a, b) = self.assertSplit(self.str_list[6])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).click()
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/title").text, "关于场景鹿", "OK, 关于场景鹿", "errorrrrrr, 关于场景鹿")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/app_thumb").is_displayed(), True, "OK, 长颈鹿头像", "errorrrrrr, 长颈鹿头像")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/version").text, "场景鹿1.0", "OK, 场景鹿1.0", "errorrrrrr, 场景鹿1.0")
        # 功能介绍
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/function_introduction").text, "功能介绍", "OK, 功能介绍", "errorrrrrr, 功能介绍")
        # ? 无法点击

        # 意见反馈
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/suggestion_feedback").text, "意见反馈", "OK, 意见反馈", "errorrrrrr, 意见反馈")
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/suggestion_feedback").click()
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/title").text, "意见反馈", "OK, 意见反馈", "errorrrrrr, 意见反馈")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/contentParentLayout").find_element_by_xpath("//android.widget.LinearLayout/android.widget.TextView[contains(@index,0)]").text, "感谢你提出的宝贵意见和建议，你留下的每个字都将用来改善我们的产品。", "OK, 感谢你提出的宝贵意见和建议，你留下的每个字都将用来改善我们的产品。", "errorrrrrr, 感谢你提出的宝贵意见和建议，你留下的每个字都将用来改善我们的产品。")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/content").text, "用的不爽，说两句哦…", "OK, 用的不爽，说两句哦…", "errorrrrrr, 用的不爽，说两句哦…")
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/content").send_keys(u"非常好用，分享朋友圈")
        # 提交
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/actionBar").find_element_by_xpath("//android.widget.TextView[contains(@index,2)]").click()
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/suggestion_feedback").click()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()


        # 服务协议
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/service_agreement").text, "服务协议", "OK, 服务协议", "errorrrrrr, 服务协议")
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/service_agreement").click()
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/title").text, "用户协议", "OK, 用户协议", "errorrrrrr, 用户协议")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()


        # 隐私政策
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/privacy_policy").text, "隐私政策", "OK, 隐私政策", "errorrrrrr, 隐私政策")
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/privacy_policy").click()
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/title").text, "隐私政策", "OK, 隐私政策", "errorrrrrr, 隐私政策")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()
        # 检查新版本 ？ 无法点击
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/check_the_new_version").text, "检查新版本", "OK, 检查新版本", "errorrrrrr, 检查新版本")
        # self.driver.find_element_by_id("com.mowin.scenesdeer:id/check_the_new_version").click()

        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()


        # 清除缓存
        (a, b) = self.assertSplit(self.str_list[7])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).click()
        sleep(2)
        # 检查场景鹿弹框
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/title").text, "场景鹿", "OK, 场景鹿", "errorrrrrr, 场景鹿")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/content").text, "是否要清除缓存？", "OK, 是否要清除缓存？", "errorrrrrr, 是否要清除缓存？")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/negative").text, "取消", "OK, 取消", "errorrrrrr, 取消")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/positive").text, "清除", "OK, 清除", "errorrrrrr, 清除")
        # 点击取消
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/negative").click()


        # 切换帐号或退出登录 （未做第三方检查）
        (a, b) = self.assertSplit(self.str_list[8])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).click()
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/title").text, "切换帐号/退出登录", "OK, 切换帐号/退出登录", "errorrrrrr, 切换帐号/退出登录")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/switch_account").text, "切换登录账号", "OK, 切换登录账号", "errorrrrrr, 切换登录账号")

        # 退出登录
        # self.driver.find_element_by_id("com.mowin.scenesdeer:id/logout_login").click()

        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()



    def checkSceneType(self,sceneName,exlSheet,sheetNum,id0,id1,id2,id3,ignoreBeforeNums):
        # ignoreBeforeNums 表示忽略分类前N个，这N个不进行遍历.
        # 附近场景，遍历分类及商圈内容
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/home_tab").click()
        sleep(2)
        self.driver.find_element_by_id(id0).click()
        sleep(2)

        # 遍历一级分类
        l_onetmp = []
        l_one = []
        l_exlone = []
        l_onenum = tmp0 = 0
        dd = self.driver.find_element_by_id(id1).find_elements_by_id(id3)
        for d in dd:
            l_onetmp.append(d.text)
        # 向上滚屏3次，可修改滚屏次数
        for i in range(0, 3):
            (startX, endX, startY, endY) = self.screenWidthHeight(id1)
            self.driver.swipe(endX/2, endY-95, endX/2, startY+95, 1000)  # 向上滚动
            dd = self.driver.find_element_by_id(id1).find_elements_by_id(id3)
            for d in dd:
                l_onetmp.append(d.text)
            sleep(1)
        # 去重生成一级分类列表 l_one[]
        for id in l_onetmp:
            if id not in l_one:
                l_one.append(id)
                l_onenum = l_onenum + 1
        # for id in range(0, l_d):
        #     print l_one[id]
        # 向下滚屏3次
        for i in range(0, 3):
            self.driver.swipe(endX/2, startY+1, endX/2, endY-1, 1000)  # 向下滚动
            sleep(1)
        # 与excel中的预期数据进行比较并记录结果。
        for j in range(self.exlColnums(exlSheet, 1)):
            l_exlone.append(eval(exlSheet).cell_value(j, 0))
        if len(l_one) != len(l_exlone):
            print "[Errorrrrr, " + sceneName + " , 预期与实测数量不一致!]"
        else:
            for j in range(self.exlColnums(exlSheet, 1)):
                newWs = newbk.get_sheet(sheetNum)
                if l_one[j] == l_exlone[j]:
                     newWs.write(j, 1, "OK", styleBlue)
                     tmp0=tmp0+1
                else:
                     print "[Errorrrrr, " + sceneName + " -  预期(" + l_exlone[j] + ") <> 实测(" + l_one[j] + ")]"
                     newWs.write(j, 1, l_one[j], styleRed)
                     tmp0=0
            newbk.save(varExcel)
            if tmp0 == len(l_one):
                print "[OK, " + sceneName + ", 一级分类]"

        # 遍历一级分类，获取商圈名
        dnum = countdslen = 0
        y = z = 2
        l_twotmp = []
        dslen = len(self.driver.find_element_by_id(id1).find_elements_by_id(id3))
        for i in range(int(l_onenum/dslen)+1):
            ds = self.driver.find_element_by_id(id1).find_elements_by_id(id3)
            for d in ds:
                if dnum < ignoreBeforeNums:
                    dnum = dnum + 1
                elif d.text == l_one[dnum]:
                    # print d.text
                    d.click()
                    sleep(1)
                    dd2 = self.driver.find_element_by_id(id2).find_elements_by_id(id3)
                    for d2 in dd2:
                        l_twotmp.append(d2.text)

                    # 商圈，向上滚动3次，？？？考虑每个商圈都有"其他"，当显示其他时则无需再滚动。
                    (startX, endX, startY, endY) = self.screenWidthHeight(id2)
                    if endY > 500:
                        for i in range(0, 3):
                            self.driver.swipe(endX-1, endY-95, endX-1, startY+95, 1000)  # 向上滚动
                            dd2 = self.driver.find_element_by_id(id2).find_elements_by_id(id3)
                            for d2 in dd2:
                                l_twotmp.append(d2.text)
                            sleep(2)

                    # 去重生成 l_two[n]
                    l_two = []
                    l_s = 0
                    for id in l_twotmp:
                        if id not in l_two:
                            l_two.append(id)
                            l_s = l_s + 1
                    # for id in range(0, l_s):
                    #     print l_two[id]
                    dnum = dnum + 1
                    l_twotmp = []
                    countdslen = countdslen + 1
                    l_exltwo = []
                    tmp1 =0

                    # 与excel中的预期数据进行比较并记录结果
                    for j in range(self.exlColnums(exlSheet, countdslen + y)):
                        l_exltwo.append(eval(exlSheet).cell_value(j, countdslen + y - 1))
                    if len(l_two) != len(l_exltwo):
                        print "[Errorrrrr, " + sceneName + " - " + l_exltwo[0] + " - 预期" + str(len(l_exltwo)) + "个, 实测" + str(len(l_two)) + "个]"
                    else:
                        for j in range(self.exlColnums(exlSheet, countdslen + y)):
                            newWs = newbk.get_sheet(sheetNum)
                            if l_two[j] == l_exltwo[j]:
                                newWs.write(j, countdslen + y, "OK", styleBlue)
                                tmp1 = tmp1 + 1
                            else:
                                print "[Errorrrrr, " + sceneName + " - " + d.text  +" - 预期(" + l_exltwo[j] + ") <> 实测(" + l_two[j] + ")]"
                                newWs.write(j, countdslen + y, l_two[j], styleRed)
                                tmp1 = 0
                        newbk.save(varExcel)
                        if tmp1 == len(l_two):
                            print "[OK, " + sceneName + " - " + d.text + "]"
                    l_exltwo = []
                    y = y +1

            (startX, endX, startY, endY) = self.screenWidthHeight(id1)
            self.driver.swipe(endX-1, endY-90, endX-1, startY+90, 1000)  # 向上滚动
            ignoreBeforeNums = 0
            sleep(4)


    # 附近场景
    def drv_near(self):
        self.TestcaseModule()
    def nearSceneType(self):
        # C4-1,检查附近场景分类
        print ">" * 150
        print "C4-1,检查附近场景分类"
        self.checkSceneType("附近场景","sheetArea", 2,self.str_list[0],self.str_list[1],self.str_list[2],self.str_list[3],0)
        pass

    def nearComSceneType(self):
        # C4-2,检查公共场景分类
        print ">" * 150
        print "C4-2,检查公共场景分类"
        # self.driver.swipe(500, 270, 500, 270, 1000)
        self.driver.swipe(200, 100, 200, 100, 1000)
        # sleep(2)
        self.checkSceneType("公共场景","sheetCom", 3,self.str_list[0],self.str_list[1],self.str_list[2],self.str_list[3],4)
        # pass

    def nearSplitSceneType(self):
        # C4-3,检查分场景分类
        print ">" * 150
        print "C4-3,检查分场景分类"
        self.driver.swipe(200, 100, 200, 100, 1000)
        sleep(2)
        self.checkSceneType("分场景","sheetSplit", 4,self.str_list[0],self.str_list[1],self.str_list[2],self.str_list[3],1)





    # 我的场景
    def drv_my(self):
        self.TestcaseModule()
    def my(self):
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/my_scenes_tab").click()
        sleep(2)

    # 私聊
    def drv_chat(self):
        self.TestcaseModule()
    def chat(self):
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/chat_tab").click()
        sleep(2)



if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(cjl)  # 构造测试集
    unittest.TextTestRunner(verbosity=2).run(suite1)  # 执行测试

