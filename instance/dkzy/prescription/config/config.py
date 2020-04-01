# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2018-3-15
# Description:
# HTMLTestRunner.py /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7

# firefox for mac
# 下载：https://github.com/mozilla/geckodriver/releases/tag/v0.15.0 （geckodriver 0.15）
# 解压：geckodriver 复制到 /usr/local/bin
# geckodriver 0.15版本安装路径： /usr/local/Cellar/geckodriver/0.15.0/bin
# 更新geckodriver驱动 , brew install geckodriver , 截止2017/11/10 最新版本0.20 ，但不能用。建议用0.15版本（测试可用）
# from selenium import webdriver
# driver = webdriver.Firefox(firefox_profile=None, firefox_binary=None, timeout=30, capabilities=None, proxy=None, executable_path='/usr/local/bin/geckodriver', firefox_options=None, log_path='geckodriver.log')
# driver.implicitly_wait(10)

# chrome for mac
# 下载：http://chromedriver.storage.googleapis.com/index.html 最新2.37 与 chrome浏览器版本 65.0.3325.162（正式版本） （64 位）匹配。
# 解压：chromedriver 复制到 /usr/local/bin
# from selenium import webdriver
# driver = webdriver.Chrome()

# selenium driver for mac
# 通过命令行安装：sudo -H pip install selenium
# selenium目前对Python3支持并不好，所以还是使用自带2.7.10。
# 显示selenium当前版本的命令 pip show selenium
# Name: selenium
# Version: 3.3.1
# Summary: Python bindings for Selenium
# Home-page: https://github.com/SeleniumHQ/selenium/
# Author: UNKNOWN
# Author-email: UNKNOWN
# License: Apache 2.0
# Location: /Library/Python/2.7/site-packages

#***************************************************************

import sys, os, unittest,time,xlwt, xlrd, MySQLdb
from xlutils.copy import copy
reload(sys)
sys.setdefaultencoding("utf-8")
from selenium import webdriver
import json,xlwt,datetime
from Public.PageObject.LevelPO import *
from selenium.webdriver.common.keys import Keys
from random import choice
from pytesseract import *
from PIL import Image
from selenium.webdriver.common.by import By
from Public.PageObject.BasePage import BasePage
from time import sleep
# from pytesser import *
import pytesseract

varProjectTitle = '审方处方web'

varUrlB = "https://cetc.iotcetc.com:8084/phphis/web/app.php/login"
varUrlC = "https://cetc.iotcetc.com:8084/terminal-v2/"
# varURLtest = "https://cetc.iotcetc.com:8084/phphis-branches/consult-history-dev/web/app.php/login/"

# varLogPrefixPath = '/Users/linghuchong/Downloads/51/Project/Dangjian/log/dangjian_'   # log文件的前缀
# varExcel = '/Users/linghuchong/Downloads/51/Project/Dangjian/TestData/web20.xls'   # 绝对路径
# bk = xlrd.open_workbook(varExcel, formatting_info=True)
# newbk = copy(bk)
# sheetParam = bk.sheet_by_name("param")
# sheetCase = bk.sheet_by_name("case")
# styleRed = xlwt.easyxf('font: name Times New Roman, color-index red')

varTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # 当天日期时间，格式：20170914143616982，类型是 str，
varYMD = datetime.datetime.now().strftime('%Y-%m-%d')  # 当天日期，格式：2016-06-28 ， 类型是 str


# 初始化参数化
# varExcel = os.path.abspath(r"web10.xls")
# print varExcel
# varExcel = '/Users/linghuchong/Downloads/51/Project/Dangjian/TestData/web10.xls'
# varReport = "/Users/linghuchong/Downloads/51/Project/CJL/report/CJLreport1_0.html"
# varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 获取当天日期时间,格式：20161020130318
# bk = xlrd.open_workbook(varExcel, formatting_info=True)
# newbk = copy(bk)
# sheetMain = bk.sheet_by_name("main")
# sheetTestCase = bk.sheet_by_name("testcase")
# styleRed = xlwt.easyxf('font: name Times New Roman, color-index red')
# styleBlue = xlwt.easyxf('font: name Times New Roman, color-index blue')
# styleGray25 = xlwt.easyxf('font: name Times New Roman, color-index gray25')

# conn = MySQLdb.connect(host='10.111.3.5', user='cetc', passwd='20121221', db='dangjian', port=3306, use_unicode=True)
# cur = conn.cursor();cur.execute('SET NAMES utf8;');conn.set_character_set('utf8');cur.execute('show tables')
#

# # 加启动配置 (解决：Chrome正受到自动测试软件的控制)
# (Session info: chrome=65.0.3325.181) (Driver info: chromedriver=2.37 for win32 )
options = webdriver.ChromeOptions()
options.add_argument('disable-infobars')
driverB = webdriver.Chrome(chrome_options=options)

# driverB = webdriver.Firefox()
# driverB.implicitly_wait(10)


# driver = webdriver.Firefox(firefox_profile=None, firefox_binary=None, timeout=30, capabilities=None, proxy=None, executable_path='/Users/linghuchong/Downloads/51/ForWin/Selenium/selenium3/geckodriver', firefox_options=None, log_path='geckodriver5.log')
# driver = webdriver.Firefox(firefox_profile=None, firefox_binary=None, timeout=30, capabilities=None, proxy=None, executable_path='/usr/local/Cellar/geckodriver/0.19.1/bin/geckodriver', firefox_options=None)
# driver = webdriver.Firefox(firefox_profile=None, firefox_binary=None,
#                  timeout=30, capabilities=None, proxy=None,
#                  executable_path=u"/usr/local/Cellar/geckodriver/0.19.1/bin/geckodriver", firefox_options=None,
#                  log_path="geckodriver.log")
# driver = webdriver.PhantomJS(executable_path='/usr/local/bin/geckodriver')
# driver = webdriver.Firefox(executable_path = '/usr/local/Cellar/geckodriver/0.19.1/bin/geckodriver')
# browser = webdriver.Firefox()




