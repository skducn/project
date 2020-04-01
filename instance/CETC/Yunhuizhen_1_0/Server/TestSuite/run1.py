# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description:
# HTMLTestRunner.py /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7
#***************************************************************

import os, sys, unittest, xlwt, xlrd, MySQLdb, tempfile,shutil,chardet,random,webbrowser,platform,string,datetime,redis,commands,urllib2,MultipartPostHandler
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from xlwt.Style import *
from xlrd import open_workbook
from xlutils.copy import copy
import unittest,time,HTMLTestRunner
# sys.path.append('//Users//linghuchong//Downloads//51//Project//CETC//DKDJ_1_0//Server//PageObject//LoginPO.py')
from TestCase import *

class Run1(unittest.TestCase):
    suite = unittest.TestSuite()
    varExcel = os.path.abspath(r"../TestData/Yunhuizhen_1_0.xls")
    varExcelReportPath = os.path.abspath(r"../TestReport/Yunhuizhen_")
    varExcelReport = ""
    l_varExcelReport = varExcelReportPath.split('/')
    for i in range(1, len(l_varExcelReport)):
        varExcelReport = varExcelReport + "//" + l_varExcelReport[i]

    bk = xlrd.open_workbook(varExcel, formatting_info=True)
    sheetCase = bk.sheet_by_name("case")
    for i in range(1, sheetCase.nrows):
        if sheetCase.cell_value(i, 0) == "Y":
            exec("suite.addTest(unittest.makeSuite(" + sheetCase.cell_value(i, 2) + "))")

    fp = open(varExcelReport + time.strftime("%Y-%m-%d_%H:%M:%S",time.localtime(time.time())) + '.html', 'wb')
    print varExcelReport + time.strftime("%Y-%m-%d_%H:%M:%S",time.localtime(time.time())) + '.html'
    HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'云惠诊1.0', description=u'测试报告').run(suite)
    fp.close()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Run1)

