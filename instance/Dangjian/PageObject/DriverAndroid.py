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

# print sys.path
# from resource.source.comparePic import *
# from resource.source import test2

#****************************************************************
# x = os.gxetcwd()
# print
#
# srcPath=r"DKDJ1_0.xls"
# path=os.path.abspath(srcPath)
# print "全路径为：",path
# print "路径名，文件名",os.path.split(path)


# 参数化
varExcel = os.path.abspath(r"web20.xls")
# varReport = "/Users/linghuchong/Downloads/51/Project/CJL/report/CJLreport1_0.html"
varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 获取当天日期时间,格式：20161020130318
# varTableDetails = "/Users/linghuchong/Downloads/51/Project/CJL/report/CJLtable" + varTimeYMDHSM + ".html"
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


class dkdj(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        # 获取手机制造商信息,如 adb shell getprop | grep "model\|version.sdk\|manufacturer\|hardware\|platform\|revision\|serialno\|product.name\|brand"
        androidVersion = commands.getoutput('adb shell getprop ro.build.version.release')
        androidSerialno = commands.getoutput('adb shell getprop ro.serialno')
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = "5.0"  #str(float(androidVersion[0:3]))
        desired_caps['deviceName'] = androidSerialno
        desired_caps['appPackage'] = 'com.cetc.partybuilding'
        desired_caps['appActivity'] = 'com.cetc.partybuilding.activity.InitActivity'
        desired_caps['unicodeKeyboard'] = 'True'
        desired_caps['resetKeyboard'] = 'True'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        reload(sys)
        sys.setdefaultencoding('utf8')




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
                      if "=" in N:
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
                      newWs.write(l, 0, varTimeYMDHSM, styleBlue)
                      newbk.save(varExcel)
              except:
                  print "Errorrrrrrr , Excel("+str(l+1)+") , " + sheetTestCase.cell_value(case1, 2) + " , " + sheetTestCase.cell_value(l, 3) + " , " +sheetTestCase.cell_value(l, 4) + " , " +sheetTestCase.cell_value(l, 5)
                  newWs = newbk.get_sheet(1)
                  newWs.write(l, 0, varTimeYMDHSM, styleRed)
                  newbk.save(varExcel)







    def msgbox(self):
        print "取消升级"
        sleep(3)

        self.driver.find_element_by_id("android:id/button1").click()
        sleep(3)
        self.driver.find_element_by_id("com.cetc.partybuilding:id/news_more_btn").click()
        self.driver.find_element_by_id("android:id/tabs").find_element_by_xpath("//android.widget.FrameLayout[contains(@index,1)]").find_element_by_id("com.cetc.partybuilding:id/btn_text").click()
        sleep(5)
        print self.screenY
        self.driver.swipe(self.screenX/2, self.screenY/2, self.screenX/2, self.screenY/2+200, 1000)
        sleep(3)
        print self.driver.find_element_by_id("com.cetc.partybuilding:id/listview").find_element_by_xpath("//android.widget.LinearLayout[contains(@index,1)]").find_element_by_id("com.cetc.partybuilding:id/title_tv").text

        # self.assertEqual(self.driver.find_element_by_id("com.cetc.partybuilding:id/item_notice_tv_title").text,"历史通知", "OK, 消息盒子-历史通知文案正确", "errorrrrrr, 消息盒子-历史通知文案错误")
        sleep(1212)



if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(dkdj)  # 构造测试集
    unittest.TextTestRunner(verbosity=2).run(suite1)  # 执行测试

