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



class cjl(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4'
        desired_caps['deviceName'] = 'appium'
        desired_caps['appPackage'] = 'com.kuping.android.boluome.life'
        desired_caps['appActivity'] = 'com.kuping.android.boluome.life.ui.main.SplashActivity'
        desired_caps['unicodeKeyboard'] = 'True'
        desired_caps['resetKeyboard'] = 'True'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        reload(sys)
        sys.setdefaultencoding('utf8')

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def test_Main(self):
        print "这里写程序"


if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(cjl)
    unittest.TextTestRunner(verbosity=2).run(suite1)

