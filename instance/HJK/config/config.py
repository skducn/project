# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description:
# HTMLTestRunner.py /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7
# 在线更新最新的geckodriver驱动命令， brew install geckodriver   ,截止11/10 最新版本1.19.1 但不好用。建议用0.15版本
# geckodriver 使用0.15版本 /usr/local/Cellar/geckodriver/0.15.0/bin
# 将geckodriver 复制到 /usr/local/bin
# 显示selenium当前版本的命令 pip show selenium
# Name: selenium
# Version: 3.7.0

#***************************************************************

import sys, os, unittest,time,HTMLTestRunner,xlwt, xlrd, MySQLdb
from xlutils.copy import copy
reload(sys)
sys.setdefaultencoding("utf-8")
from selenium import webdriver

from Public.PageObject.LevelPO import *
from selenium.webdriver.common.keys import Keys
from random import choice

from pytesseract import *
from PIL import Image
from selenium.webdriver.common.by import By
from Public.PageObject.BasePage import BasePage
from time import sleep
import json,xlwt,datetime
# from pytesser import *
# import Image

# varExcel = os.path.abspath(r"../TestData/Cos.xls")  # run1, 批量跑
# varExcel = os.path.abspath(r"../../TestData/Cos.xls")  # 单独运行
# varExcel = os.path.abspath(r"/Users/linghuchong/Downloads/51/Project/Cos/TestData/Cos.xls")  # run1, 批量跑

varProjectTitle = u'党建 - 学思践悟'

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
varExcel = os.path.abspath(r"web10.xls")
print varExcel
# varExcel = '/Users/linghuchong/Downloads/51/Project/Dangjian/TestData/web10.xls'
# varReport = "/Users/linghuchong/Downloads/51/Project/CJL/report/CJLreport1_0.html"
varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 获取当天日期时间,格式：20161020130318
bk = xlrd.open_workbook(varExcel, formatting_info=True)
newbk = copy(bk)
sheetMain = bk.sheet_by_name("main")
sheetTestCase = bk.sheet_by_name("testcase")
styleRed = xlwt.easyxf('font: name Times New Roman, color-index red')
styleBlue = xlwt.easyxf('font: name Times New Roman, color-index blue')
styleGray25 = xlwt.easyxf('font: name Times New Roman, color-index gray25')

conn = MySQLdb.connect(host='10.111.3.5', user='cetc', passwd='20121221', db='dangjian', port=3306, use_unicode=True)
cur = conn.cursor();cur.execute('SET NAMES utf8;');conn.set_character_set('utf8');cur.execute('show tables')
#
# driver = webdriver.Firefox(firefox_profile=None, firefox_binary=None, timeout=30, capabilities=None, proxy=None, executable_path='/usr/local/bin/geckodriver', firefox_options=None, log_path='geckodriver.log')
# driver.implicitly_wait(10)


# driver = webdriver.Firefox(firefox_profile=None, firefox_binary=None, timeout=30, capabilities=None, proxy=None, executable_path='/Users/linghuchong/Downloads/51/ForWin/Selenium/selenium3/geckodriver', firefox_options=None, log_path='geckodriver5.log')
# driver = webdriver.Firefox(firefox_profile=None, firefox_binary=None, timeout=30, capabilities=None, proxy=None, executable_path='/usr/local/Cellar/geckodriver/0.19.1/bin/geckodriver', firefox_options=None)
# driver = webdriver.Firefox(firefox_profile=None, firefox_binary=None,
#                  timeout=30, capabilities=None, proxy=None,
#                  executable_path=u"/usr/local/Cellar/geckodriver/0.19.1/bin/geckodriver", firefox_options=None,
#                  log_path="geckodriver.log")
# driver = webdriver.PhantomJS(executable_path='/usr/local/bin/geckodriver')
# driver = webdriver.Firefox(executable_path = '/usr/local/Cellar/geckodriver/0.19.1/bin/geckodriver')
# browser = webdriver.Firefox()




