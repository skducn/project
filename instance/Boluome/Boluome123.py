# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description: android自动化测试框架
#***************************************************************

import os, sys, unittest, xlwt, xlrd, MySQLdb, tempfile,shutil,chardet,random,webbrowser,platform,string,datetime,redis,commands,urllib2,MultipartPostHandler
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
# from CJLinterfaceDriver import *
# from ssh_cmd import *
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from time import sleep

# print sys.path
# from resource.source.comparePic import *
# from resource.source import test2

#****************************************************************

# 参数化
varExcel = "/Users/linghuchong/Downloads/51/Project/CJL/excel/CJL1_0.xls"
varReport = "/Users/linghuchong/Downloads/51/Project/CJL/report/CJLreport1_0.html"
varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 获取当天日期时间,格式：20161020130318
varTableDetails = "/Users/linghuchong/Downloads/51/Project/CJL/report/CJLtable" + varTimeYMDHSM + ".html"
# connMongo155 = MongoClient('192.168.2.155', 10005); db = connMongo155.sceneWeb  # mongodb
# connRedis166 = redis.StrictRedis(host='192.168.2.166', port=6379, db=0, password="dlhy123456")  # redis CJL66
# connRedis167 = redis.StrictRedis(host='192.168.2.167', port=6380, db=0, password="dlhy123456")  # redis CJL67
# connPersonal = MySQLdb.connect(host='192.168.2.164', user='remote', passwd='Dlhy66506043', db='personal', port=3306, use_unicode=True)
# curPersonal = connPersonal.cursor();curPersonal.execute('SET NAMES utf8;');connPersonal.set_character_set('utf8');curPersonal.execute('show tables')
# connScenemsg = MySQLdb.connect(host='192.168.2.164', user='remote', passwd='Dlhy66506043', db='scenemsg', port=3306, use_unicode=True)
# curScenemsg = connScenemsg.cursor();curScenemsg.execute('SET NAMES utf8;');connScenemsg.set_character_set('utf8');curScenemsg.execute('show tables')
# connSysparam = MySQLdb.connect(host='192.168.2.164', user='remote', passwd='Dlhy66506043', db='sysparam', port=3306, use_unicode=True)
# curSysparam = connSysparam.cursor();curSysparam.execute('SET NAMES utf8;');connSysparam.set_character_set('utf8');curSysparam.execute('show tables')
# connUpload = MySQLdb.connect(host='192.168.2.164', user='remote', passwd='Dlhy66506043', db='upload', port=3306, use_unicode=True)
# curUpload = connUpload.cursor();curUpload.execute('SET NAMES utf8;');connUpload.set_character_set('utf8');curUpload.execute('show tables')
# bk = xlrd.open_workbook(varExcel, formatting_info=True)
# newbk = copy(bk)
# sheetMain = bk.sheet_by_name("main")
# sheetTestCase = bk.sheet_by_name("testcase")
# sheetArea = bk.sheet_by_name("area")
# sheetCom = bk.sheet_by_name("com")
# sheetSplit = bk.sheet_by_name("split")
# styleRed = xlwt.easyxf('font: name Times New Roman, color-index red')
# styleBlue = xlwt.easyxf('font: name Times New Roman, color-index blue')
# styleGray25 = xlwt.easyxf('font: name Times New Roman, color-index gray25')



class Boluome123(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print "21212"
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.1'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['appPackage'] = 'com.kuping.android.boluome.life'
        desired_caps['appActivity'] = 'com.kuping.android.boluome.life.ui.main.SplashActivity'
        desired_caps['unicodeKeyboard'] = 'True'
        desired_caps['resetKeyboard'] = 'True'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        reload(sys)
        sys.setdefaultencoding('utf8')


        print ">" * 150
        # 手机信息定义与输出
        # 定义手机分辨率的宽,高
        self.screenX = self.driver.get_window_size()['width']
        self.screenY = self.driver.get_window_size()['height']
        tmpProductmodel = commands.getoutput('adb shell getprop ro.product.model')
        tmpProductdevice = commands.getoutput('adb shell getprop ro.product.device')
        tmpSdk = commands.getoutput('adb shell getprop ro.build.version.sdk')
        tmpAbi = commands.getoutput('adb shell getprop ro.product.cpu.abi')
        tmpSerialno = commands.getoutput('adb shell getprop ro.serialno')
        self.productmodel = tmpProductmodel.strip()
        print "测试机品牌 = " + str(tmpProductmodel.strip()) + " , 设备号 = " + str(tmpProductdevice.strip()) + " , 分辨率 = " + str(self.screenX) + "*" + str(self.screenY) + " , Android版本 = " + str(androidVersion.strip()) + " , SDK = " + str(tmpSdk.strip()) + " , CPU = " + str(tmpAbi.strip()) + " , SerialNo = " + str(tmpSerialno.strip())



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

    def assertEqual(self, expected, actual, okmsg, errmsg):
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
        # 获取元素图片的长度和高度
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
    def camera(self, varWay,varPicNum):
        # self.camera("从手机相册选择",5)
        # 点击上传，弹出拉框" 拍照、从手机相册选择、取消"
        # 检查元素 - 拍照

        # self.assertEqual(el1.text, "拍照", "OK, " + el1.text, "errorrrrrr, " + el1.text)
        # 从手机相册选择

        # self.assertEqual(el2.text, "从手机相册选择", "OK, " + el2.text, "errorrrrrr, " + el2.text)
        # 取消
        # cancel = self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/cancel").text
        # self.assertEqual(cancel, "取消", "OK, 取消", "errorrrrrr, 取消")

        if varWay == "拍照":
            el1 = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[contains(@index,0)]")
            el1.click()
        elif varWay == "从手机相册选择":
            el2 = self.driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[contains(@index,2)]")
            el2.click()
        else:
            self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/cancel").click()

        sleep(5)
        varImages = self.driver.find_elements_by_id(sheetMain.cell_value(1, 5)+":id/image")
        x = 0
        for varImage in varImages:
            if x == varPicNum:
                varImage.click()
                break
            x = x + 1
        sleep(3)
        # 上传头像 - 点击保存 （调用第三方手机ID）
        for i in range(1, 6):
            if self.productmodel == sheetMain.cell_value(i, 9).encode("utf-8"):
                self.driver.find_element_by_id(sheetMain.cell_value(i, 10)).click()
                break
        sleep(3)

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
            print "[Errorrrrr, " + sceneName + " , 预期(" + str(len(l_exlone)) + ")与实测(" + str(len(l_one)) +")数量不一致!]"
        else:
            for j in range(self.exlColnums(exlSheet, 1)):
                newWs = newbk.get_sheet(sheetNum)
                if l_one[j] in l_exlone[j] :
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

        if int(l_onenum%dslen) == 0: xy = int(l_onenum/dslen)
        else: xy = int(l_onenum/dslen)+1

        for i in range(xy):
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
                    tmp1 = 0

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
            sleep(3)

    def getAttachment(self,attachmentFilePath):
        contentType, encoding = mimetypes.guess_type(attachmentFilePath)
        if contentType is None or encoding is not None:
            contentType = 'application/octet-stream'
        mainType, subType = contentType.split('/', 1)
        file = open(attachmentFilePath, 'rb')
        if mainType == 'text':
            attachment = MIMEText(file.read())
        elif mainType == 'message':
            attachment = email.message_from_file(file)
        elif mainType == 'image':
            attachment = MIMEImage(file.read(), subType=subType)
        elif mainType == 'audio':
            attachment = MIMEAudio(file.read(), subType=subType)
        else:
            attachment = MIMEBase(mainType, subType)
        attachment.set_payload(file.read())
        encode_base64(attachment)
        file.close()
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachmentFilePath))
        return attachment
    def sendemail(self, subject, text, *attachmentFilePaths):
        gmailUser = 'jinhao@mo-win.com.cn'
        gmailPassword = 'Dlhy123456'
        recipient = 'jinhao@mo-win.com.cn'
        # recipient = "'jinhao@mo-win.com.cn', 'guoweiliang@mo-win.com.cn'"
        msg = MIMEMultipart()
        msg['From'] = gmailUser
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(text, 'plain', 'utf-8'))
        # 附件是可选项
        for attachmentFilePath in attachmentFilePaths:
            if attachmentFilePath != '':
                 msg.attach(self.getAttachment(attachmentFilePath))
        mailServer = smtplib.SMTP('smtp.exmail.qq.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmailUser, gmailPassword)
        mailServer.sendmail(gmailUser, recipient, msg.as_string())
        mailServer.close()
        print('Sent email to %s' % recipient)
    def sendErrLog(self, subtitle, testStep):
        sleep(1)
        str154 = ssh_cmd("192.168.2.154", "root", "Dlhy66506043", "tail -70 /usr/local/tomcat/logs/catalina.out")
        str163 = ssh_cmd("192.168.2.163", "root", "Dlhy66506043", "tail -70 /usr/local/tomcat/logs/catalina.out")
        sleep(2)
        if "java.lang.NullPointerException" in str154: self.sendemail(u'server154ErrorLog - ' + subtitle, u'你好，\n\n        ' + subtitle + u' - 日志报错! \n\n        测试账号：' + myPhone + u'\n\n        步骤：'+ testStep +  '\n\n        ' + str(str154) + u'\n\n\n        本邮件自动发送，由于程序自动截取错误代码，可能存在误报现象，如有发生敬请谅解。\n\n', '')
        if "java.lang.NullPointerException" in str163: self.sendemail(u'server163ErrorLog - ' + subtitle, u'你好，\n\n        ' + subtitle + u' - 日志报错! \n\n        测试账号：' + myPhone + u'\n\n        步骤：'+ testStep +  '\n\n        ' + str(str163) + u'\n\n\n        本邮件自动发送，由于程序自动截取错误代码，可能存在误报现象，如有发生敬请谅解。\n\n', '')
    def toShare(self, platform):
        # 分享到第三方平台
        # 检查页面元素 - 5个平台 + 取消
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/time_line_min_icon").is_displayed(), True, "OK, 朋友圈icon", "errorrrrrr, 朋友圈icon")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/time_line_min_layout").find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, "朋友圈", "OK, 朋友圈", "errorrrrrr, 朋友圈")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/wx_session_min_icon").is_displayed(), True, "OK, 微信好友icon", "errorrrrrr, 微信好友icon")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/wx_session_min_layout").find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, "微信好友", "OK, 微信好友" , "errorrrrrr, 微信好友")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/qq_friend_min_icon").is_displayed(), True, "OK, QQicon", "errorrrrrr, QQicon")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/qq_friend_min_layout").find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, "QQ", "OK, QQ", "errorrrrrr, QQ")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/qq_zone_min_icon").is_displayed(), True, "OK, QQ空间icon", "errorrrrrr, QQ空间icon")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/qq_zone_min_layout").find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, "QQ空间", "OK, QQ空间", "errorrrrrr, QQ空间")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/sina_weibo_min_icon").is_displayed(), True, "OK, 新浪微博icon", "errorrrrrr, 新浪微博	icon")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/sina_weibo_min_layout").find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, "新浪微博", "OK, 新浪微博", "errorrrrrr, 新浪微博")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/cancel").text, "取消", "OK, 取消", "errorrrrrr, 取消")
        sleep(2)
        # 分享平台
        if platform == "朋友圈":
            # 朋友圈
            self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/time_line_min_layout").click()
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
            self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/wx_session_min_layout").click()
            sleep(4)
            # 选择好友 令狐冲
            self.driver.find_element_by_id("com.tencent.mm:id/brn").click()
            sleep(4)
            self.assertEqual(self.driver.find_element_by_id("com.tencent.mm:id/aa3").text, "[链接]我一直在用场景鹿和附近的伙伴们聊天，真的很方便，你也一起来吧~", "OK, [链接]我一直在用场景鹿和附近的伙伴们聊天，真的很方便，你也一起来吧~", "errorrrrrr, [链接]我一直在用场景鹿和附近的伙伴们聊天，真的很方便，你也一起来吧~")
            self.driver.find_element_by_id("com.tencent.mm:id/bnn").click()
            self.driver.find_element_by_id("com.tencent.mm:id/aa1").click()
        elif platform == "QQ":
            # QQ
            self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/qq_friend_min_layout").click()
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
            self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/qq_zone_min_layout").click()
            sleep(4)
            self.driver.find_element_by_id("com.tencent.mobileqq:id/ivTitleBtnRightText").click()
        elif platform == "微博新浪":
            # 微博新浪
            self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/sina_weibo_min_layout").click()
            sleep(4)
            self.assertEqual(self.driver.find_element_by_id("com.sina.weibo:id/edit_view").text, "想看看附近伙伴都在聊什么？快试试场景鹿吧！聊天社交很方便~", "OK, 想看看附近伙伴都在聊什么？快试试场景鹿吧！聊天社交很方便~", "errorrrrrr, 想看看附近伙伴都在聊什么？快试试场景鹿吧！聊天社交很方便~")
            self.driver.find_element_by_id("com.sina.weibo:id/titleSave").click()  # 发送
        else:
            print "Errorrrrrr, 分享的渠道不存在！"




    # 功能点
    def drv_func(self):
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
    def addFriend(self, userA, userB):
        # 加好友，验证红点，删除好友
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)

        # 创建新用户userB 并获取小鹿号
        self.jumpLogin()
        varUserBXLH = self.loginPhone(userB, u"约翰福音" + str(randomDigits(3)), "男")
        self.jumpLogin()
        print "手机号 "+ userB + "已登出"

        # 用户userA登录
        self.loginPhone(userA, "", "")
        varUserAName = self.driver.find_element_by_id("com.mowin.scenesdeer:id/name").text

        # 进入通讯录加好友
        print "=> 点击通讯录"
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/address_book").click()

        # self.sendErrLog(u'addFriend', u'我 - 点击通讯录后报错')
        # 点击新的朋友 - 搜索小鹿号
        print "=> 点击新的朋友"
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/new_friend").click()

        # self.sendErrLog(u'addFriend', u'我 - 通讯录 - 点击新的朋友后报错')
        print "=> 点击搜索小鹿号"
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/status_bar").click()

        print "=> 输入" + str(userB) + "小鹿号"
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/search_scene").send_keys(varUserBXLH)
        self.driver.keyevent(66)
        sleep(2)
        print "=> 点击搜索结果userB"
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/content_layout").click()
        # self.sendErrLog(u'addFriend', u'我 - 通讯录 - 新的朋友 - 搜索小鹿号 - 点击搜索结果后报错')
        print "=> 点击加好友"
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/actionButton").click()

        print "=> 点击发送"
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/actionBar").find_element_by_xpath("//android.widget.TextView[contains(@index,2)]").click()
        sleep(2)

        # 连续返回
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/back").click()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/back").click()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/back").click()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/back").click()
        # 点击设置，退出登录后返回到我页面
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/setting").click()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/switch_account_or_log_out").click()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/logout_login").click()
        sleep(2)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/positive").click()
        sleep(2)
        print "手机号 " + str(userA) + " 已登出"

        # 用户userB登录,并验证红点
        self.jumpLogin()
        self.loginPhone(userB, "", "")
        sleep(6)
        # self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/chatUnRedCount").is_displayed(),True, "私聊右上角红点可见", "errorrrrrr, 私聊右上角红点不可见")
        print "私聊右上角红点数 = " + self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/chatUnRedCount").text
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/chat_tab").click()
        # 私聊页 - 新的朋友
        newFriends = self.driver.find_elements_by_id(sheetMain.cell_value(1, 5)+":id/content_layout")
        for newfriend in newFriends:
            reddot = newfriend.find_element_by_id(sheetMain.cell_value(1, 5)+":id/red_dot").text
            nickname = newfriend.find_element_by_id(sheetMain.cell_value(1, 5)+":id/nick_name").text
            latestmsg = newfriend.find_element_by_id(sheetMain.cell_value(1, 5)+":id/latest_msg").text
            tmptime = newfriend.find_element_by_id(sheetMain.cell_value(1, 5)+":id/time").text
            print "私聊列表页, 红点数 = " + reddot + ", " + nickname + " , " + latestmsg + " , " + tmptime
            if nickname == "新的朋友":
                newfriend.click()
                break
        # 新的朋友 - 接受
        newFriendreces = self.driver.find_elements_by_id(sheetMain.cell_value(1, 5)+":id/content_layout")
        for newFriendrece in newFriendreces:
            nickname = newFriendrece.find_element_by_id(sheetMain.cell_value(1, 5)+":id/nick_name").text
            latestmsg = newFriendrece.find_element_by_id(sheetMain.cell_value(1, 5)+":id/msg").text
            tmpaccept = newFriendrece.find_element_by_id(sheetMain.cell_value(1, 5)+":id/accept").text
            print "新的朋友列表页, " + nickname + " , " + latestmsg + " , " + tmpaccept
            if nickname == varUserAName and tmpaccept == "接受":
                print "=> 点击接受"
                newFriendrece.find_element_by_id(sheetMain.cell_value(1, 5)+":id/accept").click()
                sleep(2)
                print "显示 " + newFriendrece.find_element_by_id(sheetMain.cell_value(1, 5)+":id/hint").text
                break
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/back").click()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()
        # 点击设置，退出登录后返回到我页面
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/setting").click()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/switch_account_or_log_out").click()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/logout_login").click()
        sleep(2)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/positive").click()
        sleep(2)


        # 用户userA登录,并验证红点
        self.jumpLogin()
        self.loginPhone(userA, "", "")
        sleep(6)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/chatUnRedCount").is_displayed(),True, "私聊右上角红点可见", "errorrrrrr, 私聊右上角红点不可见")
        print "红点数 = " + self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/chatUnRedCount").text
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/chat_tab").click()
        # 私聊页 - 新的朋友
        newFriends = self.driver.find_elements_by_id(sheetMain.cell_value(1, 5)+":id/content_layout")
        for newfriend in newFriends:
            reddot = newfriend.find_element_by_id(sheetMain.cell_value(1, 5)+":id/red_dot").text
            nickname = newfriend.find_element_by_id(sheetMain.cell_value(1, 5)+":id/nick_name").text
            latestmsg = newfriend.find_element_by_id(sheetMain.cell_value(1, 5)+":id/latest_msg").text  # 谁的手已同意您的好友申请
            tmptime = newfriend.find_element_by_id(sheetMain.cell_value(1, 5)+":id/time").text
            print "红点数=" + reddot + ", " + nickname + " , " + latestmsg + " , " + tmptime
            if nickname == "新的朋友":
                newfriend.click()
                break
        # 新的朋友 - 接受
        newFriendreces = self.driver.find_elements_by_id(sheetMain.cell_value(1, 5)+":id/content_layout")
        for newFriendrece in newFriendreces:
            nickname = newFriendrece.find_element_by_id(sheetMain.cell_value(1, 5)+":id/nick_name").text
            latestmsg = newFriendrece.find_element_by_id(sheetMain.cell_value(1, 5)+":id/msg").text
            tmphint = newFriendrece.find_element_by_id(sheetMain.cell_value(1, 5)+":id/hint").text
            print "OK ," + nickname + " , " + latestmsg + " , " + tmpaccept
            if nickname == varUserAName and tmphint == "已添加":
                break
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/back").click()



    # 我
    def drv_me(self):
        self.TestcaseModule()
    def jumpLogin(self):
        # print ">" * 150
        # print sheetTestCase.cell_value(self.l, 4)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()  # 点击我
        # self.sendErrLog(u'jumpLogin', u'附近场景 - 点击我后报错')
        sleep(3)
        # 判断是否登录，未登录则点击登录
        # 判断二维码btn是否存在，存在则表示已登录，反之则反
        if self.getElementExist(sheetMain.cell_value(1, 5)+":id/qr_code") == True :
            # 已登录, 点击设置，退出登录后返回到我页面
            self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/setting").click()
            # self.sendErrLog(u'jumpLogin', u'我 - 点击设置后报错')
            self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/switch_account_or_log_out").click()
            # self.sendErrLog(u'jumpLogin', u'我 - 设置 - 点击切换账号或退出登录后报错')
            self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/logout_login").click()
            # self.sendErrLog(u'jumpLogin', u'我 - 设置 - 切换账号或退出登录 - 点击退出登录后报错')
            self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/positive").click()
            # self.sendErrLog(u'jumpLogin', u'我 - 设置 - 切换账号或退出登录 - 退出登录 - 点击确定后报错')
            sleep(2)
        # self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/no_data_layout").find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text ,"点击登录", "OK, 点击登录", "errorrrrrr, 点击登录")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/no_data_layout").click()
        # self.sendErrLog(u'jumpLogin', u'我 - 点击点击登录后报错')


    def loginElement(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        # 无密码快捷登录,页面元素检查
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "无密码快捷登录", "OK, 无密码快捷登录", "errorrrrrr, 无密码快捷登录")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/phoneNumber").clear()
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/phoneNumber").text, "请输入手机号码", "OK, 请输入手机号码", "errorrrrrr, 请输入手机号码")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/getMobileCode").text, "获取验证码", "OK, 获取验证码", "errorrrrrr, 获取验证码")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/mobileCode").text, "请输入验证码", "OK, 请输入验证码", "errorrrrrr, 请输入验证码")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/login").text, "手机号登录", "OK, 手机号登录", "errorrrrrr, 手机号登录")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/userAgreementCheckBox").text, "我同意", "OK, 我同意", "errorrrrrr, 我同意")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/userAgreement").text, "《场景鹿用户协议》", "OK, 《场景鹿用户协议》", "errorrrrrr, 《场景鹿用户协议》")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/otherAccountLoginLayout").find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, "第三方账户登录", "OK, 第三方账户登录" , "errorrrrrr, 第三方账户登录")
        # 微信
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/weixinLogin").is_displayed(), True, "OK, 微信btn", "errorrrrrr, 微信btn")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/contentParentLayout").find_element_by_xpath("//android.widget.RelativeLayout/child::android.widget.LinearLayout/child::android.widget.RelativeLayout[1]/android.widget.TextView[contains(@index,1)]").text, "微信", "OK, 微信", "errorrrrrr, 微信")
        # QQ
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/qqLogin").is_displayed(), True, "OK, QQbtn", "errorrrrrr, QQbtn")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/contentParentLayout").find_element_by_xpath("//android.widget.RelativeLayout/child::android.widget.LinearLayout/child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,1)]").text, "QQ", "OK, QQ", "errorrrrrr, QQ")
        # 微博
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/weiboLogin").is_displayed(), True, "OK, 微博btn", "errorrrrrr, 微博btn")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/contentParentLayout").find_element_by_xpath("//android.widget.RelativeLayout/child::android.widget.LinearLayout/child::android.widget.RelativeLayout[3]/android.widget.TextView[contains(@index,1)]").text, "微博", "OK, 微博", "errorrrrrr, 微博")

    def loginPhone(self, userPhone, userNickname, userSex):
        # varXLH = self.loginPhone(userB, u"约翰福音" + str(randomDigits(3)), "男")
        # ? 从数据库中获取最大的手机号并+1 ，确保每次登录的手机号是最新的。（未做）
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/phoneNumber").send_keys(int(userPhone))
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/getMobileCode").click()
        sleep(2)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/mobileCode").send_keys(getCJLverifyCode(int(userPhone)))
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/login").click()
        sleep(3)

        # 如果是新用户，需进行完善个人资料
        if self.getElementExist(sheetMain.cell_value(1, 5)+":id/title") == True:
            if self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text == "完善个人资料":
                # 完善个人资料 - 上传头像
                self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/headPic").click()
                self.camera("从手机相册选择",5)

                # 昵称、性别
                self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/remark").send_keys(userNickname)
                if userSex == "男":self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/male").click()  # 男
                else:self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/female").click()  # 女
                self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/complete").click()  # 完成（返回我页面）
                sleep(3)
                varXLH = self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/small_deer_number").text
                varXLH = varXLH.replace("小鹿号：", "")
                print "手机号 " + str(int(userPhone)) + "("+self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/name").text+")创建成功, 小鹿号=" + str(varXLH)
            else:
                print "errorrrrrr, loginPhone, 完善个人资料 <> " + self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text
        elif self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/status_bar").find_element_by_xpath("//android.widget.TextView[contains(@index,0)]").text == "我":
            varXLH = self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/small_deer_number").text
            varXLH = varXLH.replace("小鹿号：", "")
            print "手机号 " + str(int(userPhone)) + "("+self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/name").text+")登录成功, 小鹿号=" + str(varXLH)
        # 返回小鹿号
        return varXLH

    def loginWeixin(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.jumpLogin()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/weixinLogin").click()  # 点击微信
        # 微信登录流程
        self.sendErrLog(u'loginWeixin', u'无密码快捷登录 - 点击微信btn后报错')
        sleep(6)
        # 微信页，点击 确认登录，登录后跳转到我页面
        self.driver.swipe(self.screenX/2, 1200, self.screenX/2, 1200, 500)  # XT1085
        sleep(8)
        if self.getElementExist(sheetMain.cell_value(1, 5)+":id/name") == True:
            print "OK, 微信("+self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/name").text+")登录成功"
        else:
            self.sendErrLog(u'loginWeixin', u'我 - 用户昵称定位报错')
        # 设置，切换账号／退出登录，检查微信账号是否存在，并打勾，最后退出登录
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/setting").click()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/switch_account_or_log_out").click()
        varExits = self.driver.find_elements_by_id(sheetMain.cell_value(1, 5)+":id/content_layout")
        for varExit in varExits:
            ElementStatus = False
            try:
                varExit.find_element_by_id(sheetMain.cell_value(1, 5)+":id/checked")
                ElementStatus = True
            except :
                ElementStatus = False
            if ElementStatus == True:
                print "切换登录账号 => " + varExit.find_element_by_id(sheetMain.cell_value(1, 5)+":id/nick_name").text + "(" + varExit.find_element_by_id(sheetMain.cell_value(1, 5)+":id/account_source").text + "),已打勾"
            else:
                print "切换登录账号 => " + varExit.find_element_by_id(sheetMain.cell_value(1, 5)+":id/nick_name").text + "(" + varExit.find_element_by_id(sheetMain.cell_value(1, 5)+":id/account_source").text + ")"
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/logout_login").click()
        self.sendErrLog(u'loginWeixin', u'我 - 设置 - 切换账号或退出登录 - 点击退出登录后报错')
        sleep(2)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/positive").click()
        self.sendErrLog(u'loginWeixin', u'我 - 设置 - 切换账号或退出登录 - 退出登录 - 点击确定后报错')
        print "OK, 退出微信"

    def loginQQ(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        sleep(3)
        self.jumpLogin()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/qqLogin").click()  # 点击QQ
        # QQ登录流程
        self.sendErrLog(u'loginQQ', u'无密码快捷登录 - 点击QQbtn后报错')
        sleep(6)
        if self.getElementExist("com.tencent.mobileqq:id/name") == True:
            # QQ页，点击登录，登录后跳转到我页面
            self.driver.find_element_by_id("com.tencent.mobileqq:id/name").click()  # 点击登录 (QQ账号登录过，如霹雳火烛)
        # 否则可能QQ已经授权过，直接登录并跳转到我页面
        sleep(8)
        if self.getElementExist(sheetMain.cell_value(1, 5)+":id/name") == True:
            print "OK, QQ("+self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/name").text+")登录成功"
        else:
            self.sendErrLog(u'loginQQ', u'我 - 用户昵称定位报错')
        # 设置，切换账号／退出登录，检查微信账号是否存在，并打勾，最后退出登录
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/setting").click()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/switch_account_or_log_out").click()
        varExits = self.driver.find_elements_by_id(sheetMain.cell_value(1, 5)+":id/content_layout")
        for varExit in varExits:
            ElementStatus = False
            try:
                varExit.find_element_by_id(sheetMain.cell_value(1, 5)+":id/checked")
                ElementStatus = True
            except :
                ElementStatus = False
            if ElementStatus == True:
                print "切换登录账号 => " + varExit.find_element_by_id(sheetMain.cell_value(1, 5)+":id/nick_name").text + "(" + varExit.find_element_by_id(sheetMain.cell_value(1, 5)+":id/account_source").text + "),已打勾"
            else:
                print "切换登录账号 => " + varExit.find_element_by_id(sheetMain.cell_value(1, 5)+":id/nick_name").text + "(" + varExit.find_element_by_id(sheetMain.cell_value(1, 5)+":id/account_source").text +")"
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/logout_login").click()
        self.sendErrLog(u'loginQQ', u'我 - 设置 - 切换账号或退出登录 - 点击退出登录后报错')
        sleep(2)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/positive").click()
        self.sendErrLog(u'loginQQ', u'我 - 设置 - 切换账号或退出登录 - 退出登录 - 点击确定后报错')
        print "OK, 退出QQ"

    def loginWeibo(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        sleep(3)
        self.jumpLogin()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/weiboLogin").click()  # 点击微博
        # 微博流程
        self.sendErrLog(u'loginWeibo', u'无密码快捷登录 - 点击微博btn后报错')

        sleep(6)
        # 微博页，点击确定，登录后跳转到我页面
        self.driver.find_element_by_id("com.sina.weibo:id/bnLogin").click()  # 点击确定 （微博号：猴子_001）
        sleep(8)
        if self.getElementExist(sheetMain.cell_value(1, 5)+":id/name") == True:
            print "OK, 微博("+self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/name").text+")登录成功"
        else:
            self.sendErrLog(u'loginWeibo', u'我 - 用户昵称定位报错')
        # 设置，切换账号／退出登录，检查微信账号是否存在，并打勾，最后退出登录
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/setting").click()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/switch_account_or_log_out").click()
        varExits = self.driver.find_elements_by_id(sheetMain.cell_value(1, 5)+":id/content_layout")
        for varExit in varExits:
            ElementStatus = False
            try:
                varExit.find_element_by_id(sheetMain.cell_value(1, 5)+":id/checked")
                ElementStatus = True
            except :
                ElementStatus = False
            if ElementStatus == True:
                print "切换登录账号 => " + varExit.find_element_by_id(sheetMain.cell_value(1, 5)+":id/nick_name").text + "(" + varExit.find_element_by_id(sheetMain.cell_value(1, 5)+":id/account_source").text + "),已打勾"
            else:
                print "切换登录账号 => " + varExit.find_element_by_id(sheetMain.cell_value(1, 5)+":id/nick_name").text + "(" + varExit.find_element_by_id(sheetMain.cell_value(1, 5)+":id/account_source").text +")"
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/logout_login").click()
        self.sendErrLog(u'loginWeibo', u'我 - 设置 - 切换账号或退出登录 - 点击退出登录后报错')
        sleep(2)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/positive").click()
        self.sendErrLog(u'loginWeibo', u'我 - 设置 - 切换账号或退出登录 - 退出登录 - 点击确定后报错')
        print "OK, 退出微博"
        sleep(3)

    def loginInfoElement(self, newPhone):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.jumpLogin()
        self.loginPhone(newPhone)
        # 完善个人资料，页面元素
        sleep(3)

        # 新用户第一次登录后才会进入 完善个人资料
        if self.getElementExist(sheetMain.cell_value(1, 5)+":id/title") == True:
            if self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text == "完善个人资料":
                # 检查返回
                self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/back").is_displayed(), True, "OK, 返回键", "errorrrrrr, 返回键")

                # 0=上传头像 , 1=昵称 , 2=输入昵称 , 3=我是帅哥 , 4=我是美女 ，
                for i in range(0, 5):
                    (a, b) = self.assertSplit(self.str_list[i])
                    self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)

                self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/contentLayout").find_element_by_xpath("//android.widget.TextView[contains(@index,8)]").text, self.str_list[5], "OK, " + self.str_list[5], "errorrrrrr, " + self.str_list[5])

                # 点击 拍照机，检查文案"拍照、从手机相册选择、取消"
                self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/headPic").click()  # 上传头像
                sleep(4)
                self.camera("从手机相册选择",5)
                sleep(3)

                # 侦探{手机号尾4位}
                self.varnickname = sheetMain.cell_value(1, 6) + str(int(sheetMain.cell_value(1, 7)))[-4:]
                self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/remark").send_keys(self.varnickname)  # 输入昵称
                sleep(2)
                self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/male").click()  # 选择性别,男
                self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/complete").click()  # 完成
                sleep(3)
            else:
                print "warning, 完善个人资料页不存在, 请检查手机号是否是新的！！！"
        else:
            self.sendErrLog(u'loginInfoElement', u'我 - 完善个人资料不存在报错')
        sleep(2)

    def meElement(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()
        sleep(4)
        # 我
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/status_bar").find_element_by_xpath("//android.widget.TextView[contains(@index,0)]").text, "我", "OK, 我", "errorrrrrr, 我")
        # 扫一扫
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/menu").is_displayed(), True, "OK, 扫一扫", "errorrrrrr, 扫一扫")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/menu").click()
        # 头像
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/head_icon").is_displayed(), True, "OK, 头像", "errorrrrrr, 头像")
        # 昵称
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/name").text, self.varnickname, "OK, 昵称", "errorrrrrr, 昵称 ," + self.varnickname + "<>" + self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/name").text)
        # 性别
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/gender").is_displayed(), True, "OK, 性别", "errorrrrrr, 性别")
        # 小鹿号，只检查文案+数字个数 (小鹿号：2016122710030)
        varDeernumber = self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/small_deer_number").text
        varDeernumber = varDeernumber.replace("：", ":")
        x = varDeernumber.split(":")
        if x[0] == "小鹿号" and len(x[1]) == 13:
            print "OK, " + varDeernumber
        else:
            print "errorrrrrr, " + varDeernumber
        self.meXiaoluhao = x[1]
        # 个人签名
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/sign").text, "个性签名：", "OK, 个性签名", "errorrrrrr, 个性签名错误 , 个性签名： <>" + self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/sign").text)
        # 二维码
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/qr_code").is_displayed(), True, "OK, 二维码", "errorrrrrr, 二维码")

        # 0=通讯录 , 1=我建的场景 , 2=我的相册 , 3=我的足迹 , 4=分享[场景鹿]给好友 , 5=设置
        for i in range(0, 6):
            (a, b) = self.assertSplit(self.str_list[i])
            self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)

    def meInfo(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()
        sleep(3)

        # 先获取我页面中的小鹿号，(小鹿号：2016122710030)
        meXIAOLUHAO = self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/small_deer_number").text
        # meXIAOLUHAO = "我的" + meXIAOLUHAO.replace("：", ":")

        #  点击个人信息
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/user_info_layout").click()
        self.sendErrLog(u'meInfo', u'我 - 点击个人信息后报错')
        sleep(3)
        # 标题 = 个人信息
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "个人信息", "OK, 个人信息" , "errorrrrrr, 个人信息")
        # 头像
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/head_icon_hint").text, "头像", "OK, 头像" , "errorrrrrr, 头像")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/head_icon").click()
        self.sendErrLog(u'meInfo', u'我 - 个人信息 - 点击头像后报错')
        sleep(6)
        self.camera("取消")
        # 昵称 (修改昵称为 科比abc)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/nickname_hint").text, "昵称", "OK, 昵称", "errorrrrrr, 昵称")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/nickname").click()
        self.sendErrLog(u'meInfo', u'我 - 个人信息 - 点击昵称后报错')
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/title").text, "更改昵称", "OK, 更改昵称", "errorrrrrr, 更改昵称")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/content").clear()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/content").send_keys(u"科比abc")
        sleep(2)
        el3 =self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/actionBar").find_element_by_xpath("//android.widget.TextView[contains(@index,2)]")
        self.assertEqual(el3.text, "保存", "OK, 保存" , "errorrrrrr, 保存")
        el3.click()
        self.sendErrLog(u'meInfo', u'我 - 个人信息 - 修改昵称保存后报错')
        sleep(2)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/nickname").text, "科比abc", "OK, 修改昵称后显示", "errorrrrrr, 修改昵称后显示")

        # 小鹿号
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/small_deer_number_hint").text, "小鹿号", "OK, 小鹿号", "errorrrrrr, 小鹿号")
        infoXIAOLUHAO = self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/small_deer_number").text

        # 登录账号 及 小icon
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/account_number_hint").text, "登录账号", "OK, 登录账号" , "errorrrrrr, 登录账号")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/account_number").is_displayed(), True, "OK, 登录账号第三方头像", "errorrrrrr, 登录账号第三方头像")

        # 性别 (修改昵称为 女)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/sex_hint").text, "性别", "OK, 性别", "errorrrrrr, 性别")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/sex").text, "男", "OK, 男", "errorrrrrr, 男")

        # 地区 及值
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/district_hint").text, "地区", "OK, 地区", "errorrrrrr, 地区")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/district").click()
        self.sendErrLog(u'meInfo', u'我 - 个人信息 - 修改地区后报错')
        sleep(2)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "选择地区", "OK, 标题选择地区第一层", "errorrrrrr, 标题选择地区第一层")
        districts = self.driver.find_elements_by_id(sheetMain.cell_value(1, 5)+":id/district")
        for district in districts:
            if district.text == "上海市":
                district.click()
                self.sendErrLog(u'meInfo', u'我 - 个人信息 - 修改地区选择上海市 后报错')
                sleep(2)
                self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "选择地区", "OK, 标题选择地区第二层", "errorrrrrr, 标题选择地区第二层")
                districts2 = self.driver.find_elements_by_id(sheetMain.cell_value(1, 5)+":id/district")
                for district2 in districts2:
                    if district2.text == "上海市":
                        district2.click()
                        self.sendErrLog(u'meInfo', u'我 - 个人信息 - 修改地区选择上海市 上海市后报错')
                        break
                break
        sleep(3)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/district").text, u"上海市  上海市", "OK, 上海市  上海市", "errorrrrrr, 上海市  上海市")

        # 个人签名 (修改为 weibo)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/personal_sign_hint").text, "个人签名", "OK, 个人签名", "errorrrrrr, 个人签名")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/personal_sign").click()
        sleep(2)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/title").text, "更改个人签名", "OK, 更改个人签名", "errorrrrrr, 更改个人签名")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/content").clear()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/content").send_keys(u"weibo")
        sleep(2)
        el3 = self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/actionBar").find_element_by_xpath("//android.widget.TextView[contains(@index,2)]")
        self.assertEqual(el3.text, "保存", "OK, 保存" , "errorrrrrr, 保存")
        el3.click()
        self.sendErrLog(u'meInfo', u'我 - 个人信息 - 修改个人签名后报错')
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/personal_sign").text, "weibo", "OK, 修改个人签名后显示", "errorrrrrr, 修改个人签名后显示")

        # 返回
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()
        self.sendErrLog(u'meInfo', u'我 - 个人信息 - 点击返回后报错')

        # 验证小鹿号
        self.assertEqual(u"小鹿号：" + infoXIAOLUHAO, meXIAOLUHAO, "OK, 小鹿号码内外比较", "errorrrrrr, 小鹿号码内外比较")

    def meAddresslist(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()
        sleep(2)

        # 获取小鹿号
        meXIAOLUHAO = self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/small_deer_number").text

        # 点击通讯录，
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/address_book").click()
        self.sendErrLog(u'meAddresslist', u'我 - 点击通讯录后报错')

        self.assertContain("通讯录",self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text,"OK, 标题包含通讯录", "errorrrrrr, 标题包含通讯录")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/status_bar").is_displayed(), True, "OK, 搜索框", "errorrrrrr, 搜索框")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/search").text, "搜索", "OK, 搜索文字","errorrrrrr, 搜索文字")

        # 点击新的朋友
        (a, b) = self.assertSplit(self.str_list[0])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).click()
        self.sendErrLog(u'meAddresslist', u'我 - 通讯录 - 点击新的朋友后报错')
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, b, "OK, 标题=" + b, "errorrrrrr, 标题=" + b)

        # 新的朋友 - 点击扫一扫
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/actionBar").find_element_by_xpath("//android.widget.ImageView[contains(@index,2)]").is_displayed(), True, "OK, 扫一扫", "errorrrrrr, 扫一扫")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/actionBar").find_element_by_xpath("//android.widget.ImageView[contains(@index,2)]").click()
        self.sendErrLog(u'meAddresslist', u'我 - 通讯录 - 新的朋友 - 点击扫一扫后报错')
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/back").click()
        # self.driver.keyevent(67)  # 退格键

        # 新的朋友 - 详情页各元素
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/status_bar").is_displayed(), True, "OK, 搜索框", "errorrrrrr, 搜索框")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/search").text, "搜索小鹿号", "OK, 搜索小鹿号文字", "errorrrrrr, 搜索小鹿号文字")
        newfrdXIAOLUHAO = "我的" + meXIAOLUHAO.replace("：", ":")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/my_small_deer_number").text, newfrdXIAOLUHAO, "OK, " + newfrdXIAOLUHAO, "errorrrrrr, " + newfrdXIAOLUHAO)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/qr_code").is_displayed(), True, "OK, 二维码", "errorrrrrr, 二维码")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/add_phone_contacts").text, "添加手机联系人", "OK, 添加手机联系人", "errorrrrrr, 添加手机联系人")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/add_weixin_friend").text, "添加微信好友", "OK, 添加微信好友", "errorrrrrr, 添加微信好友")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/add_qq_friend").text, "添加QQ好友", "OK, 添加QQ好友", "errorrrrrr, 添加QQ好友")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/no_data_icon").is_displayed(), True, "OK, 背景鹿头", "errorrrrrr, 背景鹿头")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/no_data_hint").text, "没有新的好友邀请信息", "OK, 没有新的好友邀请信息", "errorrrrrr, 没有新的好友邀请信息")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()

        # 分组标签
        (a, b) = self.assertSplit(self.str_list[1])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).click()
        self.sendErrLog(u'meAddresslist', u'我 - 通讯录 - 点击分组标签后报错')

        sleep(2)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, b, "OK, 标题=" +b , "errorrrrrr, 标题=" +b)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/add_label").find_element_by_xpath("//android.widget.ImageButton[contains(@index,0)]").is_displayed(), True, "OK, 分组标签前+符号", "errorrrrrr, 分组标签前+符号")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/add_label").find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, "新建标签", "OK, 新建标签", "errorrrrrr, 新建标签")

        # 点击新建标签
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/add_label").find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").click()
        self.sendErrLog(u'meAddresslist', u'我 - 通讯录 - 分组标签 - 点击新建标签后报错')
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "新建标签", "OK, 标题=新建标签" , "errorrrrrr, 标题=新建标签")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/textView2").text, "标签名字", "OK, 标签名字" , "errorrrrrr, 标签名字")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/label_name").text, "设置标签名字", "OK, 设置标签名字" , "errorrrrrr, 设置标签名字")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/label_name").send_keys(u"朋友的家")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/tag_user_num").text, "标签成员", "OK, 标签成员" , "errorrrrrr, 标签成员")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/add_icon").is_displayed(), True, "OK, 添加成员前+符号" , "errorrrrrr, 添加成员前+符号")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/add_member").find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, "添加成员", "OK, 添加成员", "errorrrrrr, 添加成员")

        # 点击添加成员 （必须要有联系人 或 场景）
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/add_member").find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").click()
        self.sendErrLog(u'meAddresslist', u'我 - 通讯录 - 分组标签 - 点击添加成员后报错')
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "选择联系人", "OK, 标题=选择联系人" , "errorrrrrr, 标题=选择联系人")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/status_bar").is_displayed(), True, "OK, 搜索框", "errorrrrrr, 搜索框")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/search").text, "搜索", "OK, 搜索", "errorrrrrr, 搜索")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/import_from_the_scene").text, "从场景里面导入", "OK, 从场景里面导入", "errorrrrrr, 从场景里面导入")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/letter_list").is_displayed(),True , "OK, 字母A-Z", "errorrrrrr, 字母A-Z")
        # 点击 从场景里面导入
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/import_from_the_scene").click()
        self.sendErrLog(u'meAddresslist', u'我 - 通讯录 - 分组标签 - 添加成员 - 点击从场景里面导入后报错')
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "选择场景", "OK, 标题=选择场景" , "errorrrrrr, 标题=选择场景")
        # ？？(暂无内容，从选择场景返回到通讯录共4次返回)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()

        # 通讯录 - 字母列表
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/letter_list").is_displayed(), True, "OK, 字母列表", "errorrrrrr, 字母列表")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()
        sleep(2)

    def meMyscene(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()
        sleep(2)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/my_scene").click()
        self.sendErrLog(u'meMyscene', u'我 - 点击我建的场景后报错')

        (a, b) = self.assertSplit(self.str_list[0])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/no_data_icon").is_displayed(), True, "OK, 背景鹿头", "errorrrrrr, 背景鹿头")
        (a, b) = self.assertSplit(self.str_list[1])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()
        sleep(2)
    def meMyalbum(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()
        sleep(2)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/my_photo_album").click()
        self.sendErrLog(u'meMyscene', u'我 - 点击我的相册后报错')
        (a, b) = self.assertSplit(self.str_list[0])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/no_data_icon").is_displayed(), True, "OK, 背景鹿头", "errorrrrrr, 背景鹿头")
        (a, b) = self.assertSplit(self.str_list[1])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()
        sleep(2)
    def meMyfoot(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()
        sleep(2)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/my_footprint").click()
        self.sendErrLog(u'meMyscene', u'我 - 点击我的足迹后报错')
        (a, b) = self.assertSplit(self.str_list[0])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/no_data_icon").is_displayed(), True, "OK, 背景鹿头", "errorrrrrr, 背景鹿头")
        (a, b) = self.assertSplit(self.str_list[1])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()
        sleep(2)
    def meShare(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        # C3-7,我 - 分享[场景鹿]给好友(朋友圈、微信好友、QQ、QQ空间、新浪微博)"
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()
        sleep(2)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/share_the_app_with_friend").click()
        self.sendErrLog(u'meMyscene', u'我 - 点击分享[场景鹿]给好友后报错')

        (a, b) = self.assertSplit(self.str_list[0])
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/time_line_min_icon").is_displayed(), True, "OK, " + b + "icon", "errorrrrrr, " + b + "icon")
        self.assertEqual(self.driver.find_element_by_id(a).find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, b, "OK, " + b, "errorrrrrr, " + b)
        (a, b) = self.assertSplit(self.str_list[1])
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/wx_session_min_icon").is_displayed(), True, "OK, " + b + "icon", "errorrrrrr, " + b + "icon")
        self.assertEqual(self.driver.find_element_by_id(a).find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, b, "OK, " + b, "errorrrrrr, " + b)
        (a, b) = self.assertSplit(self.str_list[2])
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/qq_friend_min_icon").is_displayed(), True, "OK, " + b + "icon", "errorrrrrr, " + b + "icon")
        self.assertEqual(self.driver.find_element_by_id(a).find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, b, "OK, " + b, "errorrrrrr, " + b)
        (a, b) = self.assertSplit(self.str_list[3])
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/qq_zone_min_icon").is_displayed(), True, "OK, " + b + "icon", "errorrrrrr, " + b + "icon")
        self.assertEqual(self.driver.find_element_by_id(a).find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, b, "OK, " + b, "errorrrrrr, " + b)
        (a, b) = self.assertSplit(self.str_list[4])
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/sina_weibo_min_icon").is_displayed(), True, "OK, " + b + "icon", "errorrrrrr, " + b + "icon")
        self.assertEqual(self.driver.find_element_by_id(a).find_element_by_xpath("//android.widget.TextView[contains(@index,1)]").text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/cancel").click()
        sleep(2)
    def meSetting(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/me_tab").click()
        sleep(2)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/setting").click()
        self.sendErrLog(u'meMyscene', u'我 - 点击设置后报错')

        # 设置
        (a, b) = self.assertSplit(self.str_list[0])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)

        # 新消息通知
        (a, b) = self.assertSplit(self.str_list[1])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).click()
        self.sendErrLog(u'meSetting', u'我 - 设置 - 点击新消息通知后报错')
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "新消息通知", "OK, 新消息通知", "errorrrrrr, 新消息通知")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/contentParentLayout").find_element_by_xpath("//android.widget.LinearLayout/child::android.widget.RelativeLayout[1]/android.widget.TextView[contains(@index,0)]").text, "接收新消息通知", "OK, 接收新消息通知", "errorrrrrr, 接收新消息通知")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/receive_new_message_alerts").get_attribute("checked"), "true", "OK, 接收新消息通知(打开)", "errorrrrrr, 接收新消息通知(打开)")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/contentParentLayout").find_element_by_xpath("//android.widget.LinearLayout/child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,0)]").text, "通知显示消息详情", "OK, 通知显示消息详情", "errorrrrrr, 通知显示消息详情")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/notice_shows_the_details").get_attribute("checked"), "true", "OK, 通知显示消息详情(打开)", "errorrrrrr, 通知显示消息详情(打开)")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/contentParentLayout").find_element_by_xpath("//android.widget.LinearLayout/android.widget.TextView[contains(@index,3)]").text, "若关闭，当收到聊天新消息时，将不再显示发送人和消息内容", "OK, 若关闭，当收到聊天新消息时，将不再显示发送人和消息内容", "errorrrrrr, 若关闭，当收到聊天新消息时，将不再显示发送人和消息内容")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/contentParentLayout").find_element_by_xpath("//android.widget.LinearLayout/child::android.widget.RelativeLayout[3]/android.widget.TextView[contains(@index,0)]").text, "声音", "OK, 声音", "errorrrrrr, 声音")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/sound").get_attribute("checked"), "true", "OK, 声音(打开)", "errorrrrrr, 声音(打开)")
        # 开关打开功能。
        # self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/sound").click()
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/contentParentLayout").find_element_by_xpath("//android.widget.LinearLayout/child::android.widget.RelativeLayout[4]/android.widget.TextView[contains(@index,0)]").text, "振动", "OK, 振动", "errorrrrrr, 振动")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/vibrate").get_attribute("checked"), "true", "OK, 振动(打开)", "errorrrrrr, 振动(打开)")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()

        # 勿扰模式
        (a, b) = self.assertSplit(self.str_list[2])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).click()
        self.sendErrLog(u'meSetting', u'我 - 设置 - 点击勿扰模式后报错')
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "勿扰模式", "OK, 勿扰模式", "errorrrrrr, 勿扰模式")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/contentParentLayout").find_element_by_xpath("//android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.TextView[contains(@index,0)]").text, "勿扰模式", "OK, 勿扰模式", "errorrrrrr, 勿扰模式")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/no_disturb_pattern").get_attribute("checked"), "false", "OK, 勿扰模式(关闭)", "errorrrrrr, 勿扰模式(关闭)")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/contentParentLayout").find_element_by_xpath("//android.widget.LinearLayout/android.widget.TextView[contains(@index,1)]").text, "开启后在设定时间段内收到新消息时不会响铃或振动", "OK, 开启后在设定时间段内收到新消息时不会响铃或振动", "errorrrrrr, 开启后在设定时间段内收到新消息时不会响铃或振动")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()

        # 隐私
        (a, b) = self.assertSplit(self.str_list[3])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).click()
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "隐私", "OK, 隐私", "errorrrrrr, 隐私")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/contentParentLayout").find_element_by_xpath("//android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.TextView[contains(@index,0)]").text, "加我为好友时需要验证", "OK, 加我为好友时需要验证", "errorrrrrr, 加我为好友时需要验证")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/verify").get_attribute("checked"), "true", "OK, 加我为好友时需要验证(打开)", "errorrrrrr, 加我为好友时需要验证(打开)")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/black_list").text, "黑名单", "OK, 黑名单", "errorrrrrr, 黑名单")
        # 隐私 - 黑名单
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/black_list").click()
        self.sendErrLog(u'meSetting', u'我 - 设置 - 隐私 - 点击黑名单后报错')
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "黑名单", "OK, 黑名单", "errorrrrrr, 黑名单")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/no_black_list_bg").is_displayed(), True, "OK, 背景长颈鹿", "errorrrrrr, 背景长颈鹿")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/black_list_is_empty").text, "黑名单为空", "OK, 黑名单为空", "errorrrrrr, 黑名单为空")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/no_black_list_layout").find_element_by_xpath("//android.widget.TextView[contains(@index,2)]").text, "加入黑名单后，你将不再接收对方任何消息", "OK, 加入黑名单后，你将不再接收对方任何消息", "errorrrrrr, 加入黑名单后，你将不再接收对方任何消息")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()

        # 关于场景鹿
        (a, b) = self.assertSplit(self.str_list[4])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        # 关于场景鹿 - 场景鹿版本
        (a, b) = self.assertSplit(self.str_list[5])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).click()
        self.sendErrLog(u'meSetting', u'我 - 设置 - 点击关于场景鹿后报错')
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "关于场景鹿", "OK, 关于场景鹿", "errorrrrrr, 关于场景鹿")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/app_thumb").is_displayed(), True, "OK, 长颈鹿头像", "errorrrrrr, 长颈鹿头像")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/version").text, b, "OK, " + b, "errorrrrrr, " + b)

        # 关于场景鹿 - 功能介绍
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/function_introduction").text, "功能介绍", "OK, 功能介绍", "errorrrrrr, 功能介绍")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/function_introduction").click()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()
        self.sendErrLog(u'meSetting', u'我 - 设置 - 关于场景鹿 - 点击功能介绍后报错')

        # 关于场景鹿 - 意见反馈
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/suggestion_feedback").text, "意见反馈", "OK, 意见反馈", "errorrrrrr, 意见反馈")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/suggestion_feedback").click()
        self.sendErrLog(u'meSetting', u'我 - 设置 - 关于场景鹿 - 点击意见反馈后报错')
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "意见反馈", "OK, 意见反馈", "errorrrrrr, 意见反馈")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/contentParentLayout").find_element_by_xpath("//android.widget.LinearLayout/android.widget.TextView[contains(@index,0)]").text, "感谢你提出的宝贵意见和建议，你留下的每个字都将用来改善我们的产品。", "OK, 感谢你提出的宝贵意见和建议，你留下的每个字都将用来改善我们的产品。", "errorrrrrr, 感谢你提出的宝贵意见和建议，你留下的每个字都将用来改善我们的产品。")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/content").text, "用的不爽，说两句哦…", "OK, 用的不爽，说两句哦…", "errorrrrrr, 用的不爽，说两句哦…")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/content").send_keys(u"非常好用，分享朋友圈")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/actionBar").find_element_by_xpath("//android.widget.TextView[contains(@index,2)]").click()
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/suggestion_feedback").click()
        self.sendErrLog(u'meSetting', u'我 - 设置 - 关于场景鹿 - 意见反馈 - 点击提交后报错')
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()

        # 关于场景鹿 - 服务协议
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/service_agreement").text, "服务协议", "OK, 服务协议", "errorrrrrr, 服务协议")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/service_agreement").click()
        self.sendErrLog(u'meSetting', u'我 - 设置 - 关于场景鹿 - 点击服务协议后报错')
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "用户协议", "OK, 用户协议", "errorrrrrr, 用户协议")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()

        # 关于场景鹿 - 隐私政策
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/privacy_policy").text, "隐私政策", "OK, 隐私政策", "errorrrrrr, 隐私政策")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/privacy_policy").click()
        self.sendErrLog(u'meSetting', u'我 - 设置 - 关于场景鹿 - 点击隐私政策后报错')
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "隐私政策", "OK, 隐私政策", "errorrrrrr, 隐私政策")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()

        # 关于场景鹿 - 检查新版本 （？无法点击）
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/check_the_new_version").text, "检查新版本", "OK, 检查新版本", "errorrrrrr, 检查新版本")
        # self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/check_the_new_version").click()
        # self.sendErrLog(u'meSetting', u'我 - 设置 - 关于场景鹿 - 点击检查新版本后报错')

        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()

        # 清除缓存
        (a, b) = self.assertSplit(self.str_list[6])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).click()
        self.sendErrLog(u'meSetting', u'我 - 设置 - 点击清除缓存后报错')
        # 清除缓存 - 弹框
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "场景鹿", "OK, 场景鹿", "errorrrrrr, 场景鹿")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/content").text, "是否要清除缓存？", "OK, 是否要清除缓存？", "errorrrrrr, 是否要清除缓存？")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/negative").text, "取消", "OK, 取消", "errorrrrrr, 取消")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/positive").text, "清除", "OK, 清除", "errorrrrrr, 清除")
        # 清除缓存 - 弹框 - 点击清除
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/positive").click()
        self.sendErrLog(u'meSetting', u'我 - 设置 - 清除缓存 - 点击清除后报错')

        # 切换帐号或退出登录
        (a, b) = self.assertSplit(self.str_list[7])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).click()
        self.sendErrLog(u'meSetting', u'我 - 设置 - 点击切换帐号或退出登录后报错')
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "切换帐号/退出登录", "OK, 切换帐号/退出登录", "errorrrrrr, 切换帐号/退出登录")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/switch_account").text, "切换登录账号", "OK, 切换登录账号", "errorrrrrr, 切换登录账号")
        # 切换帐号或退出登录 - 点击退出登录（返回我页面）
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/logout_login").click()
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/content").text,"退出后不会删除任何历史数据，下次登录依然可以使用本账号。", "OK, 退出后不会删除任何历史数据，下次登录依然可以使用本账号。", "errorrrrrr, 退出后不会删除任何历史数据，下次登录依然可以使用本账号。")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/negative").text,"取消", "OK, 取消", "errorrrrrr, 取消")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/positive").text,"确定", "OK, 确定", "errorrrrrr, 确定")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/positive").click()
        self.sendErrLog(u'meSetting', u'我 - 设置 - 切换帐号或退出登录 - 点击退出登录确定后报错')

        # 我 - 点击登录
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/no_data_layout").click()
        sleep(2)
        self.loginPhone(sheetMain.cell_value(1, 7))


    # 附近场景
    def drv_near(self):
        self.TestcaseModule()
    def nearSceneType(self):
        # C4-1,检查附近场景分类
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.checkSceneType("附近场景","sheetArea", 2,sheetMain.cell_value(1, 5) + ":id/near_scenes_layout",sheetMain.cell_value(1, 5) + ":id/pop_listview_left",sheetMain.cell_value(1, 5) + ":id/pop_listview_right",sheetMain.cell_value(1, 5) + ":id/textView",0)
    def nearComSceneType(self):
        # C4-2,检查公共场景分类
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.driver.swipe(200, 100, 200, 100, 1000)
        sleep(2)
        self.checkSceneType("公共场景","sheetCom", 3,sheetMain.cell_value(1, 5) + ":id/all_scenes_layout",sheetMain.cell_value(1, 5) + ":id/pop_listview_left",sheetMain.cell_value(1, 5) + ":id/pop_listview_right",sheetMain.cell_value(1, 5) + ":id/textView",4)

        # self.checkSceneType("公共场景","sheetCom", 3,self.str_list[0],self.str_list[1],self.str_list[2],self.str_list[3],4)
    def nearSplitSceneType(self):
        # C4-3,检查分场景分类
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.driver.swipe(200, 100, 200, 100, 1000)
        sleep(2)
        self.checkSceneType("群组","sheetSplit", 4,sheetMain.cell_value(1, 5) + ":id/child_scenes_layout",sheetMain.cell_value(1, 5) + ":id/pop_listview_left",sheetMain.cell_value(1, 5) + ":id/pop_listview_right",sheetMain.cell_value(1, 5) + ":id/textView",1)

        # self.checkSceneType("群组","sheetSplit", 4,self.str_list[0],self.str_list[1],self.str_list[2],self.str_list[3],1)

    def nearElement(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.driver.swipe(200, 100, 200, 100, 1000)
        sleep(2)

        # 点击上海市，选择城市详情页
        (a, b) = self.assertSplit(self.str_list[0])
        self.assertEqual(self.driver.find_element_by_id(a).text[0:3], b, "OK, " + b , "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).click()
        self.sendErrLog(u'nearElement', u'附近场景 - 点击{城市}后报错')
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "选择城市", "OK, 选择城市" , "errorrrrrr, 选择城市")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/search").text, "输入城市名、拼音首字母", "OK, 输入城市名、拼音首字母" , "errorrrrrr, 输入城市名、拼音首字母")
        # GPS定位城市
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/gps_location_title").text, "GPS定位城市", "OK, GPS定位城市" , "errorrrrrr, GPS定位城市")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/gps_location").text, "上海市", "OK, 上海市" , "errorrrrrr, 上海市")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/hot_city_title").text, "热门城市", "OK, 热门城市" , "errorrrrrr, 热门城市")
        # 遍历3个热门城市
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/hot_city_list").find_element_by_xpath("//child::android.widget.RelativeLayout[1]/android.widget.TextView[contains(@index,0)]").text, "北京市", "OK, 北京市", "errorrrrrr, 北京市")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/hot_city_list").find_element_by_xpath("//child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,0)]").text, "天津市", "OK, 天津市", "errorrrrrr, 天津市")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/hot_city_list").find_element_by_xpath("//child::android.widget.RelativeLayout[3]/android.widget.TextView[contains(@index,0)]").text, "沈阳市", "OK, 沈阳市", "errorrrrrr, 沈阳市")
        # 点击北京市
        el4 = self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/hot_city_list").find_element_by_xpath("//child::android.widget.RelativeLayout[1]/android.widget.TextView[contains(@index,0)]")
        el4.click()
        self.sendErrLog(u'nearElement', u'选择城市 - 热门城市 - 点击北京市后报错')
        sleep(2)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/city").text[0:3], "北京市", "OK, 北京市" + b , "errorrrrrr, 北京市")

        # 搜索场景
        (a, b) = self.assertSplit(self.str_list[1])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b , "errorrrrrr, " + b)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/search_scene").click()
        self.sendErrLog(u'nearElement', u'附近场景 - 点击搜索框后报错')
        sleep(2)
        # 搜公共场景
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/search_scene").text, "输入公共场景名称、地点等", "OK, 输入公共场景名称、地点等" , "errorrrrrr, 输入公共场景名称、地点等")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/text1").text, "搜公共场景", "OK, 搜公共场景" , "errorrrrrr, 搜公共场景")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/public_classify").text, "公共场景", "OK, 公共场景" , "errorrrrrr, 公共场景")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/arrow").is_displayed(), True, "OK, 下箭头btn" , "errorrrrrr, 下箭头btn")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/search_history").text, "历史搜索", "OK, 历史搜索" , "errorrrrrr, 历史搜索")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/clear_search_recorder").text, "清空搜索记录", "OK, 清空搜索记录" , "errorrrrrr, 清空搜索记录")
        # 搜群组
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/text2").text, "搜群组", "OK, 搜群组" , "errorrrrrr, 搜群组")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/child_scene_layout").click()
        self.sendErrLog(u'nearElement', u'附近场景 - 搜索场景 - 点击搜群组后报错')
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/search_scene").text, "输入群组名称、地点等", "OK, 输入群组名称、地点等" , "errorrrrrr, 输入群组名称、地点等")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/public_classify").text, "群组", "OK, 群组" , "errorrrrrr, 群组")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/arrow").is_displayed(), True, "OK, 下箭头btn" , "errorrrrrr, 下箭头btn")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/search_history").text, "历史搜索", "OK, 历史搜索" , "errorrrrrr, 历史搜索")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/clear_search_recorder").text, "清空搜索记录", "OK, 清空搜索记录" , "errorrrrrr, 清空搜索记录")
        # 搜场景号
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/text3").text, "搜场景号", "OK, 搜场景号" , "errorrrrrr, 搜场景号")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/scenes_num_layout").click()
        self.sendErrLog(u'nearElement', u'附近场景 - 搜索场景 - 点击搜场景号后报错')
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/search_scene").text, "输入场景号", "OK, 输入场景号" , "errorrrrrr, 输入场景号")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/search_history").text, "历史搜索", "OK, 历史搜索" , "errorrrrrr, 历史搜索")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/clear_search_recorder").text, "清空搜索记录", "OK, 清空搜索记录" , "errorrrrrr, 清空搜索记录")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/back").click()
        sleep(2)

        # 附近场景,公共场景,群组
        for i in range(2, 5):
            (a, b) = self.assertSplit(self.str_list[3])
            self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b , "errorrrrrr, " + b)

        # 北京市公共场景头像，北京市文字，0人在场，0条足迹，欢迎加入场景一起交友聊天。
        # 北京市（暂时只有一个市信息）
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/scene_logo").is_displayed(), True, "OK, 北京市公共场景头像btn" , "errorrrrrr, 北京市公共场景头像btn")
        (a, b) = self.assertSplit(self.str_list[5])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b , "errorrrrrr, " + b)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/scene_name").text, "北京市", "OK, 北京市" , "errorrrrrr, 北京市")
        tmpPersonal = self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/personal_number").text
        self.assertContain("人在场",tmpPersonal, "OK, " + tmpPersonal , "errorrrrrr, " + tmpPersonal)
        tmpFootprint = self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/footprint_number").text
        self.assertContain("条足迹",tmpFootprint, "OK, " + tmpFootprint , "errorrrrrr, " + tmpFootprint)

        (a, b) = self.assertSplit(self.str_list[6])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b , "errorrrrrr, " + b)

        # 加号
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/add_scene").is_displayed(), True, "OK, 右上角加号btn", "errorrrrrr, 右上角加号btn")
        self.sendErrLog(u'nearElement', u'附近场景 - 点击右上角加号btn后报错')

    def nearCreateCom(self, comName):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.comName = comName
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/home_tab_hint").click()
        sleep(2)

        # 点击加号
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/add_scene").click()
        sleep(2)
        # 加号 -  创建公共场景（遍历）
        self.driver.swipe(self.screenX-100, 310, self.screenX-100, 310, 1000)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "创建公共场景", "OK, 创建公共场景", "errorrrrrr, 创建公共场景")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/my_location").text, "我的位置:", "OK, 我的位置:", "errorrrrrr, 我的位置:")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/map").is_displayed(), True, "OK, 定位btn" , "errorrrrrr, 定位btn")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/location_name").text, "场景地点名称", "OK, 场景地点名称", "errorrrrrr, 场景地点名称")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/location_name_ed").text, self.str_list[0], "OK, " + self.str_list[0], "errorrrrrr, " + self.str_list[0])
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/headPicHint").text, "上传公共场景头像图片", "OK, 上传公共场景头像图片", "errorrrrrr, 上传公共场景头像图片")

        # 创建公共场景 - 上传头像
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/headPic").click()
        self.camera("从手机相册选择")
        sleep(3)

        # 选择图片作为头像
        varImages2 = self.driver.find_elements_by_id(sheetMain.cell_value(1, 5)+":id/image")
        x = 0
        for varImage in varImages2:
            if x == 5:
                varImage.click()
                break
            x = x + 1
        sleep(3)
        # 点击保存 （调用第三方手机ID）
        for i in range(1, 3):
            if self.productmodel == sheetMain.cell_value(i, 9).encode("utf-8"):
                self.driver.find_element_by_id(sheetMain.cell_value(i, 10)).click()
                break
        sleep(3)

        # 创建公共场景 - 场景地点名称
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/location_name_ed").send_keys(comName)

        # 创建公共场景  - 选择地点所属区域/商圈
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/business_area").text, "选择地点所属区域/商圈", "OK, 选择地点所属区域/商圈", "errorrrrrr, 选择地点所属区域/商圈")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/business_area").click()
        sleep(4)
        self.driver.swipe(self.screenX-100, 600, self.screenX-100, 600, 1000)  # 选择分类
        sleep(3)

        # 创建公共场景 - 选择地点分类
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/area_classify").text, "选择地点分类", "OK, 选择地点分类", "errorrrrrr, 选择地点分类")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/area_classify").click()
        sleep(4)
        self.driver.swipe(self.screenX-100, 600, self.screenX-100, 600, 1000)  # 选择分类
        sleep(3)

        # 创建公共场景 - 公共场景文字介绍
        self.driver.swipe(self.screenX/2, self.screenY-100, self.screenX/2, self.screenY-500, 1000)
        sleep(3)
        el4 = self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/contentParentLayout").find_element_by_xpath("//android.widget.ScrollView/android.widget.LinearLayout/android.widget.TextView[contains(@index,11)]")
        self.assertEqual(el4.text, self.str_list[1], "OK, " + self.str_list[1], "errorrrrrr, " + self.str_list[1])
        el4 = self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/contentParentLayout").find_element_by_xpath("//android.widget.ScrollView/android.widget.LinearLayout/android.widget.TextView[contains(@index,12)]")
        self.assertEqual(el4.text, self.str_list[2], "OK, " + self.str_list[2], "errorrrrrr, " + self.str_list[2])

        # 确认，返回到附近场景
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/sure").click()
        self.sendErrLog(u'nearCreateCom', u'附近场景 - 创建公共场景确认后报错')



    # 我的场景
    def drv_my(self):
        self.TestcaseModule()
    def myScene(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/my_scenes_tab").click()
        self.sendErrLog(u'myScene', u'附近场景 - 点击我的场景后报错')

        # 临时测试数据
        self.comName = "西北大学"

        # 遍历我的场景,进入刚刚创建的公共场景
        mySceneLists = self.driver.find_elements_by_id(sheetMain.cell_value(1, 5)+":id/my_scene_layout")

        vartmp = 0
        for mySceneList in mySceneLists:
            # mySceneList.find_element_by_id(sheetMain.cell_value(1, 5)+":id/scene_mark")  # 公
            # mySceneList.find_element_by_id(sheetMain.cell_value(1, 5)+":id/scene_address")  # 地址（分公共场景肯定有地址）
            self.varComSceneName = mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,0)]").text
            if self.varComSceneName == self.comName:
                # 公
                self.varGONG = mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[1]/android.widget.TextView[contains(@index,0)]").text
                # 公共场景名
                self.varComSceneName = mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,0)]").text
                # 公共场景地址
                self.varComSceneAddress = mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[3]/android.widget.TextView[contains(@index,0)]").text
                # 在场人数
                varPeopleNums = mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,1)]").text
                # 创建时间
                varComSceneTime = mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,2)]").text
                print "OK, " + self.varGONG + " , " + self.varComSceneName + " , " + self.varComSceneAddress + " , " + varPeopleNums + " , " + varComSceneTime
                mySceneList.click()
                vartmp = 1
                self.sendErrLog(u'myScene', u'我的场景 - 点击刚创建的公共场景名后报错')
                break
        self.assertEqual(vartmp, 1, "OK, 我的场景中公共场景名" , "Errorrrrrrr, 我的场景中未找到刚创建公共场景名！" )

        # except :
        #         print "12121212112"
                # try:
                #     mySceneList.find_element_by_id(sheetMain.cell_value(1, 5)+":id/scene_address")
                #     print mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,0)]").text + " , " + mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[3]/android.widget.TextView[contains(@index,0)]").text + " , " + mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,1)]").text + " , " + mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,2)]").text
                # except:
                #     print mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,0)]").text + " , " + mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,1)]").text + " , " + mySceneList.find_element_by_xpath("//child::android.widget.RelativeLayout[2]/android.widget.TextView[contains(@index,2)]").text

    def mySceneCom(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        sleep(2)
        # 公
        (a, b) = self.assertSplit(self.str_list[0])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b , "errorrrrrr, " + b)
        self.driver.find_element_by_id(a).click()
        sleep(2)

        # 公共场景、公共场景介绍文字、知道了
        for i in range(1, 4):
            (a, b) = self.assertSplit(self.str_list[i])
            self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b , "errorrrrrr, " + b)
        (a, b) = self.assertSplit(self.str_list[3])
        self.driver.find_element_by_id(a).click()  # 点击知道了
        sleep(2)

        self.assertContain(self.comName, self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/common_scene_name_and_number").text, "OK ,公共场景标题","Errorrrrrrr ,公共场景标题")

        # 浮动btn(只看好友)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/msgView").is_displayed(), True, "OK, 浮动btn(只看好友)" , "errorrrrrr, 浮动btn(只看好友)")

        # 发消息
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/content").text, "输入内容…", "OK, 输入内容…" , "errorrrrrr, 输入内容…")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/content").send_keys(u"大家好，我是莫妮卡，初次驾到请多关照！第一次使用场景鹿，感觉非常好用，可以在场景里找到志同道合的小伙伴，平时喜欢唱歌和烹饪，有空与大家一起分享心得，🙏")
        sleep(1)
        self.driver.keyevent(66)
        sleep(2)

        # 点击表情符号
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/face").is_displayed(), True, "OK, 表情符号btn" , "errorrrrrr, 表情符号btn")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/face").click()
        sleep(2)
        tmpFaces = self.driver.find_elements_by_id(sheetMain.cell_value(1, 5)+":id/faceViewPager")
        for tmpFace in tmpFaces:
            tmpFace.find_element_by_xpath("//android.widget.GridView/android.widget.RelativeLayout[contains(@index,3)]").click()
            self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/send").click()
            break
        # 选择第二套头像
        (a, b, c, d) = self.screenWidthHeight(sheetMain.cell_value(1, 5)+":id/faceViewPager")
        self.driver.swipe(b-10, (c+d)/2, 10, (c+d)/2, 1000)
        sleep(3)
        tmpFaces2 = self.driver.find_elements_by_id(sheetMain.cell_value(1, 5)+":id/faceViewPager")
        for tmpFace2 in tmpFaces2:
            tmpFace2.find_element_by_xpath("//android.widget.GridView/android.widget.RelativeLayout[contains(@index,3)]").click()
            break

        self.driver.find_element_by_id("com.mowin.scenesdeer:id/private_msg_parent_layout").click()
        sleep(2)

        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/moreFunc").is_displayed(), True, "OK, 更多功能btn" , "errorrrrrr, 更多功能btn")
        # 选择拍照
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/moreFunc").click()
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/camera").text,"拍照","OK, 拍照" , "errorrrrrr, 拍照")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/camera").click()
        sleep(3)
        self.driver.swipe(self.screenX/2, self.screenY/2, self.screenX/2, self.screenY/2, 1000)
        # print self.screenX/2
        # print self.screenY/2
        sleep(4)
         # 点击保存 （调用第三方手机ID）
        for i in range(1, 3):
            if self.productmodel == sheetMain.cell_value(i, 9).encode("utf-8"):
                self.driver.find_element_by_id(sheetMain.cell_value(i, 11)).click()
                break
        sleep(3)

        # 选择图片
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/moreFunc").click()
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/picture").text,"图片","OK, 图片" , "errorrrrrr, 图片")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/picture").click()
        # 选择图片作为头像
        varImages = self.driver.find_elements_by_id(sheetMain.cell_value(1, 5)+":id/image")
        x = 0
        for varImage in varImages:
            if x == 4:
                varImage.click()
                break
            x = x + 1
        sleep(2)

        # 选择小视频
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/moreFunc").click()
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/video").text,"小视频","OK, 小视频" , "errorrrrrr, 小视频")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/video").click()
        sleep(5)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/recorder").text,"按住拍","OK, 按住拍" , "errorrrrrr, 按住拍")

        (a, b, c, d)=self.screenWidthHeight(sheetMain.cell_value(1, 5)+":id/recorder")
        self.driver.swipe((a+b)/2, (c+d)/2, (a+b)/2, (c+d)/2, 10000)
        sleep(8)

        # 点击 +
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/expand").click()
        # + -  点击场景信息
        self.driver.swipe(self.screenX-100, 300, self.screenX-100, 300, 1000)
        self.sendErrLog(u'mySceneCom', u'我的场景 - {公共场景} -  + - 点击场景信息后报错')


    def mySceneInfo(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        # 场景信息页面内
        (a, b) = self.assertSplit(self.str_list[0])
        self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/sceneName").text, self.varComSceneName, "OK, " + self.comName, "errorrrrrr, " + self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/sceneName").text + " <> " + self.comName)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/baseInfoLayout").is_displayed(), True, "OK, 背景图" ,"errorrrrrr, 背景图")
        self.assertContain("场景ID", self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/sceneId").text, "OK, " + self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/sceneId").text, "errorrrrrr, " + self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/sceneId").text)
        self.assertEqual(self.getElementExist(sheetMain.cell_value(1, 5)+":id/category"), True, "OK, " + self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/category").text, "errorrrrrr, " + self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/category").text)
        # 本场景还未上传... , 场景公告 ,电话：无,分享场景
        for i in range(1, 5):
            (a, b) = self.assertSplit(self.str_list[i])
            self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)

        self.assertContain("欢迎加入", self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/sceneAnnouncement").text,"OK, " + self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/sceneAnnouncement").text, "errorrrrrr, " + self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/sceneAnnouncement").text)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/address").text, "地点：" + self.varComSceneAddress, "OK, 地址：" + self.varComSceneAddress, "errorrrrrr, 地址：" + self.varComSceneAddress)
        # print "(" + self.driver.find_element_by_id(self.str_list[8]).text + ")"
        # print "(地点：" + self.varComSceneAddress + ")"

        # 看看小伙伴们的足迹
        self.assertContain("看看小伙伴们的足迹(", self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/footPrint").text, "OK, " + self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/footPrint").text, "errorrrrrr, " + self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/footPrint").text)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/footPrint").click()
        sleep(3)
        self.assertContain("足迹(", self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "OK, " + self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text, "errorrrrrr, " + self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/title").text)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/search_layout").is_displayed(), True, "OK, 搜索框", "errorrrrrr, 搜索框")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/search_logo").is_displayed(), True, "OK, 搜索icon", "errorrrrrr, 搜索icon")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/search").text, "搜索", "OK, 搜索", "errorrrrrr, 搜索")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/filter").text, "排序筛选", "OK, 排序筛选", "errorrrrrr, 排序筛选")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/arrow_bottom").is_displayed(), True, "OK, 向下箭头icon", "errorrrrrr, 向下箭头icon")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/back").click()

        # 分享场景

        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/shareScene").click()
        self.toShare("朋友圈")
        (a, b, c, d) = self.screenWidthHeight(sheetMain.cell_value(1, 5)+":id/contentParentLayout")
        self.driver.swipe(self.screenX-100, d-1, self.screenX-100, c+1, 1000)
        sleep(2)

        # 我在本场景的昵称
        self.assertEqual("我在本场景的昵称", self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/myNickNameLayout").find_element_by_xpath("//android.widget.TextView[contains(@index,0)]").text, "Ok, 我在本场景的昵称" , "errorrrrrr, 我在本场景的昵称" )

        # 自动留下足迹，置顶聊天，查找聊天记录，报错／补充信息，清空聊天记录, 删除并退出
        for i in range(5, 11):
            (a, b) = self.assertSplit(self.str_list[i])
            self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)

        # 查找聊天记录
        (a, b) = self.assertSplit(self.str_list[7])
        self.driver.find_element_by_id(a).click()
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/search_scene").text, "搜索", "OK, 搜索", "errorrrrrr, 搜索")
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/search_scene").send_keys(u"john")
        sleep(2)
        self.driver.keyevent(66)
        sleep(2)
        x = self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/list_view").find_element_by_xpath("//child::android.widget.LinearLayout[1]/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[contains(@index,0)]").text
        y = self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/list_view").find_element_by_xpath("//child::android.widget.LinearLayout[1]/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView[contains(@index,0)]").text
        print x + " , " + y

        # # 删除并退出
        (a, b) = self.assertSplit(self.str_list[10])
        self.driver.find_element_by_id(a).click()
        sleep(2)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/positive").click()  # 点击退出
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/back").click()


    def mySceneInCom(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        # 点击加号
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/add_scene").click()
        # 公共场景 - 添加到我的场景
        self.driver.swipe(self.screenX-100, 400, self.screenX-100, 400, 1000)
        sleep(4)


    def mySceneShare(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        # 点击加号
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/add_scene").click()
        # 公共场景 - 召唤小伙伴
        self.driver.swipe(self.screenX-100, 800, self.screenX-100, 800, 1000)
        # ??? 检查

    def mySceneCreateSplit(self, varSplitName):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        self.varSplitName = varSplitName
        # 点击加号
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/add_scene").click()
        # # 创建群组
        self.driver.swipe(self.screenX-100, 600, self.screenX-100, 600, 1000)
        sleep(2)

        # 遍历检查创建群组页面元素
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/title").text, "创建群组", "OK, 创建群组", "errorrrrrr, 创建群组")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/sceneMark").text, "公", "OK, 公", "errorrrrrr, 公")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/parentSceneName").text, self.comName, "OK, " + self.comName, "errorrrrrr, " + self.comName)

        # 文案检查
        for i in range(0, 4):
            (a, b) = self.assertSplit(self.str_list[i])
            self.assertEqual(self.driver.find_element_by_id(a).text, b, "OK, " + b, "errorrrrrr, " + b)

        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/scenesName").send_keys(varSplitName)
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/category").click()
        sleep(3)
        tmpTypes = self.driver.find_elements_by_id("com.mowin.scenesdeer:id/pop_listview_right")
        for tmpType in tmpTypes:
            tmpType.find_element_by_xpath("//android.widget.RelativeLayout[contains(@index,2)]").click()
            break
        sleep(4)

        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/commit").click()

        # 创建成功-完善资料
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/title").text, "创建成功-完善资料", "OK, 创建成功-完善资料", "errorrrrrr, 创建成功-完善资料")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/sceneName").text, self.varSplitName, "OK, " + self.varSplitName, "errorrrrrr, " + self.varSplitName)
        self.assertContain("群组ID",self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/sceneId").text, "OK, 群组ID", "errorrrrrr, 群组ID")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/category").text, "80党", "OK, 80党", "errorrrrrr, 80党")
        self.assertContain("群组成员(",self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/sceneMemberHint").text, "OK, 群组成员(", "errorrrrrr, 群组成员(")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/head_pic").is_displayed(), True, "OK, 群组成员头像btn", "errorrrrrr, 群组成员头像btn")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/add_member").is_displayed(), True, "OK, 群组成员+btn", "errorrrrrr, 群组成员+btn")

        # 点击群成员 + （跳转到添加联系人）
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/add_member").click()
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/title").text, "添加联系人", "OK, 添加联系人", "errorrrrrr, 添加联系人")
        # ？？？
        # 调用添加联系人模块
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/back").click()

        #  召唤小伙伴 ，调用模块 ？？？ 不再编写。
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/shareScene").text, "召唤小伙伴", "OK, 召唤小伙伴", "errorrrrrr, 召唤小伙伴")


        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/addressHint").text, "地址", "OK, 地址", "errorrrrrr, 地址")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/address").text, "输入所在地点楼层、门牌号等", "OK, 输入所在地点楼层、门牌号等", "errorrrrrr, 输入所在地点楼层、门牌号等")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/phoneHint").text, "电话", "OK, 电话", "errorrrrrr, 电话")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/phoneNumber").text, "输入联系电话", "OK, 输入联系电话", "errorrrrrr, 输入联系电话")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/announcementHint").text, "群组公告", "OK, 群组公告", "errorrrrrr, 群组公告")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/announcement").text, "输入公告内容, 让大家更了解你的群组", "OK, 输入公告内容, 让大家更了解你的群组", "errorrrrrr, 输入公告内容, 让大家更了解你的群组")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/addSceneVerifyHint").text, "加群组验证", "OK, 加群组验证", "errorrrrrr, 加群组验证")
        self.driver.swipe(self.screenX/2,self.screenY-10,self.screenX/2,self.screenY/2/2,1000)
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/allow").text, "允许任何人", "OK, 允许任何人", "errorrrrrr, 允许任何人")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/verify").text, "需身份验证", "OK, 需身份验证", "errorrrrrr, 需身份验证")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/disallow").text, "不允许任何人", "OK, 不允许任何人", "errorrrrrr, 不允许任何人")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/publicSceneHint").text, "群组公开", "OK, 群组公开", "errorrrrrr, 群组公开")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/allowGuest").text, "允许游客访问", "OK, 允许游客访问", "errorrrrrr, 允许游客访问")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5) + ":id/disAllowGuest").text, "禁止游客访问", "OK, 禁止游客访问", "errorrrrrr, 禁止游客访问")
        self.assertEqual(self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/actionBar").find_element_by_xpath("//android.widget.TextView[contains(@index,2)]").text,"完成", "OK, 完成", "errorrrrrr, 完成")

        # 点击完成 （返回到群组聊天页）
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/actionBar").find_element_by_xpath("//android.widget.TextView[contains(@index,2)]").click()

    def splitSceneInfoElement(self):
        print ">" * 150
        print sheetTestCase.cell_value(self.l, 4)
        # ?? 遍历群主信息页
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/back").click()





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
        self.driver.find_element_by_id(sheetMain.cell_value(1, 5)+":id/back").click()



if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(Boluome123)  # 构造测试集
    unittest.TextTestRunner(verbosity=2).run(suite1)  # 执行测试

