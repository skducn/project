# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description: android自动化测试框架
#***************************************************************

import os, sys, unittest, xlwt, xlrd, MySQLdb, tempfile,shutil,chardet,random,webbrowser,platform,string,datetime,redis
from email.mime.text import MIMEText
from email.mime.multipart import *
import mimetypes
import email
import smtplib
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
import mimetypes
import base64
import smtplib
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
#from jhj_v1_5_setup import *
#win32api,win32con,HTMLTestRunner
# import HTMLTestRunner
from pymongo import MongoClient
# from CJLinterfaceDriver import *
# from ssh_cmd import *
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from time import sleep

from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
import subprocess

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


# # 参数化
# varExcel = os.path.abspath(r"web20.xls")
# # varReport = "/Users/linghuchong/Downloads/51/Project/CJL/report/CJLreport1_0.html"
# varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 获取当天日期时间,格式：20161020130318
# bk = xlrd.open_workbook(varExcel, formatting_info=True)
# newbk = copy(bk)
# sheetMain = bk.sheet_by_name("main")
# sheetTestCase = bk.sheet_by_name("testcase")
# styleRed = xlwt.easyxf('font: name Times New Roman, color-index red')
# styleBlue = xlwt.easyxf('font: name Times New Roman, color-index blue')
# styleGray25 = xlwt.easyxf('font: name Times New Roman, color-index gray25')


class dkdj(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # 获取手机制造商信息,如 adb shell getprop | grep "model\|version.sdk\|manufacturer\|hardware\|platform\|revision\|serialno\|product.name\|brand"
        androidVersion = subprocess.getoutput('adb shell getprop ro.build.version.release')
        androidSerialno = subprocess.getoutput('adb shell getprop ro.serialno')
        desired_caps = {}
        # desired_caps['automationName'] = 'Uiautomator2'
        print("222222")

        desired_caps['platformName'] = 'Android'
        # desired_caps['platformVersion'] = str(float(androidVersion[0:3]))
        desired_caps['platformVersion'] = '6.0.1'
        desired_caps['deviceName'] = androidSerialno
        # desired_caps['app'] = '/Users/linghuchong/Downloads/51/android/dangjian/PartyBuilding1.0.0_prod.apk'
        # desired_caps['app'] = 'D:\\51\\python\\project\\zyjk\\EHR\\ehr_dmp_release_ttest_v1.3.0.apk'
        desired_caps['appPackage'] = 'zy.android.healthstatisticssystem'
        desired_caps['appActivity'] = 'zy.android.healthstatisticssystem.mvp.ui.activity.SplashActivity'
        desired_caps['unicodeKeyboard'] = 'True'
        desired_caps['resetKeyboard'] = 'True'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        # reload(sys)
        # sys.setdefaultencoding('utf8')

        print(">" * 150)
        # 手机信息定义与输出
        # 定义手机分辨率的宽,高
        self.screenX = self.driver.get_window_size()['width']
        self.screenY = self.driver.get_window_size()['height']
        tmpProductmodel = subprocess.getoutput('adb shell getprop ro.product.model')
        tmpProductdevice = subprocess.getoutput('adb shell getprop ro.product.device')
        tmpSdk = subprocess.getoutput('adb shell getprop ro.build.version.sdk')
        tmpAbi = subprocess.getoutput('adb shell getprop ro.product.cpu.abi')
        tmpSerialno = subprocess.getoutput('adb shell getprop ro.serialno')
        self.productmodel = tmpProductmodel.strip()
        print("测试机品牌 = " + str(tmpProductmodel.strip()) + " , 设备号 = " + str(tmpProductdevice.strip()) + " , 分辨率 = " + str(self.screenX) + "*" + str(self.screenY) + " , Android版本 = " + str(androidVersion.strip()) + " , SDK = " + str(tmpSdk.strip()) + " , CPU = " + str(tmpAbi.strip()) + " , SerialNo = " + str(tmpSerialno.strip()))


    @classmethod
    def tearDownClass(self):
        self.driver.quit()



if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(dkdj)  # 构造测试集
    unittest.TextTestRunner(verbosity=2).run(suite1)  # 执行测试

