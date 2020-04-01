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

# str_list= []
# for m in range(7, 30):  # id0 - id16
#   if sheetTestCase.cell(27, m).value != "":
#       N = sheetTestCase.cell_value(27, m)
#       N = sheetMain.cell_value(1, 5) + ":" + N
#       str_list.append(str(N))
#       print str_list[m-7]
#   else:
#       break
# sleep(1212)

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

        sleep(5)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/nextView").click()  # 场景进入
        sleep(5)
        self.varnickname = "test"
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
              for m in range(7, 30):  # id0 - id16
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
    def assertEqual(self,expected, actual,okmsg,errmsg):
        if expected == actual :print okmsg
        else:print errmsg
    def assertContain(self,one,allcontain,okmsg,errmsg):
        if one in allcontain: print okmsg
        else:print errmsg
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
        return int(location["x"]), varWidth, int(location["y"]), varHeight
    def exlColnums(self,exlSheet,col):
        # 获取sheetArea某列的行数 (表格列从1算起)
        # 遍历分类
        vatCount = 0
        varContent = [eval(exlSheet).cell(i, col-1).value for i in range(eval(exlSheet).nrows)]
        for i in range(len(varContent)):
            if varContent[i]!="":vatCount = vatCount + 1
            else:break
        return vatCount
    def camera(self, choose1):
        # self.camera("拍照")
        # 点击某一头像或照片后 遍历下拉框中" 拍照、从手机相册选择、取消"，并触发某一项
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

    def toShare(self, platform):
        # 分享到第三方平台
        # 检查页面元素 - 5个平台 + 取消
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/time_line_min_icon").is_displayed(), True, "OK, 朋友圈icon", "errorrrrrr, 朋友圈icon")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/time_line_min_layout").find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, "朋友圈", "OK, 朋友圈", "errorrrrrr, 朋友圈")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/wx_session_min_icon").is_displayed(), True, "OK, 微信好友icon", "errorrrrrr, 微信好友icon")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/wx_session_min_layout").find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, "微信好友", "OK, 微信好友" , "errorrrrrr, 微信好友")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/qq_friend_min_icon").is_displayed(), True, "OK, QQicon", "errorrrrrr, QQicon")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/qq_friend_min_layout").find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, "QQ", "OK, QQ", "errorrrrrr, QQ")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/qq_zone_min_icon").is_displayed(), True, "OK, QQ空间icon", "errorrrrrr, QQ空间icon")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/qq_zone_min_layout").find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, "QQ空间", "OK, QQ空间", "errorrrrrr, QQ空间")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/sina_weibo_min_icon").is_displayed(), True, "OK, 新浪微博icon", "errorrrrrr, 新浪微博	icon")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/sina_weibo_min_layout").find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, "新浪微博", "OK, 新浪微博", "errorrrrrr, 新浪微博")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/cancel").text, "取消", "OK, 取消", "errorrrrrr, 取消")
        sleep(2)
        # 分享平台
        if platform == "朋友圈":
            # 朋友圈
            self.driver.find_element_by_id("com.mowin.scenesdeer:id/time_line_min_layout").click()
            sleep(4)
            # 登录微信
            if self.driver.find_element_by_id("android:id/text1").text == "登录微信":
                self.driver.find_element_by_id("com.tencent.mm:id/b_t").find_element_by_xpath("//android.widget.EditText[contains(@index,1)]").send_keys("happyjinhao")
                self.driver.find_element_by_id("com.tencent.mm:id/b_u").find_element_by_xpath("//android.widget.EditText[contains(@index,1)]").send_keys("jinhao123")
                self.driver.find_element_by_id("com.tencent.mm:id/b_v").click()
                sleep(4)
                # 登录失败，返回
                if self.getElementExist("com.tencent.mm:id/bnn") == True :
                    self.driver.find_element_by_id("com.tencent.mm:id/bnn").click()
                    self.driver.find_element_by_id("com.tencent.mm:id/gd").click()
                sleep(12)
            self.assertEqual(self.driver.find_element_by_id("com.tencent.mm:id/bh6").text, "想看看附近伙伴都在聊什么？快试试场景鹿吧！聊天社交很方便~", "OK, 想看看附近伙伴都在聊什么？快试试场景鹿吧！聊天社交很方便~", "errorrrrrr, 想看看附近伙伴都在聊什么？快试试场景鹿吧！聊天社交很方便~")
            self.driver.find_element_by_id("com.tencent.mm:id/fw").click()  # 发送
        elif platform == "微信好友":
            # 微信好友
            self.driver.find_element_by_id("com.mowin.scenesdeer:id/wx_session_min_layout").click()
            sleep(4)
            # 选择好友 令狐冲
            self.driver.find_element_by_id("com.tencent.mm:id/brn").click()
            sleep(4)
            self.assertEqual(self.driver.find_element_by_id("com.tencent.mm:id/aa3").text, "[链接]我一直在用场景鹿和附近的伙伴们聊天，真的很方便，你也一起来吧~", "OK, [链接]我一直在用场景鹿和附近的伙伴们聊天，真的很方便，你也一起来吧~", "errorrrrrr, [链接]我一直在用场景鹿和附近的伙伴们聊天，真的很方便，你也一起来吧~")
            self.driver.find_element_by_id("com.tencent.mm:id/bnn").click()
            self.driver.find_element_by_id("com.tencent.mm:id/aa1").click()
        elif platform == "QQ":
            # QQ
            self.driver.find_element_by_id("com.mowin.scenesdeer:id/qq_friend_min_layout").click()
            sleep(4)
            # QQ已登录情况 (测试QQ：3525023378，这里index=5 是令狐冲，可按照实际情况调整)
            self.driver.find_element_by_id("com.tencent.mobileqq:id/listView1").find_element_by_xpath("//android.widget.RelativeLayout[contains(@index,5)]").click()
            sleep(4)
            self.assertEqual(self.driver.find_element_by_id("com.tencent.mobileqq:id/name").text, "我一直在用场景鹿和附近的伙伴们...", "OK, 我一直在用场景鹿和附近的伙伴们...", "errorrrrrr, 我一直在用场景鹿和附近的伙伴们...")
            self.assertEqual(self.driver.find_element_by_id("com.tencent.mobileqq:id/tv_summary").text, "想看看附近伙伴都在聊什么？快试试场景鹿吧！聊天社交很方便~", "OK, 想看看附近伙伴都在聊什么？快试试场景鹿吧！聊天社交很方便~", "errorrrrrr, 想看看附近伙伴都在聊什么？快试试场景鹿吧！聊天社交很方便~")
            self.driver.find_element_by_id("com.tencent.mobileqq:id/dialogRightBtn").click()
            self.driver.find_element_by_id("com.tencent.mobileqq:id/dialogLeftBtn").click()
        elif platform == "QQ空间":
            # QQ空间
            self.driver.find_element_by_id("com.mowin.scenesdeer:id/qq_zone_min_layout").click()
            sleep(4)
            self.driver.find_element_by_id("com.tencent.mobileqq:id/ivTitleBtnRightText").click()
        elif platform == "微博新浪":
            # 微博新浪
            self.driver.find_element_by_id("com.mowin.scenesdeer:id/sina_weibo_min_layout").click()
            sleep(4)
            self.assertEqual(self.driver.find_element_by_id("com.sina.weibo:id/edit_view").text, "想看看附近伙伴都在聊什么？快试试场景鹿吧！聊天社交很方便~", "OK, 想看看附近伙伴都在聊什么？快试试场景鹿吧！聊天社交很方便~", "errorrrrrr, 想看看附近伙伴都在聊什么？快试试场景鹿吧！聊天社交很方便~")
            self.driver.find_element_by_id("com.sina.weibo:id/titleSave").click()  # 发送
        else:
            print "Errorrrrrr, 分享的渠道不存在！"


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
    def installAPK(self, ApkName, appPackage, appActivity):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        print "[doing..., " + str(ApkName) + "]"
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
        # 跳转我
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()
        sleep(4)

        # 点击登录
        if self.getElementExist(self.str_list[1]) == True :
            # 点击设置，进行退出操作并返回到我页面
            self.driver.find_element_by_id(self.str_list[0]).click()
            self.driver.find_element_by_id(self.str_list[2]).click()
            self.driver.find_element_by_id(self.str_list[3]).click()
            sleep(2)
            self.driver.find_element_by_id(self.str_list[4]).click()
            sleep(2)
            self.driver.find_element_by_id(self.str_list[5]).click()
        else:
            self.assertEqual(self.driver.find_element_by_id(self.str_list[5]).find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text ,"点击登录", "OK, 点击登录", "errorrrrrr, 点击登录")
            # el = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.ScrollView/android.widget.RelativeLayout/child::android.widget.RelativeLayout/child::android.widget.RelativeLayout[1]/android.widget.TextView[contains(@text,'点击登录')]")
            self.driver.find_element_by_id(self.str_list[5]).click()
        sleep(2)
    def loginElement(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        # 无密码快捷登录,页面元素检查
        (a, b) = self.assertSplit(self.str_list[0])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        (a, b) = self.assertSplit(self.str_list[1])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        (a, b) = self.assertSplit(self.str_list[2])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        (a, b) = self.assertSplit(self.str_list[3])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        (a, b) = self.assertSplit(self.str_list[4])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        (a, b) = self.assertSplit(self.str_list[5])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        (a, b) = self.assertSplit(self.str_list[6])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        (a, b) = self.assertSplit(self.str_list[7])
        self.assertEqual(self.driver.find_element_by_id(a).find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, b, "OK, " + b, "errorrrrrr, " + b)
        # 微信
        (a, b) = self.assertSplit(self.str_list[8])
        self.assertEqual(self.driver.find_element_by_id(a).is_displayed(), True, "OK, " + b + "btn", "errorrrrrr, " + b + "btn")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/contentParentLayout").find_element_by_xpath("//android.widget.RelativeLayout/child::android.widget.LinearLayout/child::android.widget.RelativeLayout[1]/android.widget.TextView[contains(@index,1)]").text, b, "OK, " + b, "errorrrrrr, " + b)

        # QQ
        (a, b) = self.assertSplit(self.str_list[9])
        self.assertEqual(self.driver.find_element_by_id(a).is_displayed(), True, "OK, " + b + "btn", "errorrrrrr, " + b + "btn")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/contentParentLayout").find_element_by_xpath("//android.widget.RelativeLayout/child::android.widget.LinearLayout/child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,1)]").text, b, "OK, " + b, "errorrrrrr, " + b)

        # 微博
        (a, b) = self.assertSplit(self.str_list[10])
        self.assertEqual(self.driver.find_element_by_id(a).is_displayed(), True, "OK, " + b + "btn", "errorrrrrr, " + b + "btn")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/contentParentLayout").find_element_by_xpath("//android.widget.RelativeLayout/child::android.widget.LinearLayout/child::android.widget.RelativeLayout[3]/android.widget.TextView[contains(@index,1)]").text, b, "OK, " + b, "errorrrrrr, " + b)
    def loginPhone(self, testPhone):
        print ">" * 150
        print "C2-1-2, 手机号登录"
        # ? 从数据库中获取最大的手机号并+1 ，确保每次登录的手机号是最新的。（未做）
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/phoneNumber").send_keys(int(testPhone))  # testPhone 手机号码
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/getMobileCode").click()  # 获取验证码
        sleep(5)
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/mobileCode").send_keys(getCJLverifyCode(int(sheetMain.cell_value(1, 7))))  # 输入验证码
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/login").click()  # 手机号登录(页面跳转到我)
        if self.getElementExist("com.mowin.scenesdeer:id/name") == True:
            print str(int(testPhone)) + "("+self.driver.find_element_by_id("com.mowin.scenesdeer:id/name").text+") , 已登录"
        else:
            print str(int(testPhone)) + " , 已登录"
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

        # 新用户第一次登录后才会进入 完善个人资料
        (a, b) = self.assertSplit(self.str_list[5])
        if self.getElementExist("com.mowin.scenesdeer:id/title") == True:
            if self.driver.find_element_by_id(a).text == b:
                # 检查返回
                self.assertEqual(self.driver.find_element_by_id(self.str_list[0]).is_displayed(), True, "OK, 返回键", "errorrrrrr, 返回键")

                # 5=完善个人资料 , 6=上传头像 , 7=昵称 , 8=输入昵称 , 9=我是帅哥 ,10=我是美女 ，
                for i in range(5, 11):
                    (a, b) = self.assertSplit(self.str_list[i])
                    self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
                (a, b) = self.assertSplit(self.str_list[11])
                self.assertEqual(self.driver.find_element_by_id(a).find_element_by_xpath("//android.widget.TextView[contains(@index,8)]").text, b, "OK, " + b, "errorrrrrr, " + b)

                # 点击 拍照机，检查文案"拍照、从手机相册选择、取消"
                self.driver.find_element_by_id(self.str_list[1]).click()  # 上传头像
                sleep(6)
                self.camera("从手机相册选择")
                sleep(3)

                # 品牌名: ATH-AL00 ,选择第10张
                varimages = self.driver.find_elements_by_id(self.str_list[12])
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
                self.varnickname = sheetMain.cell_value(1, 6) + str(int(sheetMain.cell_value(1, 7)))[-4:]
                (a, b) = self.assertSplit(self.str_list[8])
                self.driver.find_element_by_id(a).send_keys(self.varnickname)  # 输入昵称
                sleep(2)
                (a, b) = self.assertSplit(self.str_list[9])
                self.driver.find_element_by_id(a).click()  # 选择性别,男
                self.driver.find_element_by_id(self.str_list[13]).click()  # 完成
                sleep(3)
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
        print sheetTestCase.cell_value(self.l, 4)
        # "C3-1,我，页面元素（头像、昵称、性别、小鹿号、个人签名、二维码、通讯录、我建的场景、我的相册、我的足迹、分享、设置、扫一扫）"
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()
        sleep(4)
        # 我
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/status_bar").find_element_by_xpath("//android.widget.TextView[contains(@index,0)]").text,"我", "OK, 我", "errorrrrrr, 我")

        # 扫一扫
        self.assertEqual(self.driver.find_element_by_id(self.str_list[12]).is_displayed(), True, "OK, 扫一扫", "errorrrrrr, 扫一扫")
        self.driver.find_element_by_id(self.str_list[12]).click()

        # 头像
        self.assertEqual(self.driver.find_element_by_id(self.str_list[0]).is_displayed(), True, "OK, 头像", "errorrrrrr, 头像")

        # 昵称
        self.assertEqual(self.driver.find_element_by_id(self.str_list[1]).text, self.varnickname, "OK, 昵称", "errorrrrrr, 昵称 ," + self.varnickname + "<>" + self.driver.find_element_by_id(self.str_list[1]).text)

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
        # 先获取我页面中的小鹿号，(小鹿号：2016122710030)
        varDeernumber = self.driver.find_element_by_id("com.mowin.scenesdeer:id/small_deer_number").text
        varDeernumber = "我的" + varDeernumber.replace("：", ":")

        # 点击搜索
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
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/actionBar").find_element_by_xpath("//android.widget.ImageView[contains(@index,2)]").click()
        self.driver.keyevent(67)  # 退格键
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
        print sheetTestCase.cell_value(self.l, 4)
        # C3-7,我 - 分享[场景鹿]给好友(朋友圈、微信好友、QQ、QQ空间、新浪微博)"
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
        (a, b) = self.assertSplit(self.str_list[11])
        self.driver.find_element_by_id(a).click()
        sleep(2)
    def meSetup(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        #  "C3-8,我 - 设置"
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
        sleep(2)
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/title").text, "用户协议", "OK, 用户协议", "errorrrrrr, 用户协议")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()

        # 隐私政策
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/privacy_policy").text, "隐私政策", "OK, 隐私政策", "errorrrrrr, 隐私政策")
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/privacy_policy").click()
        sleep(2)
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

        # 切换帐号或退出登录 （?未做第三方检查）
        (a, b) = self.assertSplit(self.str_list[8])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).click()
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/title").text, "切换帐号/退出登录", "OK, 切换帐号/退出登录", "errorrrrrr, 切换帐号/退出登录")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/switch_account").text, "切换登录账号", "OK, 切换登录账号", "errorrrrrr, 切换登录账号")

        # 新用户
        # com.mowin.scenesdeer:id/list_view
        # com.mowin.scenesdeer:id/content_layout
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/thumb").is_displayed(),True, "OK, 用户头像", "errorrrrrr, 用户头像")
        print "昵称 = " + self.driver.find_element_by_id("com.mowin.scenesdeer:id/nick_name").text
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/account_source").text,"手机号账号", "OK, 手机号账号", "errorrrrrr, 手机号账号")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/checked").is_displayed(),True, "OK, 打勾icon", "errorrrrrr, 打勾icon")

        # 退出登录（返回我页面）
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/logout_login").click()
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/content").text,"退出后不会删除任何历史数据，下次登录依然可以使用本账号。", "OK, 退出后不会删除任何历史数据，下次登录依然可以使用本账号。", "errorrrrrr, 退出后不会删除任何历史数据，下次登录依然可以使用本账号。")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/negative").text,"取消", "OK, 取消", "errorrrrrr, 取消")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/positive").text,"确定", "OK, 确定", "errorrrrrr, 确定")
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/positive").click()
        sleep(2)
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/no_data_layout").click()
        sleep(2)
        self.loginPhone(sheetMain.cell_value(1, 7))

        # self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()
        # self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()



    # 附近场景
    def drv_near(self):
        self.TestcaseModule()
    def nearSceneType(self):
        # C4-1,检查附近场景分类
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.checkSceneType("附近场景","sheetArea", 2,self.str_list[0],self.str_list[1],self.str_list[2],self.str_list[3],0)
    def nearComSceneType(self):
        # C4-2,检查公共场景分类
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.driver.swipe(200, 100, 200, 100, 1000)
        sleep(2)
        self.checkSceneType("公共场景","sheetCom", 3,self.str_list[0],self.str_list[1],self.str_list[2],self.str_list[3],4)
    def nearSplitSceneType(self):
        # C4-3,检查分场景分类
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.driver.swipe(200, 100, 200, 100, 1000)
        sleep(2)
        self.checkSceneType("分场景","sheetSplit", 4,self.str_list[0],self.str_list[1],self.str_list[2],self.str_list[3],1)

    def nearElement(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        # C4-4,页面元素（城市、搜索、+）
        # 城市
        (a, b) = self.assertSplit(self.str_list[0])

        self.assertEqual(self.driver.find_element_by_id(a).text[0:3], b, "OK, " + b , "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).click()
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/title").text, "选择城市", "OK, 选择城市" , "errorrrrrr, 选择城市")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/search").text, "输入城市名、拼音首字母", "OK, 输入城市名、拼音首字母" , "errorrrrrr, 输入城市名、拼音首字母")

        # GPS定位城市
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/gps_location_title").text, "GPS定位城市", "OK, GPS定位城市" , "errorrrrrr, GPS定位城市")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/gps_location").text, "上海市市辖区", "OK, 上海市市辖区" , "errorrrrrr, 上海市市辖区")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/hot_city_title").text, "热门城市", "OK, 热门城市" , "errorrrrrr, 热门城市")

        # 遍历3个热门城市
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/hot_city_list").find_element_by_xpath("//child::android.widget.RelativeLayout[1]/android.widget.TextView[contains(@index,0)]").text, "北京市市辖区", "OK, 北京市市辖区", "errorrrrrr, 北京市市辖区")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/hot_city_list").find_element_by_xpath("//child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,0)]").text, "天津市市辖区", "OK, 天津市市辖区", "errorrrrrr, 天津市市辖区")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/hot_city_list").find_element_by_xpath("//child::android.widget.RelativeLayout[3]/android.widget.TextView[contains(@index,0)]").text, "上海市市辖区", "OK, 上海市市辖区", "errorrrrrr, 上海市市辖区")
        # 点击北京市市辖区
        el4 = self.driver.find_element_by_id("com.mowin.scenesdeer:id/hot_city_list").find_element_by_xpath("//child::android.widget.RelativeLayout[1]/android.widget.TextView[contains(@index,0)]")
        el4.click()
        sleep(2)
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/city").text[0:3], "北京市", "OK, 北京市" + b , "errorrrrrr, 北京市")

        # 搜索场景
        (a, b) = self.assertSplit(self.str_list[1])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b , "errorrrrrr, " + b)
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/search_scene").click()
        sleep(2)
        # 搜公共场景
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/search_scene").text, "输入公共场景名称、地点等", "OK, 输入公共场景名称、地点等" , "errorrrrrr, 输入公共场景名称、地点等")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/text1").text, "搜公共场景", "OK, 搜公共场景" , "errorrrrrr, 搜公共场景")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/public_classify").text, "公共场景", "OK, 公共场景" , "errorrrrrr, 公共场景")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/arrow").is_displayed(), True, "OK, 下箭头btn" , "errorrrrrr, 下箭头btn")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/search_history").text, "历史搜索", "OK, 历史搜索" , "errorrrrrr, 历史搜索")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/clear_search_recorder").text, "清空搜索记录", "OK, 清空搜索记录" , "errorrrrrr, 清空搜索记录")

        # 搜分场景
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/text2").text, "搜分场景", "OK, 搜分场景" , "errorrrrrr, 搜分场景")
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/child_scene_layout").click()
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/search_scene").text, "输入分场景名称、地点等", "OK, 输入分场景名称、地点等" , "errorrrrrr, 输入分场景名称、地点等")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/public_classify").text, "分场景", "OK, 分场景" , "errorrrrrr, 分场景")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/arrow").is_displayed(), True, "OK, 下箭头btn" , "errorrrrrr, 下箭头btn")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/search_history").text, "历史搜索", "OK, 历史搜索" , "errorrrrrr, 历史搜索")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/clear_search_recorder").text, "清空搜索记录", "OK, 清空搜索记录" , "errorrrrrr, 清空搜索记录")

        # 搜场景号
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/text3").text, "搜场景号", "OK, 搜场景号" , "errorrrrrr, 搜场景号")
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/scenes_num_layout").click()
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/search_scene").text, "输入场景号", "OK, 输入场景号" , "errorrrrrr, 输入场景号")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/search_history").text, "历史搜索", "OK, 历史搜索" , "errorrrrrr, 历史搜索")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/clear_search_recorder").text, "清空搜索记录", "OK, 清空搜索记录" , "errorrrrrr, 清空搜索记录")
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/back").click()
        sleep(2)

        # 北京市默认没有场景
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/no_data_icon").is_displayed(), True, "OK, 背景鹿头" , "errorrrrrr, 背景鹿头")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/no_data_hint").text, "很遗憾，附近还没有场景", "OK, 很遗憾，附近还没有场景" , "errorrrrrr, 很遗憾，附近还没有场景")

        # 加号
        self.assertEqual(self.driver.find_element_by_id(self.str_list[2]).is_displayed(), True, "OK, 右上角加号btn", "errorrrrrr, 右上角加号btn")

    def nearCreateCom(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        # C4-5,创建公共场景
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/home_tab_hint").click()
        sleep(2)

        # 点击加号
        self.driver.find_element_by_id(self.str_list[0]).click()
        sleep(2)
        # 点击 创建公共场景
        self.driver.swipe(self.screenX-100, 310, self.screenX-100, 310, 1000)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "创建公共场景", "OK, 创建公共场景", "errorrrrrr, 创建公共场景")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/my_location").text, "我的位置:", "OK, 我的位置:", "errorrrrrr, 我的位置:")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/map").is_displayed(), True, "OK, 定位btn" , "errorrrrrr, 定位btn")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/location_name").text, "场景地点名称", "OK, 场景地点名称", "errorrrrrr, 场景地点名称")
        # 选择地点所属区域/商圈
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/location_name_ed").send_keys(u"人民广场" +str(randomDigits(4)))
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/business_area").text, "选择地点所属区域/商圈", "OK, 选择地点所属区域/商圈", "errorrrrrr, 选择地点所属区域/商圈")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/business_area").click()
        sleep(4)
        self.driver.swipe(self.screenX-100, 600, self.screenX-100, 600, 1000)  # 选择分类
        sleep(3)
        # 选择地点分类
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/area_classify").text, "选择地点分类", "OK, 选择地点分类", "errorrrrrr, 选择地点分类")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/area_classify").click()
        sleep(4)
        self.driver.swipe(self.screenX-100, 600, self.screenX-100, 600, 1000)  # 选择分类
        sleep(3)

        el4 = self.driver.find_element_by_id("com.mowin.scenesdeer:id/contentParentLayout").find_element_by_xpath("//android.widget.ScrollView/android.widget.LinearLayout/android.widget.TextView[contains(@index,9)]")
        self.assertEqual(el4.text, "【公共场景】是现实生活场景的网络空间。当你加入所在的小区、商务楼、学校、商场等以地理位置定义的场景,便可以自由寻找同一场景的伙伴,进行社交。相同的地点只存在一个公共场景。", "OK, 【公共场景】是现实生活场景的网络空间。当你加入所在的小区、商务楼、学校、商场等以地理位置定义的场景,便可以自由寻找同一场景的伙伴,进行社交。相同的地点只存在一个公共场景。", "errorrrrrr, 【公共场景】是现实生活场景的网络空间。当你加入所在的小区、商务楼、学校、商场等以地理位置定义的场景,便可以自由寻找同一场景的伙伴,进行社交。相同的地点只存在一个公共场景。")

        el4 = self.driver.find_element_by_id("com.mowin.scenesdeer:id/contentParentLayout").find_element_by_xpath("//android.widget.ScrollView/android.widget.LinearLayout/android.widget.TextView[contains(@index,10)]")
        self.assertEqual(el4.text, "在公共场景下你可以创建自定义分场景,召集兴趣相投的小伙伴。", "OK, 在公共场景下你可以创建自定义分场景,召集兴趣相投的小伙伴。", "errorrrrrr, 在公共场景下你可以创建自定义分场景,召集兴趣相投的小伙伴。")

        # 确认
        # self.driver.find_element_by_id("com.mowin.scenesdeer:id/sure").click()


    # 我的场景
    def drv_my(self):
        self.TestcaseModule()
    def myScene(self):
        # C5-1,我的场景列表，进入公共场景
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/my_scenes_tab").click()
        sleep(2)

        mySceneLists = self.driver.find_elements_by_id("com.mowin.scenesdeer:id/my_scene_layout")
        for mySceneList in mySceneLists:
            try:
                mySceneList.find_element_by_id("com.mowin.scenesdeer:id/scene_mark")
                # mySceneList.find_element_by_id("com.mowin.scenesdeer:id/scene_address")
                self.varGONG = mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[1]/android.widget.TextView[contains(@index,0)]").text
                self.varComSceneName = mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,0)]").text
                self.varComSceneAddress = mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[3]/android.widget.TextView[contains(@index,0)]").text
                varPeopleNums = mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,1)]").text
                varComSceneTime = mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,2)]").text
                print self.varGONG + " , " + self.varComSceneName + " , " + self.varComSceneAddress + " , " + varPeopleNums + " , " + varComSceneTime

                mySceneList.click()
                sleep(2)
                break
            except :
                try:
                    mySceneList.find_element_by_id("com.mowin.scenesdeer:id/scene_address")
                    print mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,0)]").text + " , " + mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[3]/android.widget.TextView[contains(@index,0)]").text + " , " + mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,1)]").text + " , " + mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,2)]").text
                except:
                    print mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,0)]").text + " , " + mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,1)]").text + " , " + mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,2)]").text

    def mySceneCom(self):
        # C5-2,公共场景详情页
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        sleep(5)
        self.driver.find_element_by_id(self.str_list[3]).send_keys(u"john123")
        sleep(2)
        self.driver.keyevent(66)
        sleep(2)
        self.driver.find_element_by_id(self.str_list[2]).click()
        sleep(1)
        self.driver.swipe(self.screenX-100, 300, self.screenX-100, 300, 1000)
        sleep(2)
    def mySceneInfo(self):
        # C5-3,场景信息
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        # 场景信息
        (a, b) = self.assertSplit(self.str_list[0])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.assertEqual(self.driver.find_element_by_id(self.str_list[2]).text, self.varComSceneName, "OK, " + self.varComSceneName, "errorrrrrr, " + self.driver.find_element_by_id(self.str_list[2]).text + " <> " + self.varComSceneName)
        self.assertEqual(self.driver.find_element_by_id(self.str_list[1]).is_displayed(), True, "OK, 背景图" ,"errorrrrrr, 背景图")
        self.assertContain("场景ID", self.driver.find_element_by_id(self.str_list[3]).text, "OK, " + self.driver.find_element_by_id(self.str_list[3]).text, "errorrrrrr, " + self.driver.find_element_by_id(self.str_list[3]).text)
        self.assertEqual(self.getElementExist(self.str_list[4]), True, "OK, " + self.driver.find_element_by_id(self.str_list[4]).text, "errorrrrrr, " + self.driver.find_element_by_id(self.str_list[4]).text)
        (a, b) = self.assertSplit(self.str_list[5])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        (a, b) = self.assertSplit(self.str_list[6])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.assertContain("欢迎加入", self.driver.find_element_by_id(self.str_list[7]).text,"OK, " + self.driver.find_element_by_id(self.str_list[7]).text, "errorrrrrr, " + self.driver.find_element_by_id(self.str_list[7]).text)
        self.assertEqual(self.driver.find_element_by_id(self.str_list[8]).text, "地点：" + self.varComSceneAddress, "OK, 地址：" + self.varComSceneAddress, "errorrrrrr, 地址：" + self.varComSceneAddress)
        # print "(" + self.driver.find_element_by_id(self.str_list[8]).text + ")"
        # print "(地点：" + self.varComSceneAddress + ")"

        (a, b) = self.assertSplit(self.str_list[9])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)

        # 看看小伙伴们的足迹
        self.assertContain("看看小伙伴们的足迹(", self.driver.find_element_by_id(self.str_list[10]).text, "OK, " + self.driver.find_element_by_id(self.str_list[10]).text, "errorrrrrr, " + self.driver.find_element_by_id(self.str_list[10]).text)
        self.driver.find_element_by_id(self.str_list[10]).click()
        sleep(3)
        self.assertContain("足迹(", self.driver.find_element_by_id("com.mowin.scenesdeer:id/title").text, "OK, " + self.driver.find_element_by_id("com.mowin.scenesdeer:id/title").text, "errorrrrrr, " + self.driver.find_element_by_id("com.mowin.scenesdeer:id/title").text)
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/search_layout").is_displayed(), True, "OK, 搜索框", "errorrrrrr, 搜索框")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/search_logo").is_displayed(), True, "OK, 搜索icon", "errorrrrrr, 搜索icon")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/search").text, "搜索", "OK, 搜索", "errorrrrrr, 搜索")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/filter").text, "排序筛选", "OK, 排序筛选", "errorrrrrr, 排序筛选")
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/arrow_bottom").is_displayed(), True, "OK, 向下箭头icon", "errorrrrrr, 向下箭头icon")
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/back").click()

        # 分享场景
        (a, b) = self.assertSplit(self.str_list[11])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).click()
        self.toShare("朋友圈")
        (a, b, c, d) = self.screenWidthHeight("com.mowin.scenesdeer:id/contentParentLayout")
        self.driver.swipe(self.screenX-100, d-1, self.screenX-100, c+1, 1000)
        sleep(2)

        # 我在本场景的昵称
        self.assertEqual("我在本场景的昵称", self.driver.find_element_by_id("com.mowin.scenesdeer:id/myNickNameLayout").find_element_by_xpath("//android.widget.TextView[contains(@index,0)]").text, "Ok, 我在本场景的昵称" , "errorrrrrr, 我在本场景的昵称" )

        # 自动留下足迹，置顶聊天，查找聊天记录，报错／补充信息，清空聊天记录
        for i in range(12, 18):
            (a, b) = self.assertSplit(self.str_list[i])
            self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)

        # 查找聊天记录
        (a, b) = self.assertSplit(self.str_list[14])
        self.driver.find_element_by_id(a).click()
        self.assertEqual(self.driver.find_element_by_id("com.mowin.scenesdeer:id/search_scene").text, "搜索", "OK, 搜索", "errorrrrrr, 搜索")
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/search_scene").send_keys(u"john")
        sleep(2)
        self.driver.keyevent(66)
        sleep(2)
        x = self.driver.find_element_by_id("com.mowin.scenesdeer:id/list_view").find_element_by_xpath("//child::android.widget.LinearLayout[1]/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[contains(@index,0)]").text
        y = self.driver.find_element_by_id("com.mowin.scenesdeer:id/list_view").find_element_by_xpath("//child::android.widget.LinearLayout[1]/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[contains(@index,0)]").text
        print x + " , " + y

        sleep(1212)

        # # 删除并退出
        # (a, b) = self.assertSplit(self.str_list[17])
        # self.driver.find_element_by_id(a).click()

        self.driver.find_element_by_id("com.mowin.scenesdeer:id/back").click()




        # # 添加到我的场景
        # self.driver.swipe(self.screenX-100, 400, self.screenX-100, 400, 1000)
        #
        # # 创建分场景
        # self.driver.swipe(self.screenX-100, 600, self.screenX-100, 600, 1000)
        #
        # # 分享场景
        # self.driver.swipe(self.screenX-100, 800, self.screenX-100, 800, 1000)



    # 私聊
    def drv_chat(self):
        self.TestcaseModule()
    def chat(self):
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/chat_tab").click()
        sleep(2)
        (a, b) = self.assertSplit(self.str_list[0])
        self.assertEqual(self.driver.find_element_by_id(a).find_element_by_xpath("//android.widget.TextView[contains(@index,0)]").text, b, "Ok, " + b, "errorrrrrr, " + b)
        self.assertEqual(self.driver.find_element_by_id(self.str_list[1]).is_displayed(), True, "Ok, 通讯录icon" , "errorrrrrr, 通讯录icon")
        # 通讯录
        self.driver.find_element_by_id(self.str_list[1]).click()
        sleep(2)



        (a, b) = self.assertSplit(self.str_list[2])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "Ok, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(self.str_list[3]).click()
        (a, b) = self.assertSplit(self.str_list[4])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "Ok, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).send_keys("1234")
        # 未搜索到数据
        (a, b) = self.assertSplit(self.str_list[5])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "Ok, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id("com.mowin.scenesdeer:id/back").click()



if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(cjl)  # 构造测试集
    unittest.TextTestRunner(verbosity=2).run(suite1)  # 执行测试

