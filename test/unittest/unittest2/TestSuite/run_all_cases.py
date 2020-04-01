# coding: utf-8
#****************************************************************
# Author     : John
# Version    : 1.0.0
# Date       : 2017-1-20
# Description:
# Function   :
#****************************************************************

import unittest,time,sys,HTMLTestRunner
from TestCase import *

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(Loginlevel2.Loginlevel2))
suite.addTest(unittest.makeSuite(Hao123.Hao12345))

fp =open('//Users//linghuchong//Downloads//51//Project//XXX_AutoTest//baidu//TestReport//Baidu_' + time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time())) + '.html', 'wb')
HTMLTestRunner.HTMLTestRunner(stream=fp,title='run_all_cases',description='测试报告').run(suite)
fp.close()



# caselist = os.listdir('//Users//linghuchong//Downloads//51//Project//XXX_AutoTest//baidu//TestSuite_Baidu//TestCase')
# for a in caselist:
#     s =a.split('.')[1]
#     if s =='py':
#         os.system('//Users//linghuchong//Downloads//51//Project//XXX_AutoTest//baidu//TestSuite_Baidu//TestCase//%s 1>>log.txt 2>&1'%a)

