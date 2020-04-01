# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description:
#***************************************************************

import os, sys, unittest, xlwt, xlrd, MySQLdb, tempfile,shutil,chardet,random,webbrowser,platform,string,datetime,redis,commands,urllib2,MultipartPostHandler
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import smtplib,pytesseract
from email.mime.text import MIMEText
from email.header import Header
from time import sleep
from xlwt.Style import *
from xlrd import open_workbook
from xlutils.copy import copy
import time,Image,ImageChops
from pymongo import MongoClient

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from time import sleep
import unittest,time,sys,HTMLTestRunner


# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# from selenium.common.exceptions import NoSuchElementException

# 参数化
varExcel = "/Users/linghuchong/Downloads/51/Project/XXX_AutoTest/baidu/TestData/Baidu1_0.xls"
bk = xlrd.open_workbook(varExcel, formatting_info=True)
newbk = copy(bk)
sheetCase = bk.sheet_by_name("case")
sheetParam = bk.sheet_by_name("param")

# driver = webdriver.Firefox(firefox_profile=None, firefox_binary=None, timeout=30, capabilities=None, proxy=None, executable_path='/Users/linghuchong/Downloads/51/ForWin/selenium/selenium3/geckodriver', firefox_options=None, log_path='geckodriver5.log')
# driver.implicitly_wait(10)
# url ="http://www.baidu.com"
#
# class BaseURL(object):
#
#     def __init__(self, selenium_driver, base_url, pagetitle):
#         self.driver = selenium_driver
#         self.base_url = base_url
#         self.pagetitle = pagetitle
#         # self.varExcel = varExcel
#         # self.sheetCase = bk.sheet_by_name("case")
#         # self.sheetParam = bk.sheet_by_name("param")
#         # styleRed = xlwt.easyxf('font: name Times New Roman, color-index red')
#         # styleBlue = xlwt.easyxf('font: name Times New Roman, color-index blue')
#         # styleGray25 = xlwt.easyxf('font: name Times New Roman, color-index gray25')
